"""Build and execute the offline dissertation notebook. No API calls or key reads."""

from pathlib import Path
import os, json, sys
import nbformat as nbf
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
N = ROOT / "notebooks"
N.mkdir(exist_ok=True)
B = ROOT / ".build"
(B / "kernels/thesis-study").mkdir(parents=True, exist_ok=True)
(B / "kernels/thesis-study/kernel.json").write_text(
    json.dumps(
        {
            "argv": [
                sys.executable,
                "-m",
                "ipykernel_launcher",
                "-f",
                "{connection_file}",
            ],
            "display_name": "Thesis study",
            "language": "python",
        }
    )
)
os.environ["JUPYTER_PATH"] = str(B) + os.pathsep + os.environ.get("JUPYTER_PATH", "")
os.environ.setdefault("MPLCONFIGDIR", str(B / "matplotlib"))
nb = nbf.v4.new_notebook()
cells = []


def md(t):
    cells.append(nbf.v4.new_markdown_cell(t))


def code(t):
    cells.append(nbf.v4.new_code_cell(t))


md("""# Evidence validation and recovery in data analysis agents

Kushal Krishnamurthy · M598 dissertation project

This notebook reproduces the **198 collected runs** without making API calls. It checks coverage and provenance, recomputes the primary evaluation and presents the post-collection sensitivity analysis. The study compares baseline, improved prompt and improved prompt plus a runtime evidence validator. No weights were fine-tuned.

The main conclusion is bounded: all conditions solved the answerable tasks; clearer instructions improved structured abstention; **no validator repair was triggered**, so its incremental effectiveness remains unestablished. The strict baseline refusal score is sensitive to missing response fields.
""")
code("""from pathlib import Path
import sys, json, subprocess
import pandas as pd
from IPython.display import display, Image
ROOT = Path.cwd()
if not (ROOT / 'src').is_dir():
    ROOT = ROOT.parent
assert (ROOT / 'src/study.py').is_file(), 'Open from the project or notebooks directory'
sys.path.insert(0, str(ROOT / 'src'))
from study import DATASET, digest
from run_experiment import read_jsonl
from evaluate import validate_records, score_run
from ground_truth import derive
OUT = ROOT / 'outputs/study_v1'
manifest = json.loads((OUT / 'manifest.json').read_text())
records = read_jsonl(OUT / 'runs.jsonl')
missing = validate_records(records, manifest)
assert not missing and len(records) == 198
print(f'Complete coverage: {len(records)}/198 runs')
print('Dataset SHA-256:', digest(DATASET.read_bytes()))
print('Frozen study SHA-256:', manifest['study_sha256'])""")
md("""## Data and independent answers

The historical CSV has game-platform rows and sales in millions of units. Year is release year. No global cleaning changes the experiment data. The source licence is unresolved; the public package contains the retrieval script and checksum rather than the CSV. The source card and frozen prompt describe a sales threshold that conflicts with the CSV: 5,781 rows record below 0.10 million global sales. Review version 2 flags all fifteen explanations repeating this premise; correct population refusals and primary scores remain unchanged. The original annotations and amendment are retained.
""")
code(
    """frame = pd.read_csv(DATASET)
print('Shape:', frame.shape)
display(frame.isna().sum().rename('missing_rows').to_frame())
truth = derive(frame)
display(pd.DataFrame([{'question_id': q, 'expected_fields': json.dumps(v)} for q, v in truth['answers'].items()]))"""
)
md("""## Recompute the frozen primary scoring rules

The plotting-only correction after collection is documented in `documentation/ANALYSIS_AMENDMENTS.md`. It does not change a score or interval. The original evaluator remains archived and hash-verifiable.
""")
code(
    """subprocess.run([sys.executable, str(ROOT / 'src/evaluate.py')], cwd=ROOT, check=True, capture_output=True, text=True)
subprocess.run([sys.executable, str(ROOT / 'scripts/supplementary_analysis.py')], cwd=ROOT, check=True, capture_output=True, text=True)
subprocess.run([sys.executable, str(ROOT / 'scripts/trace_review_analysis.py')], cwd=ROOT, check=True, capture_output=True, text=True)
subprocess.run([sys.executable, str(ROOT / 'scripts/verify_evidence.py')], cwd=ROOT, check=True, capture_output=True, text=True)
scores = pd.DataFrame([score_run(r, truth) for r in records])
assert len(scores) == 198 and scores.run_id.nunique() == 198
main = scores[scores.phase == 'main']
display(main.groupby(['condition', 'kind']).task_success.agg(['sum','count','mean']))"""
)
code("display(Image(filename=str(OUT / 'analysis/task_success.png')))")
md("""## Response format sensitivity

The frozen protocol required every requested field, including explicit nulls on unsupported tasks. Fifteen baseline responses declined the task but omitted those fields. The **post hoc relaxed rule** retains unsupported status, no asserted values and a nonempty explanation while allowing omitted fields. Numeric-claim sensitivity additionally separates the string `"null"` from an actual numeric assertion. These checks supplement, rather than replace, the frozen primary results.
""")
code(
    "display(pd.read_csv(OUT / 'analysis/posthoc_sensitivity.csv'))\ndisplay(Image(filename=str(OUT / 'analysis/abstention_sensitivity.png')))"
)
md("""## Question-level outcomes and uncertainty

The six questions within each type are purposive and repeated five times. Run-level Wilson intervals are descriptive. Paired bootstrap intervals resample question-level differences, with only six questions per type. Neither supports broad population claims.
""")
code(
    "display(main.groupby(['question_id','condition']).task_success.mean().unstack())\ndisplay(pd.read_csv(OUT / 'analysis/condition_comparisons.csv').drop(columns='interpretation'))"
)
md("""## Mechanism and recovery

No actual verified run required repair or blocking. Eight deterministic challenge checks test the validator implementation separately. They are **not additional model experiments**. One real semantically wrong answer is intentionally accepted by the limited evidence checker.
""")
code(
    """display(scores.groupby(['phase','condition'])[['validator_repairs','validator_blocked']].sum())
display(scores[scores.phase == 'recovery'].groupby('condition')[['failure_injected','task_success']].sum())
challenges = json.loads((OUT / 'analysis/validator_challenges.json').read_text())
display(pd.DataFrame(challenges['cases']))"""
)
md("""## Inspect a real failure

This verified response supplies the release-cohort total in a field requesting transaction-year sales. Its explanation acknowledges the limitation, but the structured value remains inappropriate. Evidence consistency therefore does not establish semantic correctness.
""")
code(
    """example = next(r for r in records if r['run_id'] == 'main_verified_A05_transaction_year_r5')
print(json.dumps(example['answer'], indent=2))
display(pd.DataFrame([{'tool': c['name'], 'ok': c['ok'], 'receipt': c['result']['evidence_id'], 'arguments': json.dumps(c['arguments'])} for c in example['tool_calls']]))"""
)
md("""## Recorded cost and timing

Costs use returned token counts and the documented prices. They are estimates, not an invoice reconciliation. The ledger total includes the smoke check. Latency includes remote waiting and local execution on one machine.
""")
code("""audit = json.loads((OUT / 'analysis/audit_summary.json').read_text())
print('Experiment cost USD:', round(audit['experiment_cost_usd'], 6))
print('Including smoke check USD:', round(audit['cost_including_smoke_usd'], 6))
print('Unsettled reservations:', audit['unsettled_reservations'])
display(pd.DataFrame(audit['condition_totals']).T)
display(Image(filename=str(OUT / 'analysis/cost_latency.png')))""")
md("""## Supplementary semantic review

The **post hoc, unblinded AI-assisted review** covers all 198 final explanations and 385 calls. It scores observable task interpretation, method/evidence and explanation/output alignment on three 0–2 items, plus contextual tool selection and parameter correctness. Prose is labelled supported, ambiguous or unsupported. The complete rubric and source-bound annotations accompany the package. These are fixed AI judgements, not independent human ratings. This notebook validates bindings and aggregates them; it does not regenerate the semantic judgements.

Call denominators exclude deliberately injected failures. Profile calls have no analytical parameters. Runs with no calls receive no automatic tool score. Unsupported prose incidence counts responses, not individual claims. The ambiguity sensitivity matters because its ordering differs from the narrower unsupported category.
""")
code("""review = pd.read_csv(OUT / 'analysis/posthoc_review_summary.csv')
g = review[(review.phase == 'main') & (review.kind == 'all')].set_index('condition')
display(g[['runs','prose_unsupported_n','prose_ambiguous_n','prose_flagged_n','reasoning_mean_0_6']].T)
display(g[['selection_correct_calls','selection_eligible_calls','parameter_correct_calls','parameter_eligible_calls','runs_without_eligible_calls']].T)
receipt = json.loads((OUT / 'analysis/posthoc_review_receipt.json').read_text())
print('Completed response annotations:', receipt['reviewed_runs'])
print('Completed call annotations:', receipt['reviewed_calls'])
print('Independent human raters:', receipt['independent_raters'])""")
md("""## Explicit variance within repeated questions

Sample variance uses n−1 within each five-run main-study question/condition group. Zero variance can represent stable incorrect answers. Numeric-value dispersion is conditional on finite assertions, with null/nonnumeric counts retained; one finite value has undefined variance. The full files also contain within-question latency and cost standard deviation and coefficient of variation. Do not pool unlike quantities or treat null abstentions as zero.
""")
code(
    """variance = pd.read_csv(OUT / 'analysis/posthoc_variance.csv')
display(variance[variance.question_id == 'A05_transaction_year'][['condition','runs','successes','success_sample_variance']].set_index('condition'))
numeric_variance = pd.read_csv(OUT / 'analysis/posthoc_numeric_variance.csv')
display(numeric_variance[numeric_variance.question_id == 'A05_transaction_year'][['condition','total_runs','null_or_missing','nonnumeric','n','mean','sample_variance']].set_index('condition'))
print('Nonzero binary-variance groups:', int((variance.success_sample_variance > 0).sum()), 'of', len(variance))
display(variance[variance.question_id == 'A05_transaction_year'][['condition','latency_s_mean','latency_s_sample_sd','latency_s_cv','cost_usd_mean','cost_usd_sample_sd','cost_usd_cv']].set_index('condition').T)"""
)
md("""## Independent verification of the recorded evidence

The independent script derives expected values with the standard CSV reader and decimal arithmetic, without importing the project evaluator. It checks all 198 strict task outcomes, saved response/ledger correspondence, configuration hashes and referenced chart files. This establishes local consistency, not provider authenticity or invoice reconciliation. The dataset must be supplied separately at its recorded checksum.
""")
code(
    """verification = json.loads((ROOT / '.build/evidence_verification/independent_audit.json').read_text())
display(pd.Series({k:verification[k] for k in ['runs','unique_response_ids','tool_calls','saved_chart_files','all_198_task_scores_match_independent_recomputation']}, name='verified'))"""
)
md("""## Interpretation and reproducibility boundary

The answerable benchmark reached a ceiling. Improved instructions reduced unsupported numeric outputs on this set, but the categories are represented explicitly in those instructions. The validator did not activate, and its remaining semantic error passed the intended narrow checks. All conditions recovered from the simple injected error. Future work should test unseen tasks and isolate repair opportunities before making effectiveness claims.

Raw records, the manifest, prompts, scoring source, package versions and the complete protocol accompany this notebook. The new semantic/prose review is exploratory and has no independent human adjudication. Its fixed labels and rationales are separate from the optional blank human-review form. No inter-rater reliability or population-wide hallucination claim is made. A fresh API rerun costs money and requires a new experiment name; this notebook performs offline reproduction only.
""")
nb.cells = cells
nb.metadata = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "thesis-study",
    },
    "language_info": {"name": "python", "version": sys.version.split()[0]},
}
NotebookClient(
    nb,
    timeout=120,
    kernel_name="thesis-study",
    resources={"metadata": {"path": str(ROOT)}},
).execute()
nb.metadata.kernelspec.name = "python3"
nbf.write(nb, N / "Thesis_Experiment_Reproduction.ipynb")
try:
    from nbconvert import HTMLExporter

    body, _ = HTMLExporter().from_notebook_node(nb)
    (N / "Thesis_Experiment_Reproduction.html").write_text(body)
    print("Executed notebook and HTML exported.")
except ImportError:
    print("Executed notebook exported; nbconvert is unavailable.")
assert all(
    not any(o.get("output_type") == "error" for o in c.get("outputs", []))
    for c in nb.cells
)
print("Executed code cells:", sum(c.cell_type == "code" for c in nb.cells))
