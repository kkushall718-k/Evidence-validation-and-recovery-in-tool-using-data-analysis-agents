# Submission feedback implementation

> **Current length revision (23 September 2026):** The author confirmed that all sections count. The dissertation has been shortened to 12,000 whole-document words in LibreOffice and 47 rendered pages. See `Word_Count_Audit.md` for the current count, scope and verification. This dated review is retained as history; its earlier word counts, page counts and unresolved inclusion question are superseded. Scientific evidence and the twenty-entry bibliography are unchanged; literature prose has been condensed with all twenty sources still cited. This revision did not repeat the earlier external source audit.

Updated 23 September 2026 for Kushal Krishnamurthy. The revision implements the academic and presentation feedback using the existing experiment. It preserves all 198 raw observations and frozen primary definitions. No new paid API study was conducted.

| Feedback | Implemented response | Evidence |
|---|---|---|
| Metrics alignment | Twelve-area map with operational definitions, denominators, applicability and result locations | Dissertation Table 4.2 and Section 4.10 |
| Agent reasoning | Three observable 0–2 items, per-run rationales and descriptive 0–6 totals | Appendix D; completed AI-assisted annotation file |
| Tool selection and parameters | Call-level semantic judgements, alternative valid routes, separate profile/no-call/injection eligibility | Table 5.3; posthoc_review_calls.csv |
| Prose hallucination scope | Response-level unsupported-assertion incidence, exact excerpts and separate ambiguity sensitivity | Section 5.8; posthoc_review_runs.csv |
| Variance | Within-question sample variance and latency/cost dispersion; finite/null/nonnumeric coverage | Section 5.9 and two variance CSVs |
| 198-run evidence | Independent CSV/Decimal outcome calculation and local trace/ledger reconciliation | scripts/verify_evidence.py; executed notebook |
| Reproduction | Notebook executes primary, sensitivity, trace-review and independent verification steps | notebooks/Thesis_Experiment_Reproduction.ipynb |
| Captions and contents | Explicit numbered table captions and linked chapter/subsection contents | Revised DOCX |
| Architecture routes | Labelled bypass, validation pass, one correction and blocking paths | Figure 4.1 |
| AI disclosure | Explicit identification of AI-assisted semantic assessment and absence of human adjudication | Front matter, methods, discussion and appendix |
| Viva alignment | Updated supplementary findings, limits and examination preparation | Revised PowerPoint and Viva_Preparation.md |

## Interpretation retained

All conditions solve 30/30 answerable main tasks. Strict baseline abstention of 0/30 includes formatting failures and must not be described as thirty fabricated answers. The prompt and verified conditions have 28/30 and 29/30 strict abstentions. No verified run activates repair or blocking, so incremental validator effectiveness remains unestablished.

The semantic/prose assessment is post hoc, unblinded and completed by one AI assistant. It is inspectable, but lacks independent human validation. Its source hashes and reproducible aggregation protect traceability; they do not remove judgement subjectivity. Main-phase unsupported prose counts are 4/60, 1/60 and 0/60, while including ambiguous wording yields 8/60, 3/60 and 7/60. This sensitivity remains visible.

## Final verification

A fresh extraction of the submission package passed all eighteen tests. With the exact-checksum source CSV supplied locally, the primary evaluator, supplementary checks, trace-review aggregation and independent evidence audit all completed without model calls. All seventeen analysis CSV/JSON files reproduced byte for byte. The original raw records, frozen manifest, protocol and eleven original numeric analysis files remained unchanged.

The rendered Word document contains 12,000 main-text words, 51 pages, seven numbered tables, three numbered figures and 75 linked contents entries with matching rendered page numbers. Every page and all ten slides were visually inspected. The viva retains both native charts and their original embedded workbooks; its notes total ten minutes. All twelve notebook code cells executed, and the HTML preview was visually inspected. `Submission_Verification.json` records the checks and artifact hashes. These are local verification results, not an institutional compliance certificate or independent human assessment.

## Remaining author actions

The title page retains the four placeholders explicitly requested by the author: student number, programme, supervisor and submission date. Fill them before uploading. Retain the already-confirmed professor permission for AI assistance and use any current institutional declaration form. Check the current Canvas naming, file-format, supporting-file and deadline requirements. The supplied handbook does not independently establish the current portal state.

The author should read the revised thesis and rehearse the offline notebook and viva. The raw CSV is acquired separately at its exact checksum because redistribution permission was not established. Independent reproduction here concerns saved observations and local accounting, not an authenticated provider invoice or a promise of identical future API responses.

The earlier Feedback_Review.md documents the pre-revision assessment. This implementation record describes the revision; the historical review should not be mistaken for the current completion checklist.

## Subsequent academic audit on 23 September 2026

The later Academic_Submission_Audit.md supersedes the version-1 prose counts in this historical implementation record. Version 2 corrects fifteen population explanations that repeated a supplied threshold contradicted by the CSV, and removes inaccurate boilerplate from twenty-seven rationales. Current counts are 9/60, 6/60 and 5/60 unsupported explanations, or 13/60, 8/60 and 12/60 including ambiguity. Primary outcomes, reasoning scores and tool scores remain unchanged. See Source_Description_Correction.md and the current Submission_Verification.json.
