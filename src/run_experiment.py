"""Run a frozen, interleaved experiment with an append-only API cost ledger.

No generic OPENAI_API_KEY, credential store, browser profile, or work account is
read. Only the dedicated personal key file created by configure_personal_key.py
or THESIS_OPENAI_API_KEY is accepted. No API call occurs on import.
"""
from __future__ import annotations
import argparse
import datetime as dt
import fcntl
import json
import os
import random
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

import pandas as pd
from study import (ROOT, DATASET, CONDITIONS, QUESTIONS, QUESTION_BY_ID, MODEL,
    TEMPERATURE, SEED, REPLICATIONS, MAX_TURNS, MAX_OUTPUT_TOKENS, INPUT_PRICE,
    CACHED_INPUT_PRICE, OUTPUT_PRICE, SPEND_LIMIT_USD, BASELINE_PROMPT,
    IMPROVED_PROMPT, FINAL_SCHEMA, TOOLS, DataTools, digest, verify_answer)

def utcnow():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def append_json(path, item):
    with Path(path).open('a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False, allow_nan=False) + '\n')
        f.flush(); os.fsync(f.fileno())

def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()] if Path(path).exists() else []

class BudgetExceeded(RuntimeError):
    pass

class APIError(RuntimeError):
    pass

class Client:
    def __init__(self, key, ledger, limit=SPEND_LIMIT_USD):
        self.key = key
        self.ledger = Path(ledger)
        self.limit = min(float(limit), SPEND_LIMIT_USD)

    def liability(self):
        entries = {}
        for row in read_jsonl(self.ledger):
            entries[row['request_id']] = row['usd']
        return sum(entries.values())

    @staticmethod
    def maximum_cost(payload):
        # For text-only UTF-8, byte count is a deliberately conservative token
        # bound. Extra reserve covers function/schema/chat framing. Output is
        # explicitly capped. Uncertain requests retain this entire reservation.
        input_bound = len(json.dumps(payload, ensure_ascii=False).encode('utf-8')) + 8192
        return input_bound * INPUT_PRICE + payload['max_output_tokens'] * OUTPUT_PRICE

    def create(self, payload, run_id):
        reserve = self.maximum_cost(payload)
        if self.liability() + reserve > self.limit:
            raise BudgetExceeded('Next request would exceed the experiment spending ceiling.')
        request_id = str(uuid.uuid4())
        append_json(self.ledger, {'request_id': request_id, 'run_id': run_id, 'event': 'reserved', 'usd': reserve, 'timestamp': utcnow()})
        req = urllib.request.Request('https://api.openai.com/v1/responses',
            data=json.dumps(payload).encode(), method='POST',
            headers={'Authorization': f'Bearer {self.key}', 'Content-Type': 'application/json',
                     'X-Client-Request-Id': request_id})
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.load(response)
        except urllib.error.HTTPError as exc:
            # Never log request headers, credentials, or a raw server body that
            # could echo credentials. Keep reservation on every uncertain call.
            try:
                detail = json.loads(exc.read()).get('error', {})
                code = detail.get('code') or detail.get('type') or 'unknown'
            except Exception:
                code = 'unknown'
            raise APIError(f'OpenAI HTTP {exc.code}; error code {code}. No automatic retry; cost reservation retained.') from None
        except (urllib.error.URLError, TimeoutError) as exc:
            raise APIError(f'OpenAI network failure ({type(exc).__name__}). No automatic retry; cost reservation retained.') from None
        usage = result.get('usage') or {}
        if not all(k in usage for k in ('input_tokens', 'output_tokens')):
            raise APIError('API response omitted usage; reserved cost retained and experiment stopped.')
        inp, out = usage['input_tokens'], usage['output_tokens']
        cached = (usage.get('input_tokens_details') or {}).get('cached_tokens', 0)
        if not (0 <= cached <= inp and inp >= 0 and out >= 0):
            raise APIError('Invalid usage record; reserved cost retained.')
        actual = (inp-cached)*INPUT_PRICE + cached*CACHED_INPUT_PRICE + out*OUTPUT_PRICE
        append_json(self.ledger, {'request_id': request_id, 'run_id': run_id, 'response_id': result.get('id'),
            'event': 'settled', 'usd': actual, 'reserved_usd': reserve, 'usage': usage, 'timestamp': utcnow()})
        if actual > reserve:
            raise APIError('Token usage exceeded conservative reservation. Stop and audit budget assumptions.')
        return result, actual

def planned_runs():
    rng = random.Random(SEED)
    main = []
    blocks = [(q['id'], rep) for q in QUESTIONS for rep in range(1, REPLICATIONS+1)]
    rng.shuffle(blocks)
    for qid, rep in blocks:
        conditions = list(CONDITIONS); rng.shuffle(conditions)
        for condition in conditions:
            main.append({'run_id': f'main_{condition}_{qid}_r{rep}', 'phase': 'main',
                         'condition': condition, 'question_id': qid, 'replication': rep, 'inject_failure': False})
    recovery = []
    blocks = [(q, rep) for q in ('Q02_top_games', 'Q05_filtered') for rep in range(1, 4)]
    rng.shuffle(blocks)
    for qid, rep in blocks:
        conditions = list(CONDITIONS); rng.shuffle(conditions)
        for condition in conditions:
            recovery.append({'run_id': f'recovery_{condition}_{qid}_r{rep}', 'phase': 'recovery',
                             'condition': condition, 'question_id': qid, 'replication': rep, 'inject_failure': True})
    return main + recovery

def study_manifest():
    source = {p.name: digest(p.read_bytes()) for p in sorted((ROOT/'src').glob('*.py'))}
    return {'model': MODEL, 'temperature': TEMPERATURE, 'seed': SEED, 'replications': REPLICATIONS,
        'max_turns': MAX_TURNS, 'max_output_tokens_per_call': MAX_OUTPUT_TOKENS,
        'dataset_sha256': digest(DATASET.read_bytes()), 'questions': QUESTIONS,
        'prompts': {'baseline': BASELINE_PROMPT, 'prompt': IMPROVED_PROMPT, 'verified': IMPROVED_PROMPT},
        'tools': TOOLS, 'final_schema': FINAL_SCHEMA, 'plan': planned_runs(), 'source_hashes': source, 'protocol_sha256': digest((ROOT/'PROTOCOL.md').read_bytes()),
        'prices_per_million_tokens': {'input': INPUT_PRICE*1e6, 'cached_input': CACHED_INPUT_PRICE*1e6, 'output': OUTPUT_PRICE*1e6},
        'spend_limit_usd': SPEND_LIMIT_USD}

def freeze(path):
    manifest = study_manifest()
    path = Path(path)
    if path.exists():
        old = json.loads(path.read_text())
        if old['study_sha256'] != digest(manifest):
            raise ValueError('Study inputs/code changed since freeze. Use a new experiment directory; do not combine versions.')
        return old
    result = {'frozen_at': utcnow(), 'study_sha256': digest(manifest), 'study': manifest}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    return result

def run_one(plan, client, frame, run_dir):
    question = QUESTION_BY_ID[plan['question_id']]
    tools = DataTools(frame, run_dir/'charts', inject_failure=plan['inject_failure'])
    instructions = BASELINE_PROMPT if plan['condition'] == 'baseline' else IMPROVED_PROMPT
    conversation = [{'role': 'user', 'content': question['text']}]
    started, stamp = time.perf_counter(), utcnow()
    trace, usage_rows, costs, candidates = [], [], [], []
    final = None
    raw_final = None
    error = None
    repairs = 0
    blocked = False
    fatal = None
    for turn in range(MAX_TURNS):
        payload = {'model': MODEL, 'instructions': instructions, 'input': conversation,
                   'tools': TOOLS, 'parallel_tool_calls': False, 'temperature': TEMPERATURE,
                   'max_output_tokens': MAX_OUTPUT_TOKENS, 'store': False,
                   'text': {'format': {'type': 'json_schema', 'name': 'analysis_answer', 'strict': True, 'schema': FINAL_SCHEMA}}}
        try:
            result, cost = client.create(payload, plan['run_id'])
        except (BudgetExceeded, APIError) as exc:
            error, fatal = str(exc), exc
            break
        costs.append(cost); usage_rows.append(result['usage'])
        trace.append({'turn': turn+1, 'response_id': result.get('id'), 'status': result.get('status'),
                      'output': result.get('output', []), 'usage': result['usage'], 'cost_usd': cost})
        # Preserve all function/output items as required by the Responses API.
        conversation.extend(result.get('output', []))
        if result.get('status') != 'completed':
            error = f"Response ended with status {result.get('status')}"
            break
        calls = [x for x in result.get('output', []) if x.get('type') == 'function_call']
        if calls:
            for call in calls:
                try:
                    args = json.loads(call['arguments'])
                    receipt = tools.call(call['name'], args)
                except (KeyError, json.JSONDecodeError) as exc:
                    receipt = tools.call('invalid_function_payload', {'error': type(exc).__name__})
                conversation.append({'type': 'function_call_output', 'call_id': call['call_id'],
                                     'output': json.dumps(receipt, ensure_ascii=False)})
            continue
        texts = [c['text'] for item in result.get('output', []) if item.get('type') == 'message'
                 for c in item.get('content', []) if c.get('type') == 'output_text']
        raw_final = '\n'.join(texts)
        try:
            candidate = json.loads(raw_final)
            import jsonschema
            jsonschema.validate(candidate, FINAL_SCHEMA)
        except Exception as exc:
            error = f'Final response was not valid structured output: {type(exc).__name__}'
            break
        issues = verify_answer(candidate, tools.receipts, question['fields'], question['chart'])
        candidates.append({'answer': candidate, 'issues': issues, 'turn': turn+1})
        if plan['condition'] == 'verified' and issues:
            if repairs == 0 and turn+1 < MAX_TURNS:
                repairs += 1
                conversation.append({'role': 'user', 'content': 'The evidence validator found these issues: '+json.dumps(issues)+
                    '. You may make one correction attempt using the existing tools and data. No correct answer is supplied. Revise the answer, or state that you cannot support it.'})
                continue
            blocked = True
            final = {'status': 'error', 'claims': [{'field': f, 'value': None, 'evidence_id': None, 'pointer': None} for f in question['fields']],
                     'chart_evidence_id': None, 'explanation': 'The evidence validator withheld an answer that did not pass its checks.'}
        else:
            final = candidate
        break
    else:
        error = 'Maximum API-turn budget reached without a final answer'
    record = {**plan, 'timestamp': stamp, 'finished_at': utcnow(), 'model': MODEL, 'temperature': TEMPERATURE,
              'system_prompt_sha256': digest(instructions.encode()), 'dataset_sha256': digest(DATASET.read_bytes()),
              'answer': final, 'raw_final_text': raw_final, 'candidates': candidates, 'validator_repairs': repairs,
              'validator_blocked': blocked, 'tool_calls': tools.calls, 'trace': trace, 'error': error,
              'failure_injected': tools.failure_injected, 'latency_s': time.perf_counter()-started,
              'input_tokens': sum(x['input_tokens'] for x in usage_rows),
              'cached_input_tokens': sum((x.get('input_tokens_details') or {}).get('cached_tokens', 0) for x in usage_rows),
              'output_tokens': sum(x['output_tokens'] for x in usage_rows), 'cost_usd': sum(costs), 'api_calls': len(trace)}
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir/'record.json').write_text(json.dumps(record, indent=2, ensure_ascii=False, allow_nan=False)+'\n')
    return record, fatal

def personal_key():
    key = os.environ.get('THESIS_OPENAI_API_KEY', '').strip()
    path = ROOT/'.secrets'/'openai_api_key'
    if not key and path.exists():
        key = path.read_text().strip()
    if not key:
        raise SystemExit('No dedicated personal key configured. Run configure_personal_key.py; no API calls made.')
    return key

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze-only', action='store_true')
    parser.add_argument('--limit', type=int, default=None, help='Maximum NEW scheduled runs this invocation; resumes existing frozen plan')
    parser.add_argument('--experiment', default='study_v1')
    args = parser.parse_args()
    if not args.experiment.replace('_','').replace('-','').isalnum():
        raise SystemExit('Use a simple experiment directory name')
    if args.limit is not None and args.limit < 1:
        raise SystemExit('--limit must be positive')
    output = ROOT/'outputs'/args.experiment
    output.mkdir(parents=True, exist_ok=True)
    # One process across all experiments protects the shared $10 ledger.
    with (ROOT/'outputs'/'.experiment.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('Another thesis experiment is already running')
        manifest = freeze(output/'manifest.json')
        print(f"Frozen study: {manifest['study_sha256']}; scheduled runs: {len(manifest['study']['plan'])}", flush=True)
        if args.freeze_only:
            return
        client = Client(personal_key(), ROOT/'outputs'/'api_cost_ledger.jsonl')
        frame = pd.read_csv(DATASET)
        completed = {r['run_id'] for r in read_jsonl(output/'runs.jsonl')}
        count = 0
        for plan in manifest['study']['plan']:
            if plan['run_id'] in completed:
                continue
            run_dir = output/'runs'/plan['run_id']
            # Reconcile a completed record if interrupted before aggregate append.
            if (run_dir/'record.json').exists():
                record = json.loads((run_dir/'record.json').read_text())
                append_json(output/'runs.jsonl', record)
                completed.add(plan['run_id'])
                continue
            record, fatal = run_one(plan, client, frame, run_dir)
            append_json(output/'runs.jsonl', record)
            count += 1
            print(json.dumps({'run_id': plan['run_id'], 'status': (record['answer'] or {}).get('status'),
                'error': record['error'], 'calls': record['api_calls'], 'cost_usd': round(record['cost_usd'], 6),
                'cumulative_reserved_or_settled_usd': round(client.liability(), 6)}), flush=True)
            if fatal:
                raise SystemExit(str(fatal))
            if args.limit is not None and count >= args.limit:
                break

if __name__ == '__main__':
    main()
