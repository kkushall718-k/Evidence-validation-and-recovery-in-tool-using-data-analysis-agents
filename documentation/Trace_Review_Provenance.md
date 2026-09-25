# Supplementary assessment provenance

23 September 2026. This disclosure supplements the fixed version-2 rubric and annotations. It does not revise their scores, change the frozen experiment, or claim a newly collected evaluation. The assessment is exploratory, post hoc, unblinded and AI-assisted.

## What the retained evidence establishes

| Question | Recorded evidence and limits |
|---|---|
| Who produced the assessment? | The annotations identify “Codex AI assistant” on 23 September 2026. Condition labels and primary results were visible. |
| Which evaluator model and settings? | The underlying Codex model snapshot, sampling settings and full interactive instruction context were not retained in this project. The experimental agent's `gpt-4.1-mini-2025-04-14` identifier is not evidence of the evaluator's identity. |
| What instructions survive? | The original and amended rubrics, fixed labels, rationales, trace inventory, tool-signature mapping and historical authoring logic survive. These are the available assessment specification; they are not a reconstructed original judge prompt. |
| Were these separate model-judge requests? | No separately configured judge API experiment or 198 independent judge-response logs are recorded. The authoring helper materialises a fixed assessment in one deterministic pass over the run records. Exact interactive presentation batches are unavailable. |
| How were prose labels created? | The original helper contains five explicit unsupported exceptions, thirteen ambiguous exceptions and a supported default for the other 180 records. Its comment reports prior inspection of 198 explanations and 55 distinct argument patterns. The inventory and helper substantiate the workflow, but cannot independently demonstrate the depth of semantic inspection. A default is not proof that the other responses are factually correct. |
| How were reasoning and tool fields created? | Specialised question-family and trace rules populate the fields, using unavailable columns, grouping conflicts, repeated failures, proxy answers and known run exceptions. These rules codify this fixed review; they are not a general semantic parameter validator or a validated reasoning instrument. |
| Did the author or an independent human check labels? | No human ratings, human label-verification record or human inter-rater agreement is documented in the retained project artifacts. User permission for AI assistance is separate from evidence of human verification. |
| What did the later audit change? | A targeted Codex AI audit found that the shared threshold premise conflicts with the CSV. Version 2 corrects fifteen prose labels and removes twenty-seven inaccurate boilerplate rationale sentences. It preserves reasoning and tool scores. This is a correction of one assessment, not a second independently coded rating set. |
| What is reproducible? | Source bindings, fixed annotation records, version differences and numerical aggregation can be checked. That does not independently validate semantic judgements, reconstruct missing model interactions, or authenticate provider-side records. |

## Original and corrected workflow

1. The existing 198 agent records were summarised into an explanation inventory and 55 distinct tool/argument signatures. No new agent observations were collected.
2. Codex-authored exceptions and specialised rules were encoded in the historical version-1 helper. That helper wrote the annotation file in a deterministic batch. With its write step disabled during audit, its complete record list exactly matched all 198 archived version-1 records, including 385 call annotations.
3. The analysis script checked coverage, checksums and eligibility, then aggregated the fixed labels. Its role is calculation and binding validation, not semantic adjudication.
4. A subsequent targeted AI audit identified the source-description contradiction and rationale boilerplate problem. Version-1 annotation and rubric bytes were retained; the bounded correction produced version 2.
5. Version-2 reaggregation changed unsupported-prose totals to 9/60, 6/60 and 5/60. Raw responses, prompts, primary outcomes and reasoning/tool scores stayed unchanged.

Historical evidence is in `documentation/audit_history/`: `record_annotations_v1.py.txt`, `trace_inventory_v1.jsonl`, `tool_signatures_v1.json`, `apply_annotation_correction_v2.py.txt`, both version-1 assessment files, and an authoring-history README with hashes. The `.py.txt` files are deliberately inert. Do not run the old helper against the live submission: it would replace the current annotations with historical labels and use an inappropriate current rubric hash. Use `scripts/trace_review_analysis.py` to aggregate current labels.

## Separating the identified shared-premise error

The following is a descriptive partition of existing version-2 labels, not a new endpoint or revised scoring policy. Each denominator is all sixty main-phase responses in the condition; the two component rows sum to the total. Ambiguous wording remains separate.

| Unsupported explanation category | Baseline | Structured prompt | Prompt plus validator |
|---|---:|---:|---:|
| Repeats the identified incorrect threshold premise | 5/60 (8.33%) | 5/60 (8.33%) | 5/60 (8.33%) |
| Other unsupported assertions | 4/60 (6.67%) | 1/60 (1.67%) | 0/60 (0.00%) |
| All unsupported explanations | 9/60 (15.00%) | 6/60 (10.00%) | 5/60 (8.33%) |

The fifteen inherited cases are all population-question repetitions: five of five per condition. The other cases are baseline profit repetitions 1, 2, 3 and 5, and structured-prompt transaction-year repetition 4. “Other” means not repeating this identified premise; it does not prove a distinct causal origin for every assertion. Excluding population questions would require a denominator of 55, so the table deliberately retains the complete population and denominator of 60.

The common prompt is preserved verbatim as historical evidence. Correct population abstention remains defensible because the file is not established as a worldwide census and the task explicitly includes absent games. That does not validate the false threshold explanation. Under the retained narrow rubric, appropriate refusal and output alignment can receive full process credit while the separate prose-support assessment fails. The 0–6 total must not be interpreted as comprehensive reasoning soundness or factual accuracy.

## What would strengthen a future assessment

Independent human coding with a prospectively specified rubric, blinded condition labels where feasible, recorded disagreements and adjudication would strengthen semantic validity. A separately configured model judge would need its exact model snapshot, prompts, settings, input construction and raw outputs retained. Neither procedure can be retroactively claimed for this study. The current primary numerical findings remain supported by the frozen evidence; these improvements concern the validity of the supplementary qualitative assessments.
