# Analysis amendment after collection

## Original plotting correction on 22 September 2026

The complete 198-run experiment finished before this amendment. The first offline evaluation wrote all score tables, then plotting stopped because floating-point roundoff made a zero-length error bar negative at a boundary proportion. The plotting distances in `src/evaluate.py` are now clamped to zero. No scoring definition, score value, interval formula, prompt, runtime mechanism or raw record changed. The frozen evaluator is preserved in `documentation/frozen_source/evaluate.py` and its hash matches the original manifest. The current evaluator therefore intentionally differs from the pre-run source hash. No further calls are added to the completed study_v1 directory; a fresh online experiment requires a new experiment name and manifest.

## Supplementary trace review on 23 September 2026

Submission feedback identified incomplete alignment with the requested reasoning, semantic tool-selection, parameter, prose-hallucination and variance measures. A separate post hoc review now covers every final explanation and all 385 calls from the existing 198 records. The rubric and completed AI-assisted annotations are supplied separately, with source hashes, per-run/item scores, call-level judgements, excerpts and rationales. It was an unblinded review by Codex after exposure to the results, not an independent human assessment. No human agreement statistic is claimed.

`scripts/trace_review_analysis.py` validates annotation coverage and source bindings, then writes files prefixed `posthoc_review` and `posthoc_*variance`. It does not alter the original scoring files. Numerical dispersion retains missing, nonnumeric and finite-value counts, uses within-question groups and leaves sample variance undefined below two observations. Reasoning and semantic ratings are exploratory judgements, with ambiguity sensitivity and explicit limitations. The aggregation can be reproduced from those fixed judgements; reproduction does not independently confirm their validity.

`scripts/verify_evidence.py` adds an independent CSV/Decimal calculation of every primary task outcome and reconciles saved traces with the local ledger. This confirms local consistency, not provider authenticity or invoice reconciliation. No additional API calls were collected and no raw record, runtime, prompt, answer key, study manifest or primary protocol was changed.

The manuscript adds metric definitions, denominators, new results, variance, a rubric appendix, numbered table captions and a two-level linked contents. The architecture generator labels bypass, pass, correction and blocking routes. The notebook, viva and submission instructions now reflect the supplementary review. These presentation and supplementary-analysis changes do not establish validator effectiveness: no original verified run activated repair or blocking.
