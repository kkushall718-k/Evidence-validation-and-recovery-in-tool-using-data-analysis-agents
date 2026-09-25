# Supplementary trace review rubric

Version 1, 23 September 2026. This is a **post hoc, unblinded AI-assisted review** of the existing 198 recorded interactions. Codex inspected every final explanation and the complete sequence of tool names, arguments and execution results, using the question, CSV schema, independent reference answers and saved receipts. The reviewer had already seen the conditions and primary results. No independent human reviewer or inter-rater reliability is claimed. These exploratory judgements supplement the frozen primary metrics and must not be treated as a validated psychometric measure or evidence of private internal reasoning.

## Sources and coverage

All 180 main runs and 18 recovery runs are included. The saved annotations contain one record per run and one record per tool call, including injected failures. Each run is bound to the SHA-256 of its canonical complete JSON record. Each tool annotation retains its exact arguments, receipt identifier and call index. Prose concerns retain an exact excerpt. The review covers final explanations and final structured claims, not every intermediate API output as a separate factual response.

The analysis script validates these bindings before aggregating. It reproduces calculations **from the fixed annotations**; it does not regenerate or independently validate the semantic judgements. A new model study or changed raw record needs new annotations. No paid judge API is used. The original optional human-review form remains unscored and is not presented as completed human assessment.

## Prose factual support

Each final explanation receives one mutually exclusive category. The most serious applicable category controls the response-level label:

- **0 supported:** factual statements and described methods agree with the CSV, executed receipts and declared dataset scope. A concise accurate limitation qualifies. This is absence of a detected problem under this review, not proof that all possible interpretations are true.
- **1 ambiguous:** wording leaves scope, time interpretation or reporting extent unclear, without a definite contradiction established in context. Keep these separate from confirmed unsupported claims.
- **2 unsupported:** at least one factual or quantitative assertion is contradicted by the evidence or treats an unavailable measure as established. A disclosed hypothetical assumption does not justify presenting its result as the requested actual profit or transaction total.

The principal supplementary prose incidence is category-2 responses divided by all reviewed final responses within the same phase, condition and task type. A sensitivity endpoint combines categories 1 and 2. This is **response incidence**, not the fraction of individual sentences or claims that are false. The original unsupported structured-claim measure remains separate. A correct caveat can coexist with an incorrectly populated structured field.

Examples: multiplying unit sales by an assumed dollar of profit and presenting actual net profit is category 2; claiming that release-cohort totals are transactions in 2008 is category 2. Describing release-cohort sales as sales “in this period”, without a clear temporal distinction, is category 1. An explanation that correctly says the transaction quantity is unavailable can be category 0 even when its structured answer wrongly supplies a proxy; the latter is penalised by primary scoring and the reasoning alignment item.

## Observable analytical reasoning

Three ordinal items, each 0–2, produce a descriptive total from 0 to 6. Publish item values as well as totals. Equal weighting is a pragmatic reporting choice, not an established measurement model.

| Item | 0 | 1 | 2 |
|---|---|---|---|
| Task interpretation | Treats an unavailable quantity as derivable, or materially misstates the requested quantity | Recognises a limitation but still substitutes a different quantity | Correctly identifies the calculation or why it cannot be supported |
| Method and evidence | Uses an unsuitable quantity or unsupported conversion to support the requested answer | Contains avoidable invalid arguments, an unproductive permanent-error retry or incomplete visible support for a missing-data claim, despite a defensible final answer | Appropriate executed analytical/diagnostic steps, or a justified refusal from supplied context, support the response |
| Explanation and output alignment | Explanation asserts an unsupported answer, or contradicts the meaning of a populated answer field | Ambiguous wording, or an acknowledged unavailable result represented using answered status and the literal string null | Explanation agrees with the executed method, available evidence and meaning of the final claims |

An absence claim about prices/costs, distribution channels or marketing data requires schema inspection or direct error evidence for full method credit. Selecting only sales columns does not inspect the complete schema. The review therefore gives partial method credit to otherwise correct profit refusals, the distribution refusal using only selected columns, and marketing refusals without schema inspection. Release-year interpretation and population coverage are explicitly supplied in the common context and can support their corresponding limitations. This distinction concerns observable evidence, not whether the refusal happens to be true against the CSV.

Omission of null fields, by itself, is left to the strict response-contract metric rather than automatically making a sensible explanation unsound. A transient injected service failure is not an avoidable reasoning error. No-call refusals can score fully when the supplied context establishes the limitation. A recovered invalid argument remains visible as a method score of 1, even if the final numerical answer is correct. This process penalty is distinct from task success.

## Semantic tool selection

For each call, judge whether the selected tool and operation are usable for the requested analysis or a defensible diagnostic subtask in the observed response. Profiling, appropriate counting/selection/aggregation, receipt-based plotting and bounded transient retries qualify. A query whose requested measure does not exist is unsuitable for calculation from this CSV. Executing a release-cohort or unit-sales calculation as the requested transaction total or net profit is unsuitable, even if the operation executes successfully. The same calculation may be a permissible diagnostic when the final response correctly abstains and describes its limited meaning. This contextual judgement describes how the call is used; it does not infer an unseen intention.

A grouping/measure argument conflict does not by itself make the choice of aggregation unsuitable; parameter accuracy records that error. Alternative valid paths are accepted, including separate counts versus one disjunction, profiling versus explicit missing-value counts, differing irrelevant chart titles, and alternative ordering of a complete category result. Extra calls are not automatically wrong because efficiency is a separate measure.

Selection accuracy = suitable **non-injected** calls / all non-injected calls in the same phase and condition. Calls in runs with no tools contribute no denominator; their counts are reported separately. There is no automatic full-credit tool score for a no-call run. A run-level all-calls-suitable endpoint is reported only for runs with eligible calls, and does not imply final-answer correctness.

## Semantic parameter accuracy

Score query and plot calls. Profile has no analytical arguments and is inapplicable. Parameters must identify existing columns and appropriate measures, filters, boundaries, grouping, aggregation, sorting, limits, evidence receipts, axes, series and units for the requested calculation or the explicitly limited diagnostic subtask. Assess effective tool semantics rather than exact string equality: grouping drops missing group keys, so the alternative publisher-not-empty filter plus that grouping is accepted for the observed publisher task. A one-filter any predicate is equivalent to all. Count operations count rows irrespective of unused aggregation defaults.

Unavailable columns, using a grouping key also as an aggregated measure, or interpreting release year as transaction year and units as dollars fail. Receipt-based plots must refer to a successful prior query and the intended rows/axes/series. Correct parameters in a deliberately injected failure remain annotated correct, but that call is excluded from ordinary parameter-rate denominators. Repeating an unchanged permanent schema error remains an incorrect parameter decision and is flagged separately.

Parameter accuracy = correct non-injected query/plot calls / all non-injected query/plot calls in the same phase and condition. Selection and parameter judgements overlap for some failures and are not statistically independent constructs. They are also informed by the observed final response, so they are diagnostic associations rather than independent causal predictors of correctness.

## Variance and descriptive reporting

Use complete five-repetition **main-study question-by-condition** groups. For binary task success, report sample variance with denominator n−1 and success count/n. For latency and cost, report mean, sample standard deviation, sample variance and coefficient of variation where the mean is positive. Do not pool different questions to describe repeated-run variability.

For each requested scalar, retain total runs, null/missing values, nonnumeric values and finite numeric values. Numeric sample variance uses only finite observations and requires at least two; otherwise it is missing, not zero. Label this conditional coverage explicitly. Categorical fields have no numeric variance. Numerically asserted values on unsupported questions remain included with their unsupported status; zero variation does not validate them. No null is converted into a numerical zero.

All aggregates retain phase and task type where relevant. Report numerator/denominator for binary rates and descriptive means for ordinal items. Do not claim population significance or human agreement from a single unblinded AI-assisted review. Ambiguous prose receives a separate sensitivity analysis. The review is auditable and useful for locating failures, but external human adjudication remains a limitation.
