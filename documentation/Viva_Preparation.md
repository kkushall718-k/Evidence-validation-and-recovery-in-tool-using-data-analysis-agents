# Viva preparation

The handbook specifies a ten-minute presentation followed by ten minutes of questions. The PowerPoint has ten slides with speaker notes totalling ten minutes of planned speaking time. Practise aloud and shorten examples if necessary; a timing plan is not a recorded rehearsal.

| Slide | Focus | Seconds |
|---|---|---:|
| 1 | Problem and project | 45 |
| 2 | Research questions | 55 |
| 3 | Implemented system | 65 |
| 4 | Controlled comparison | 60 |
| 5 | Answerable-task ceiling | 50 |
| 6 | Abstention and format sensitivity | 75 |
| 7 | Real semantic counterexample | 80 |
| 8 | Validator and recovery findings | 65 |
| 9 | Supplementary semantic assessment and its limits | 60 |
| 10 | Conclusions and next step | 45 |

## Questions to be ready to answer

**What is your technical contribution beyond prompting?** The executable tool interface, per-claim evidence receipts, runtime validator and bounded repair loop, frozen experiment harness, independent chart and scalar scoring, and offline reproduction package. The empirical study does not establish that every implemented component improves outcomes.

**Did you fine-tune a model?** No. The model weights and snapshot are fixed. Prompt instructions and host-side validation are the interventions.

**What did the validator improve?** Its incremental effectiveness was not demonstrated. No verified run activated its repair or block path. The one-run final-score difference cannot be attributed to feedback that never occurred. Deterministic challenge checks demonstrate implementation behaviour only.

**Why keep an unsuccessful intervention?** A transparent null result identifies the mechanism's limits. Removing failures or tuning after seeing the results would weaken the evidence. The actual semantic counterexample is a useful finding.

**Why is baseline abstention zero?** Under the strict contract, unsupported answers must include the named null fields. Fifteen baseline refusals omitted them. The post hoc relaxed rule gives 15/30, so zero strict successes does not mean every baseline answer was fabricated.

**Why are there ten non-null outputs but only nine numerical assertions?** One baseline response used the string `"null"` instead of JSON null. The frozen endpoint counts any non-null value; the sensitivity counts only finite numeric values.

**What is the most important real failure?** Verified A05 repetition 5 returns 678.9 in a transaction-year field. That number is the release-cohort total. Its citation is valid, but the requested quantity is different, and the prose itself acknowledges the limitation.

**Why not count a blocked answer as a correct refusal?** A contract failure does not establish that the question is unanswerable. Blocking produces an operational error and remains a failed task.

**How did you avoid giving the model the answers?** The tools expose the dataframe and receipts. The offline answer-key module is not imported into the runtime tool module or supplied in API inputs. The runtime checker receives field names and receipts, not reference values.

**How independent is ground truth?** The expected answers are derived separately from the agent query code and checked again with CSV and Decimal calculations. Shared task interpretation remains a possible common source of error.

**Are thirty runs thirty independent questions?** No. They are six questions repeated five times. Run-level Wilson intervals are descriptive. Paired bootstrap comparisons resample six question-level differences and are not broad population inference.

**Why did stronger instructions have more failed tool calls?** Executability and final correctness differ. Some calls asked for unavailable measures and were followed by appropriate abstention; two answerable prompt errors were recovered. Failed calls consume resources but do not always imply a wrong final answer.

**What does 6/6 recovery prove?** Only that the configurations recovered from the explicit one-time first-query failure with a clear retry instruction. It does not establish resilience to persistent outages, misleading errors or corrupted results.

**What is the dataset limitation?** Historical, selective game-platform records; units are millions of copies, Year is release year, and coverage is not a worldwide census. The experiment tests operations over the supplied records, not the source's real-world measurement accuracy.

**Who assessed reasoning and prose?** Codex performed a post hoc, unblinded AI-assisted review of all 198 explanations and 385 tool calls. Three observable reasoning items produce an exploratory 0–6 score. Each judgement has a rationale and source binding. This is not private internal reasoning, independent human evaluation or a validated general-ability measure.

**Why no human ratings or kappa?** No human ratings were collected, and one AI-assisted reviewer cannot establish inter-rater agreement. The optional human-review instrument remains blank. The completed AI-assisted annotations are a separate file. Reproducing their aggregation verifies arithmetic, not the validity of the labels.

**How is semantic selection different from executable calls?** It asks whether an operation serves the requested quantity or a defensible diagnosis. An executable release-cohort sum used as transaction-year sales fails. Parameter assessment additionally checks effective filters, measures, grouping and chart arguments. Profile calls have no parameter score; no-call refusals receive no automatic tool credit. The two semantic measures overlap and are not independent causal predictors.

**Why is unsupported prose lower than unsupported structured answering?** Several transaction-year explanations correctly acknowledge that the requested number is unavailable while their fields supply a proxy. Prose support and field correctness therefore differ. Main-phase unsupported prose counts are 9/60, 6/60 and 5/60; including ambiguous wording gives 13/60, 8/60 and 12/60. Do not hide that sensitivity.

**What does variance show?** Binary sample variance on the transaction-year task is 0, 0.3 and 0.2 over five runs. All other groups have zero binary variance. The baseline is consistently wrong on unsupported tasks under the strict rule. For the asserted transaction-year number, verified has only one finite value, so its numeric variance is undefined. Nulls are not zeroes.

**What changed after the protocol froze?** The evaluator received a documented plotting correction; its frozen version remains archived. Separate post hoc sensitivities, implementation challenges, semantic/prose annotations and variance analyses were then added. No primary scoring definition, prompt, runtime intervention or collected record changed. The new rubric was not preregistered.

**How much did it cost?** $0.325128 for the experiment and $0.325364 including the smoke check, calculated from actual returned usage at recorded prices. This is not a provider invoice reconciliation or development labour cost.

**What would you do next?** Prospectively test unseen tasks and another dataset, represent quantity semantics explicitly, and compare active validator feedback with an equally budgeted revision opportunity. Avoid adding many unrelated features.

## Short offline demonstration

Open the executed notebook. Show 198/198 coverage, strict-versus-relaxed results, the A05 verified answer, supplementary semantic scores and the variance example. Show the independent verification result and explain that the cells make no API calls. Keep the eight deterministic validator checks available for questions. Acquire the exact CSV and rehearse the notebook before any live demonstration.

## Author preparation

Read every chapter and run the offline notebook personally. Be able to explain the null result, the response-format sensitivity and each boundary of the validator in your own words. Replace the title-page placeholders, and retain the supervisor's AI permission and relevant ethics/supervision records. Do not claim personal implementation steps or validation activities you cannot explain.

**Why did the supplementary prose totals change?** All fifteen population answers repeat a sales threshold supplied by the source card and common prompt. The CSV contradicts that strict threshold. Version 2 flags those explanations while preserving the correct population refusals and the narrow reasoning anchors. Original annotations and the amendment are archived. This is an inherited premise error, not evidence that the model independently invented the threshold.
