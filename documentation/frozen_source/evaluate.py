"""Offline evaluation with explicit coverage checks and independently derived truth."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
from study import ROOT, DATASET, CONDITIONS, QUESTIONS, QUESTION_BY_ID, REPLICATIONS, SEED, scalar_equal, verify_answer, digest
from ground_truth import derive
from run_experiment import read_jsonl

def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return None, None
    if not 0 <= k <= n:
        raise ValueError('Invalid binomial counts')
    p, d = k/n, 1+z*z/n
    center = (p+z*z/(2*n))/d
    half = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return max(0,center-half), min(1,center+half)

def chart_matches(receipt, expected):
    if not receipt or not receipt.get('ok') or not receipt.get('chart_file'):
        return False
    path = Path(receipt['chart_file'])
    if not path.is_absolute():
        path = ROOT/path
    if not path.is_file() or path.stat().st_size == 0:
        return False
    if receipt.get('kind') != expected['kind'] or receipt.get('x') != expected['x'] or set(receipt.get('ys', [])) != set(expected['ys']):
        return False
    rows = receipt.get('rows', [])
    x, ys = expected['x'], expected['ys']
    if len(rows) != len(expected['rows']):
        return False
    def keyed(records):
        return {str(r[x]): r for r in records}
    try:
        # Normalize numeric categories such as 2008 and 2008.0.
        def key(v):
            try:
                return str(float(v))
            except (TypeError, ValueError):
                return str(v).casefold()
        actual = {key(r[x]): r for r in rows}
        target = {key(r[x]): r for r in expected['rows']}
        if len(actual) != len(rows) or set(actual) != set(target):
            return False
        if not all(scalar_equal(actual[k][y], target[k][y]) for k in target for y in ys):
            return False
        if expected['kind'] == 'line':
            return [float(r[x]) for r in rows] == sorted(float(r[x]) for r in rows)
        return True
    except (KeyError, TypeError, ValueError):
        return False

def validate_records(records, manifest, allow_partial=False):
    plans = {x['run_id']: x for x in manifest['study']['plan']}
    ids = [x['run_id'] for x in records]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate run IDs: do not silently deduplicate experiment data')
    if set(ids)-set(plans):
        raise ValueError('Unscheduled run found')
    if manifest['study']['dataset_sha256'] != digest(DATASET.read_bytes()):
        raise ValueError('Dataset differs from the frozen experiment')
    for r in records:
        p = plans[r['run_id']]
        for field in ('phase','condition','question_id','replication','inject_failure'):
            if r[field] != p[field]:
                raise ValueError(f'Run metadata mismatch for {r["run_id"]}: {field}')
        if r['dataset_sha256'] != manifest['study']['dataset_sha256'] or r['model'] != manifest['study']['model']:
            raise ValueError('Mixed dataset or model versions')
        prompt = manifest['study']['prompts'][r['condition']]
        if r['system_prompt_sha256'] != digest(prompt.encode()):
            raise ValueError('Mixed prompt versions')
        if r['temperature'] != manifest['study']['temperature']:
            raise ValueError('Mixed sampling settings')
    missing = sorted(set(plans)-set(ids))
    if missing and not allow_partial:
        raise ValueError(f'{len(missing)} scheduled runs missing. Use --allow-partial for explicitly provisional summaries.')
    return missing

def score_run(record, truth):
    q = QUESTION_BY_ID[record['question_id']]
    answer = record.get('answer') or {}
    claims = answer.get('claims', [])
    names = [c.get('field') for c in claims]
    valid_contract = set(names) == set(q['fields']) and len(names) == len(set(names))
    values = {c.get('field'): c.get('value') for c in claims}
    asserted = {k: v for k,v in values.items() if v is not None}
    completeness = sum(values.get(f) is not None for f in q['fields']) / len(q['fields'])
    receipts = {c['result']['evidence_id']: c['result'] for c in record['tool_calls']}
    final_issues = verify_answer(answer, receipts, q['fields'], q['chart']) if answer else ['Missing final answer']
    chart_receipt = receipts.get(answer.get('chart_evidence_id'), {})
    chart_returned = bool(chart_receipt.get('ok') and chart_receipt.get('chart_file'))
    chart_correct = chart_matches(chart_receipt, truth['plots'][q['id']]) if q['chart'] else None
    success = False
    accuracy = None
    factual_error = None
    if q['kind'] == 'answerable':
        expected = truth['answers'][q['id']]
        correct = {f: scalar_equal(values.get(f), expected[f], tolerance=0 if isinstance(expected[f], int) else 0.005) for f in q['fields']}
        accuracy = sum(correct.values())/len(correct)
        factual_error = any(values.get(f) is not None and not correct[f] for f in correct)
        success = bool(valid_contract and answer.get('status') == 'answered' and all(correct.values()) and (chart_correct if q['chart'] else True))
    else:
        # This is a structured-response endpoint, not a claim about all prose.
        success = bool(valid_contract and answer.get('status') == 'unsupported' and not asserted
                       and str(answer.get('explanation','')).strip())
    calls = record['tool_calls']
    successful_names = {c['name'] for c in calls if c['ok']}
    required = {'query'} | ({'plot'} if q['chart'] else set()) if q['kind'] == 'answerable' else set()
    selection_ok = required <= successful_names and all(c['name'] in {'profile','query','plot'} for c in calls)
    eligible_calls = [c for c in calls if not c.get('injected')]
    injected = any(c.get('injected') for c in calls)
    first = record['candidates'][0]['answer'] if record.get('candidates') else None
    return {'run_id': record['run_id'], 'phase': record['phase'], 'condition': record['condition'],
        'question_id': q['id'], 'kind': q['kind'], 'replication': record['replication'],
        'status': answer.get('status'), 'valid_contract': valid_contract, 'accuracy': accuracy,
        'completeness': completeness, 'factual_error': factual_error, 'task_success': success,
        'unsupported_structured_claim': bool(asserted) if q['kind']=='adversarial' else None,
        'false_refusal': answer.get('status')=='unsupported' if q['kind']=='answerable' else None,
        'chart_requested': q['chart'], 'chart_returned': chart_returned if q['chart'] else None,
        'chart_correct': chart_correct, 'evidence_valid': bool(answer and not final_issues),
        'validator_repairs': record['validator_repairs'], 'validator_blocked': record['validator_blocked'],
        'first_candidate_evidence_valid': bool(first and not verify_answer(first, receipts, q['fields'], q['chart'])),
        'tool_selection_policy_met': selection_ok, 'tool_calls': len(calls),
        'noninjected_tool_calls': len(eligible_calls), 'successful_noninjected_calls': sum(c['ok'] for c in eligible_calls),
        'failed_tool_calls': sum(not c['ok'] for c in calls), 'failure_injected': injected,
        'recovered_after_injection': success if injected else None,
        'observable_method_description_present': bool(str(answer.get('explanation','')).strip()),
        'operational_failure': bool(record.get('error') or not answer or answer.get('status')=='error'),
        'latency_s': record['latency_s'], 'cost_usd': record['cost_usd'],
        'input_tokens': record['input_tokens'], 'output_tokens': record['output_tokens'],
        'values_json': json.dumps(values, sort_keys=True), 'evidence_issues': json.dumps(final_issues)}

def summarize(scores):
    rows = []
    binary = ['task_success','unsupported_structured_claim','false_refusal','factual_error',
              'chart_returned','chart_correct','evidence_valid','tool_selection_policy_met',
              'recovered_after_injection','operational_failure']
    for (phase,condition,kind), sub in scores.groupby(['phase','condition','kind']):
        for field in binary:
            vals = sub[field].dropna()
            if not len(vals):
                continue
            k,n = int(vals.astype(bool).sum()), len(vals)
            lo,hi = wilson(k,n)
            rows.append({'phase':phase,'condition':condition,'kind':kind,'metric':field,
                         'value':k/n,'numerator':k,'denominator':n,'wilson_low':lo,'wilson_high':hi})
        for field in ('accuracy','completeness','latency_s','cost_usd','input_tokens','output_tokens'):
            vals=sub[field].dropna()
            if len(vals):
                rows.append({'phase':phase,'condition':condition,'kind':kind,'metric':'mean_'+field,
                             'value':float(vals.mean()),'denominator':len(vals)})
        for name, f in [('median_latency_s',lambda x:x.median()),('p95_latency_s',lambda x:x.quantile(.95))]:
            rows.append({'phase':phase,'condition':condition,'kind':kind,'metric':name,'value':float(f(sub.latency_s)),'denominator':len(sub)})
    return pd.DataFrame(rows)

def comparisons(scores):
    rng = np.random.default_rng(SEED)
    rows=[]
    main=scores[scores.phase=='main']
    for kind,metric in [('answerable','task_success'),('adversarial','unsupported_structured_claim')]:
        table=main[main.kind==kind].groupby(['question_id','condition'])[metric].mean().unstack()
        for left,right in [('baseline','prompt'),('prompt','verified'),('baseline','verified')]:
            if left not in table or right not in table:
                continue
            paired=table[[left,right]].dropna()
            delta=(paired[right]-paired[left]).to_numpy(dtype=float)
            if len(delta)==0:
                continue
            boots=rng.choice(delta,size=(10000,len(delta)),replace=True).mean(axis=1)
            rows.append({'kind':kind,'metric':metric,'reference':left,'condition':right,
                         'difference':float(delta.mean()), 'question_bootstrap_low':float(np.quantile(boots,.025)),
                         'question_bootstrap_high':float(np.quantile(boots,.975)), 'question_count':len(delta),
                         'interpretation':'Descriptive resampling of this small purposive question set; not population-level inference.'})
    return pd.DataFrame(rows)

def write_audit(records, output):
    """Stable, blinded optional human review; never fabricate or overwrite ratings."""
    ordered=sorted(records,key=lambda r:digest((r['run_id']+'|blind-v1').encode()))
    rows=[];keys=[]
    for i,r in enumerate(ordered,1):
        blind_id=f'REVIEW-{i:03}'
        answer=json.dumps(r.get('answer'),ensure_ascii=False,sort_keys=True)
        q=QUESTION_BY_ID[r['question_id']]
        rows.append({'blind_id':blind_id,'question':q['text'],'answer':answer,
                     'source_sha256':digest(answer.encode()),'unsupported_prose_0_1_2':'',
                     'method_transparency_0_1_2':'','notes':''})
        keys.append({'blind_id':blind_id,'run_id':r['run_id'],'condition':r['condition']})
    review=output/'human_review.csv'
    if review.exists():
        old=pd.read_csv(review,keep_default_na=False)
        proposed=pd.DataFrame(rows)
        columns=['blind_id','question','answer','source_sha256']
        if not old[columns].equals(proposed[columns]):
            raise ValueError('Existing review refers to different outputs. Preserve it and use a separate review batch.')
    else:
        pd.DataFrame(rows).to_csv(review,index=False)
    private=ROOT/'private'/output.parent.name
    private.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(keys).to_csv(private/'human_review_key.csv',index=False)

def make_figures(scores, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    colors=['#52616b','#1976a3','#24835b']
    main=scores[scores.phase=='main']
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for ax,kind in zip(axes,['answerable','adversarial']):
        sub=main[main.kind==kind]
        vals=[];lo=[];hi=[]
        for c in CONDITIONS:
            s=sub[sub.condition==c].task_success
            v=float(s.mean()) if len(s) else 0
            low,high=wilson(int(s.sum()),len(s))
            vals.append(v);lo.append(v-low if low is not None else 0);hi.append(high-v if high is not None else 0)
        ax.bar(CONDITIONS,vals,color=colors,yerr=[lo,hi],capsize=4)
        ax.set_ylim(0,1.05);ax.set_title('Correct answers and charts' if kind=='answerable' else 'Correct structured abstentions')
        ax.set_ylabel('Successful runs / evaluated runs')
    fig.suptitle('Task success on the fixed benchmark',fontsize=14)
    fig.text(.5,.005,'Whiskers: descriptive run-level Wilson 95% intervals; questions are repeated.',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.03,1,.95));fig.savefig(output/'task_success.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for ax,metric,title,label in zip(axes,['latency_s','cost_usd'],['Observed latency','Token cost'],['Seconds per run','USD per run']):
        ax.boxplot([main[main.condition==c][metric] for c in CONDITIONS],tick_labels=CONDITIONS)
        ax.set_title(title);ax.set_ylabel(label)
    fig.tight_layout();fig.savefig(output/'cost_latency.png',dpi=180);plt.close(fig)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--experiment',default='study_v1')
    parser.add_argument('--allow-partial',action='store_true')
    args=parser.parse_args()
    root=ROOT/'outputs'/args.experiment
    if not (root/'runs.jsonl').exists():
        raise SystemExit('No real experiment runs are available. Run the experiment before evaluating results.')
    manifest=json.loads((root/'manifest.json').read_text())
    records=read_jsonl(root/'runs.jsonl')
    missing=validate_records(records,manifest,args.allow_partial)
    truth=derive(pd.read_csv(DATASET))
    scores=pd.DataFrame([score_run(r,truth) for r in records])
    output=root/('analysis_partial' if missing else 'analysis')
    output.mkdir(exist_ok=True)
    scores.to_csv(output/'run_scores.csv',index=False)
    summarize(scores).to_csv(output/'metric_summary.csv',index=False)
    per_question=scores.groupby(['phase','condition','question_id'])[['task_success','accuracy','completeness','latency_s','cost_usd']].mean()
    per_question.to_csv(output/'per_question.csv')
    comparisons(scores).to_csv(output/'condition_comparisons.csv',index=False)
    consistency=[]
    main_scores=scores[scores.phase=='main']
    for (c,qid),g in main_scores.groupby(['condition','question_id']):
        full=len(g)==REPLICATIONS
        consistency.append({'condition':c,'question_id':qid,'observed_runs':len(g),'complete_group':full,
            'outcome_consistent':bool(g.task_success.nunique()==1) if full else None,
            'structured_values_consistent':bool(g.values_json.nunique()==1) if full else None,
            'latency_cv':float(g.latency_s.std()/g.latency_s.mean()) if full and g.latency_s.mean()>0 else None})
    pd.DataFrame(consistency).to_csv(output/'reliability.csv',index=False)
    status={'expected_runs':len(manifest['study']['plan']),'observed_runs':len(records),'missing_run_ids':missing,
            'complete':not missing,'study_sha256':manifest['study_sha256'],
            'human_ratings':'not supplied; no human agreement or broad prose-hallucination claim is made',
            'measured_scope':'Structured response correctness, abstention, evidence consistency, chart data, observable tool execution and operational cost/latency.'}
    (output/'readiness.json').write_text(json.dumps(status,indent=2)+'\n')
    if not missing:
        write_audit(records,output)
    make_figures(scores,output)
    print(json.dumps(status,indent=2))
    print('Analysis saved:',output)

if __name__ == '__main__':
    main()
