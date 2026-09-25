# Evidence validation and recovery in data analysis agents

M598 research project for Kushal Krishnamurthy. This repository contains a **198-run experiment**, its source code, recorded evidence and independent evaluation. No model weights were fine-tuned. The dissertation, manuscript source and submission documents are not published here.

This is the sharing copy. Supporting scripts and tests have been reformatted;
the frozen experiment code and recorded evidence are unchanged. See
[`documentation/CODE_CLEANUP.md`](documentation/CODE_CLEANUP.md) for the changes
and the distinction between the original and current package manifests.

`documentation/Complete_Experimental_Materials.md` contains the experimental prompts and questions. Historical submission audits describe an earlier private package, not the contents or word count of this public repository. `FILE_MANIFEST.json` inventories this public export; historical manifests remain unchanged for provenance.

## What was built

- A bounded agent with executable dataframe profiling, queries and plotting.
- Evidence receipts connecting final scalar claims to tool outputs.
- A runtime evidence validator with one possible correction opportunity.
- Three experimental conditions, repeated tasks and a separate controlled failure probe.
- Independent numerical and chart-data evaluation, an executed notebook and recorded cost accounting.
- A separately labelled post hoc review of explanatory prose, observable reasoning, semantic tool choices and parameters, with source-bound AI-assisted annotations and explicit repeated-run variance.

## Actual findings

All conditions solved 30/30 answerable tasks and 20/20 requested charts in the main study. Unsupported numeric outputs were 9/30 for baseline, 2/30 for prompt and 1/30 for verified. The frozen strict abstention score penalised omitted null fields; a clearly labelled post hoc relaxed score is 15/30, 28/30 and 29/30. **No validator repair or block occurred**, so the one-run difference between prompt and verified does not establish validator effectiveness. All conditions recovered in 6/6 simple injected-failure trials. A real verified semantic error passed the scalar evidence check.

The experiment used `gpt-4.1-mini-2025-04-14`. Its 583 API calls cost an estimated $0.325128; including the smoke check, the dedicated ledger totals **$0.325364**. No reservations remain unsettled. These are estimates from returned token usage, not invoice reconciliation.

## Offline reproduction

Use Python 3.12 on macOS or Linux. The runner's file lock uses `fcntl`; Windows is not supported by the current runner. From the extracted project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/acquire_data.py
python -m unittest discover -s tests -v
python src/evaluate.py
python scripts/supplementary_analysis.py
python scripts/trace_review_analysis.py
python scripts/verify_evidence.py
```

Only data acquisition accesses the network. Evaluation and tests require no API key and make no model calls. The CSV is excluded from Git and the submission ZIP because the original source reports an unknown licence. Acquisition verifies SHA-256 `e2076095ffcae2a92dbc6de6ecbd54455ee034bb38da550b2dc385e9265d4ebe`; a changed download is rejected rather than silently substituted. The original listing is https://www.kaggle.com/datasets/gregorut/videogamesales . Run the acquisition command above, or place an independently obtained matching CSV at `data/vgsales.csv`.

Open `notebooks/Thesis_Experiment_Reproduction.ipynb` in Jupyter or an editor with notebook support. It includes saved outputs. A self-contained HTML preview is supplied alongside it. Rebuilding and executing the notebook with `python scripts/build_notebook.py` uses the active Python environment and a local Jupyter kernel; no model calls are made. Regenerate the HTML from saved outputs using `python scripts/export_notebook_html.py`; this exporter needs only the Python standard library.

The primary score definitions remain those frozen before collection. `documentation/ANALYSIS_AMENDMENTS.md` records the original plotting correction and the later, separately reported trace assessment. The frozen evaluator is preserved in `documentation/frozen_source/evaluate.py`. Runtime, prompts and ground truth still match their frozen source hashes. The supplementary script retains strict-versus-relaxed sensitivity and eight deterministic implementation challenges. The trace-review script validates and aggregates fixed annotations; it does not create new semantic judgements. The independent verification script recomputes all 198 primary task outcomes without importing the project evaluator.

## File map

| Location | Purpose |
|---|---|
| `PROTOCOL.md` | Frozen pre-run design and outcome definitions |
| `src/study.py` | Dataset tools, prompt definitions, response contract and validator |
| `src/run_experiment.py` | Interleaved collection, saved traces and capped cost ledger |
| `src/ground_truth.py` | Independent expected answers and chart data |
| `src/evaluate.py` | Coverage validation, primary scores, intervals and figures |
| `tests/test_integrity.py` | Twelve offline integrity tests |
| `tests/test_trace_review.py` | Six additional provenance, denominator and variance tests |
| `tests/test_notebook_export.py` | Regression test for read-only notebook export |
| `scripts/supplementary_analysis.py` | Labelled post hoc checks and provenance audit |
| `scripts/trace_review_analysis.py` | Reproducible aggregation of fixed semantic annotations and variance |
| `scripts/verify_evidence.py` | Independent CSV/Decimal outcome verification and local evidence reconciliation |
| `documentation/TRACE_REVIEW_RUBRIC.md` | Complete post hoc rubric and its limitations |
| `config/trace_review_annotations.json` | Completed AI-assisted judgements for 198 responses and 385 calls |
| `documentation/Feedback_Implementation.md` | Implemented review feedback and remaining author checks |
| `documentation/Submission_Verification.json` | Recorded final checks, artifact hashes and independent evidence results |
| `outputs/study_v1/manifest.json` | Frozen model, prompt, schema, dataset and run plan |
| `outputs/study_v1/runs.jsonl` | All 198 real records |
| `outputs/study_v1/runs/` | Per-run records and generated charts |
| `outputs/study_v1/analysis/` | Scores, sensitivities, figures and readiness evidence |
| `notebooks/` | Executed reproduction notebook |
| `documentation/Viva_Preparation.md` | Timed presentation outline and examination questions |

## Fresh online experiment

The completed `study_v1` records are retained unchanged. A fresh experiment requires a **new name** because the offline plotting correction changed the evaluator's source hash after collection.

```bash
python configure_personal_key.py
python src/run_experiment.py --experiment study_replication_01 --freeze-only
python src/run_experiment.py --experiment study_replication_01
python src/evaluate.py --experiment study_replication_01
```

The configuration helper hides input and saves a dedicated personal key under `.secrets/`. The runner accepts only that file or `THESIS_OPENAI_API_KEY`; it never reads a generic OpenAI environment key or another account's credential store. Each additional run incurs charges. A shared ledger protects the configured $10 cumulative ceiling across experiments in this working project. Do not delete the ledger to make room for new spending. An extracted archive contains the recorded ledger so that its remaining allowance is explicit.

The snapshot identifier and schedule do not guarantee identical remote outputs. Use a new protocol and experiment identifier for any change to prompts, tasks or runtime behaviour. Do not mix a new experiment with these results.

## Research boundaries

The task set is small and purposive, and the improved prompt names several of its semantic distinctions. Run-level intervals are descriptive; six question-level observations per type limit bootstrap interpretation. Primary metrics concern structured claims and chart data. Ambiguous prose is reported separately. The runtime validator checks receipt consistency, not full analytical meaning. 


