# Response to the second dissertation review

> **Current length revision (23 September 2026):** The author confirmed that all sections count. The dissertation has been shortened to 12,000 whole-document words in LibreOffice and 47 rendered pages. See `Word_Count_Audit.md` for the current count, scope and verification. This dated review is retained as history; its earlier word counts, page counts and unresolved inclusion question are superseded. Scientific evidence and the twenty-entry bibliography are unchanged; literature prose has been condensed with all twenty sources still cited. This revision did not repeat the earlier external source audit.


Kushal Krishnamurthy · M598 first attempt · 23 September 2026

**Readiness: Share with caveats.** The new review supports the research direction and identifies targeted disclosure and submission issues. It does not justify restarting the experiment or claiming an additional validator benefit. This audit found one substantive provenance omission and repaired it, with related clarification of inherited misinformation, reasoning-score scope and frozen costs. The experiment and all existing assessment scores remain unchanged.

**Completeness: Partial.** All seven supplied screenshots were inspected and compared with the current canonical manuscript, retained working files, annotations, code and evidence package. The review names `Kushal_Krishnamurthy_Dissertation-2.docx`, but that document was not in the supplied review folder. Conclusions apply to the accessible canonical dissertation; exact identity with the reviewer's copy cannot be certified. Current Canvas rules, the institution's word-count inclusions and independent human semantic validation remain outside the verified evidence.

## Highest priority findings

### 1 The supplementary evaluator needed a more precise method description

**Severity: P1. Fixed.** “Codex AI-assisted review” did not explain how annotations were created. The retained authoring helper shows a fixed, rule-assisted workflow: five unsupported and thirteen ambiguous prose exceptions, a supported default for 180 other responses, and specialised rules for reasoning and tool fields. Its generated records exactly match all 198 historical version-1 annotations. This is materially different from a separately configured model judge evaluating every record under a logged protocol.

Method 4.10 and Appendix D now describe that workflow and state the missing information. A new provenance document and inert historical authoring files are included in the evidence package. The original helper must not be rerun against current labels. The underlying evaluator model snapshot, sampling settings, full interactive instructions and presentation batches were not retained; none has been invented or borrowed from the experimental model configuration.

No human verification of these labels is documented. The later AI audit was a targeted correction, not an independent second rating set. Hashes and repeatable arithmetic establish traceability, not semantic validity. This limits the evidential weight of supplementary explanation, reasoning and tool-quality scores, while leaving the independently calculated primary outcomes intact.

### 2 Inherited misinformation needed to be separated from other unsupported explanations

**Severity: P1 interpretation risk. Fixed through disclosure.** The version-2 totals were already correct, and the shared-premise error was already acknowledged. The new review is right that an explicit partition makes their interpretation clearer.

| Main-phase unsupported explanations | Baseline | Structured prompt | Prompt plus validator |
|---|---:|---:|---:|
| Repeated incorrect premise supplied in the shared prompt | 5/60 | 5/60 | 5/60 |
| Other unsupported assertions | 4/60 | 1/60 | 0/60 |
| Total, unchanged | 9/60 | 6/60 | 5/60 |

Each condition has sixty main responses. All five population-question repetitions per condition repeat the incorrect threshold. The other cases are four baseline profit explanations and one structured-prompt transaction-year explanation. These are not independent new observations or a new causal test. “Other” means not repeating this particular premise, not proof that the model independently originated every claim.

Appendix D now gives the additive partition; Threats to Validity 6.5 explicitly discusses the shared prompt's conflict with 5,781 CSV rows. The prompt remains frozen. Removing the fifteen responses or rewriting the historical prompt would conceal a design limitation. No scores were changed.

### 3 Full process credit does not establish a factually sound explanation

**Severity: P1 interpretation risk. Clarified.** The population refusals can score 2/2/2 under the narrow observable rubric while containing a false supplied premise. The refusal is appropriate, and the output avoids asserting an unavailable population count; the separate factual-support label identifies the false explanation.

Appendix D now explicitly states that the 0–6 total measures selected observable analytical decisions, not comprehensive reasoning soundness or factual accuracy. Renaming every historical field or changing scores retrospectively would require a separately documented assessment amendment. The existing labels and rubric are preserved. If the assessment expects a validated general reasoning-quality measure, the current exploratory proxy does not establish that construct; this is separate from the professor's already-confirmed permission to use AI.

### 4 The ZIP exists but needs to accompany the manuscript

**Severity: delivery gap, not evidence that the experiment is missing. Verified locally.** The reviewer was not supplied the ZIP and could not locate it at the checked path. The canonical archive was present in `thesis_project/submission/`. Before this revision, all 350 manifest-listed files matched their local counterparts, and the archive hash matched the earlier verified package. That earlier fresh extraction reproduced all seventeen analysis CSV/JSON outputs and passed eighteen tests using the separately supplied, checksum-matched source CSV.

The current revision changes methodological disclosure and packaging only. Its archive includes the historical authoring evidence and this response. Recorded runs, manifest, runtime, prompts, rubric, version-2 annotations and numerical outputs remain unchanged. A final integrity check verifies the refreshed archive against current files; unchanged calculation inputs and logic reuse the prior fresh-reproduction evidence. This is a justified reuse of evidence, not a claim to have independently validated every semantic judgement or authenticated an OpenAI invoice.

Supply the dissertation and `Thesis_Project_Submission.zip` together through the permitted submission channel. The CSV is deliberately acquired separately because redistribution rights are unresolved; its required checksum and acquisition instructions are included. The exact local filename/location should be included in any reviewer handoff. No files were sent externally during this audit.

## Word count and cost checks

**The 12,010 versus 12,000 discrepancy is explained exactly.** Both the maintained source and the DOCX contain 12,010 whitespace-separated tokens in Chapters 1–7. Ten are standalone `/` symbols in tables. The documented counter excludes tokens without alphanumeric characters, producing 12,000. This is not ten missing words or a contradictory manuscript version.

The revised main text still contains 12,000 words under that same documented convention. The handbook specifies 12,000 for this M598 first attempt, with under/over-length penalties, but does not settle every inclusion/exclusion convention. The final institutional electronic count must be checked; do not assume a general ten-percent allowance or delete ten words solely because a different counter includes punctuation. The 51-page all-inclusive rendering remains one page above the handbook's 50-page figure, so its treatment of preliminary pages, references and appendices needs confirmation.

**Frozen prices and formula are now explicit in Method 4.8.** The recorded study uses USD $0.40 per million uncached input tokens, $0.10 cached input and $1.60 output. For total input I, cached input C and output O:

`cost = [0.40 × (I − C) + 0.10 × C + 1.60 × O] / 1,000,000`

Independent decimal calculation matches all 198 per-run costs. Totals are 728,937 input tokens, of which 174,208 are cached, and 53,635 output tokens, giving **$0.3251284** for the experiment. The existing ledger total including the initial smoke check is **$0.325364**. These are frozen usage-based estimates, not current price quotations or invoice reconciliation. Cached tokens must not be charged once as ordinary input and again as cached input.

## What the new review already accepts

The review recognises that the metrics-and-scope table, semantic tool and parameter assessments, numerical variance, numbered captions, expanded contents and clarified validator routes have been added. These are resolved items, not a reason to create more charts or broaden the project. The current score variances of 0.30 and 0.20 for success proportions 3/5 and 4/5 are consistent with sample variance using n−1; consistency and correctness remain distinct.

The central research claim remains bounded: structured prompting improved handling of the tested unsupported questions; successful execution and matching evidence did not guarantee the requested meaning; the observed experiment did not demonstrate incremental benefit from the validator. All answerable runs succeeded, and no recorded validator repair or block was triggered. A null result is defensible when reported honestly. More features or another dataset are optional future work, not necessary repairs established by this review.

## Citations and submission standards

The new review spot-checks HalluLens, DS-1000 and G-Eval; it does not establish a full citation or plagiarism audit. The prior project audit examined all twenty bibliography entries and their primary sources. The references and literature chapters are unchanged in this revision, so that source-verification evidence remains applicable. See `Citation_Audit.md` for the source-by-source record and remaining style caveats. This supports the existence and bibliographic basis of the references; it does not replace an originality-database check or certify every institutional Harvard detail.

The title-page placeholders remain intentionally present because the user explicitly requested them: student number, programme, supervisor and submission date. They require real details before submission. The author's name is already correct. Professor permission for AI assistance has been confirmed by the user; this audit does not reopen that permission request. The final declaration must accurately describe the actual coding, drafting and review assistance and use any current required institutional wording.

The prior academic audit also leaves viva preparation actions visible: make related-work positioning and backup evidence easy to present, rehearse the ten-minute delivery, and prepare to explain the semantic counterexample, frozen scoring contract and annotation limitations. No additional paid experiment is needed to address the review's stated issues.

## Scoped review scorecards

Counts below describe this review's declared components and questions, not a grade or a percentage of the entire dissertation verified. Categories overlap. A zero means no observed unresolved defect in that scoped inventory; missing institutional or independent assessment evidence is stated separately.

### Dissertation quality and presentation

| Category | Observed defects | Assessment |
|---|---|---|
| Usefulness and completeness | 1 / 9 | The new review’s nine principal questions are addressed. Four intentional title placeholders remain; institutional word-count and declaration requirements remain unverified. Partial review: 2 scoped items have incomplete or stale evidence (Institutional word and page convention; Current AI declaration wording). |
| Analytical clarity | 1 / 6 | Method, results interpretation, threats and appendix disclosures are explicit. The introduction’s indirect dataset-fit sentence remains an optional P2 wording improvement. |
| Visual consistency | 0 / 6 | All six changed pages were inspected at full size. The other forty-five pages are byte-identical to prior inspected pages. The render remains 51 pages; the institution’s 50-page convention is separate. |

### Analytical correctness and robustness

| Category | Observed defects | Assessment |
|---|---|---|
| Source authority and confidence | 0 / 4 | The handbook, retained CSV, recorded responses and annotation provenance were inspected. Missing evaluator settings and independent human validation are disclosed; provider-side authenticity and current institutional rules are unverified. Partial review: 3 scoped items have incomplete or stale evidence (Supplied handbook; Recorded experiment; Supplementary assessment). |
| Value accuracy | 0 / 4 | The prose partition and all 198 costs were independently recomputed. The word-count discrepancy is exactly ten slash tokens. Existing variance results reuse unchanged calculation and reproduction evidence. |
| Within-chart agreement | N/A | No empirical chart was changed or newly assessed in this focused review; prior chart checks remain in the academic audit. Not applicable: No empirical chart was changed or newly assessed in this focused review; prior chart checks remain in the academic audit. |
| Complete source details | 0 / 22 | Twenty unchanged references retain the prior primary-source audit. The annotation workflow and frozen cost specification are now explicit. Exact departmental Harvard style remains an institutional caveat. |
| Cross-artifact consistency | 0 / 5 | Maintained sources, DOCX, convenience copy and refreshed archive agree. Unchanged viva and notebook results retain their prior verification; no numerical results changed. |
| Data-quality controls | 1 / 3 | One historical defect remains in the frozen shared prompt: its sales threshold conflicts with the CSV. It is explicitly disclosed and partitioned; raw evidence is preserved. Annotation bindings are verified, but independent semantic validation is unavailable. Partial review: 1 scoped item has incomplete or stale evidence (Fixed annotation bindings). |
| Conclusion support | 0 / 4 | The three research conclusions and supplementary process-score interpretation remain bounded. No general superiority, active validator benefit or comprehensive reasoning validity is claimed. |

## Remaining actions in priority order

1. Fill the four requested title-page placeholders and use the actual submission date.
2. Confirm the institutional electronic word-count scope, the 50-page convention, current Canvas file requirements and final AI-declaration wording. These cannot be established from the supplied screenshots alone.
3. Deliver the current DOCX and evidence ZIP together. Check the receiving system has both; an inaccessible archive cannot be evaluated by the examiner.
4. Treat supplementary semantic and process ratings as exploratory. Independent human checking would strengthen them, but is not established as a mandatory requirement by this review. Do not claim it has already happened.
5. Finish the viva preparation identified above. Optionally tighten the introduction's “It provides a setting because…” sentence into a direct explanation of why this dataset exposes the targeted semantic errors. This is a P2 wording improvement; it does not affect results.

The detailed numerical findings, reproducible implementation and bounded conclusions are defensible within the reviewed evidence. Unconditional submission readiness still depends on the personal and institutional checks above.
