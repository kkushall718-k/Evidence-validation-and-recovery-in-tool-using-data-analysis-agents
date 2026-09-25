# Academic submission audit

> **Current length revision (23 September 2026):** The author confirmed that all sections count. The dissertation has been shortened to 12,000 whole-document words in LibreOffice and 47 rendered pages. See `Word_Count_Audit.md` for the current count, scope and verification. This dated review is retained as history; its earlier word counts, page counts and unresolved inclusion question are superseded. Scientific evidence and the twenty-entry bibliography are unchanged; literature prose has been condensed with all twenty sources still cited. This revision did not repeat the earlier external source audit.

> Later review: `documentation/New_Review_Response.md` and `documentation/Trace_Review_Provenance.md` add the original annotation-authoring workflow, evaluator-provenance gaps, inherited-error partition and explicit frozen cost formula. Read those disclosures with this earlier audit. Its unchanged numerical and citation checks remain applicable.

Kushal Krishnamurthy · M598 · 23 September 2026

**Readiness: Share with caveats.** The project is a credible, bounded empirical computing dissertation with a substantive implementation and reproducible primary results. The audit found and repaired one material supplementary assessment defect. It does not establish a guaranteed grade or unconditional permission to submit. Personal metadata and current institutional submission checks remain outstanding.

**Review completeness: Partial.** The supplied handbook, all seven chapters, all twenty references, recorded experiment, evaluation code and supporting artifacts were examined within the scope below. Current Canvas instructions, official personal approval records, the exact departmental Harvard variant, an originality-database report, native Microsoft Office behaviour and the author's viva understanding were not independently verified. A risk-focused semantic re-review inspected seventy distinct responses and fourteen complete tool sequences; it was not a second independent human assessment of all 198 responses.

**Changes made:** corrected the source-description/prose assessment, propagated the results to the thesis, notebook and viva, repaired twenty-seven inaccurate rationale sentences, clarified a metric numerator, corrected undated documentation citations and reference styling, and refreshed the evidence archive. Frozen prompts, runtime, protocol, raw records and primary outcomes are preserved.

## Findings and disposition

### 1. P1 Fixed — the supplementary prose review accepted a contradicted supplied premise

The source card and common prompt describe games selling over 100,000 copies. The retained CSV has **5,781 game-platform rows below 0.10 million recorded global sales**, and 6,181 at or below that value. Even summing included platform rows by exact Name leaves 3,940 names below 0.10 million. This establishes an internal source-description/data discrepancy; it does not independently establish complete real-world sales for each title.

All fifteen population-question explanations asserted the hard threshold directly and were previously marked supported. Version 2 now marks those assertions unsupported. The requested worldwide census remains unavailable, so the refusal outcomes and frozen primary scores remain correct. The error was inherited from supplied context; it must not be described as an unprompted invention by the model. The experiment itself has not been rewritten after collection.

| Main-phase endpoint, 60 responses per condition | Baseline | Prompt | Verified |
|---|---:|---:|---:|
| Unsupported explanations, corrected | 9/60 | 6/60 | 5/60 |
| Ambiguous wording only | 4/60 | 2/60 | 7/60 |
| Unsupported or ambiguous explanations | 13/60 | 8/60 | 12/60 |
| Observable reasoning mean, unchanged | 4.87 | 5.40 | 5.45 |

The reasoning score has narrower anchors: recognition that the requested quantity is unavailable, a context-supported refusal and agreement with null output fields. Those anchors are retained rather than silently adding a new penalty. They do not certify every premise as true. See [the amendment](Source_Description_Correction.md), thesis Section 4.2, Table 5.3 and Appendix D. Original annotations and rubric remain in `audit_history/`.

### 2. P2 Fixed — annotation explanations and one metric label were imprecise

Twenty-seven rationales incorrectly said invalid arguments were visible, although the affected traces had no non-injected failed call. Their partial method score was justified by incomplete schema inspection. Only the false sentence was removed; no reasoning or tool score changed. The hallucination row in Table 4.2 now identifies runs asserting values as its numerator, consistent with the actual response-incidence endpoint. It does not imply an atomic claim-count rate.

### 3. P2 Fixed in part — references were valid but needed publication-date and style cleanup

All twenty references identify genuine primary sources and have matching in-text citations. No fabricated publication, unmatched reference or material misrepresentation of the cited scholarly claims was found. The review checked publisher/author metadata and abstracts or relevant source passages, not every page of every paper. Three official living documentation pages did not establish 2026 as their publication year; their labels now consistently use n.d.a/n.d.b/n.d.c. Publication and webpage titles receive italics in the rendered bibliography.

**Minor proposed polish:** the three NeurIPS entries have precise publisher URLs but omit page spans/DOIs. Complete these if required by the department's Harvard variant. This is bibliographic consistency, not missing evidence. The exact institutional variant and originality report remain unverified. The [twenty-source audit](Citation_Audit.md) links each primary source and records access limitations.

### 4. P2 Proposed — the viva could make prior work and the research gap more visible

The ten-slide deck explains the research questions, implementation, comparison, findings and limits, with a 600-second speaking plan. It does not give related work its own visible treatment, and there are no dedicated backup slides. The CDS presentation guidance recommends both. A short comparison to ReAct/tool-use benchmarks and the narrower evidence-versus-meaning gap would strengthen the defence. Existing `Viva_Preparation.md` supplies questions and a demonstration route. The notes' timing is a plan, not evidence of a completed rehearsal.

### 5. Needs input — author and institutional checks cannot be certified from project files

The four title-page placeholders are intentional, following the author's instruction: student number, programme, supervisor and date. Complete them before upload. The 12,000-word count uses the documented project method and excludes front matter, references and appendices; confirm the institution's counting convention in Word. The complete rendering is 51 pages including those sections; the handbook lists 50 pages alongside 12,000 words but does not clarify whether that page figure is an independent hard limit or which sections it includes.

Professor permission for AI assistance was explicitly confirmed by the author and is disclosed, including drafting and analysis. This audit does not demand permission again. The actual approval/ethics records, six-meeting log, current declaration template, Canvas deadline, permitted upload format and supporting-file rules were not independently inspected. Their absence from this package is not proof they were not completed. An institutional originality check and personal viva rehearsal remain separate author actions.

## Handbook requirements matrix

The governing supplied document is the February 2026 Dissertation Module Handbook. Page numbers below refer to that PDF. Historical 80-run planning files in `files-3` are not current experimental evidence or additional university rules. In particular, their two-human-rater plan and old repository filenames are superseded by the disclosed fresh design.

| Requirement or recommendation | Evidence and assessment |
|---|---|
| M598 single-student dissertation: 12,000 words / 50 pages, p.4 | Project count is 12,000 across Chapters 1–7 including headings, tables and figure captions. Complete PDF rendering is 51 pages. Counting exclusions and page-limit interpretation need institutional confirmation; no assumed 10% tolerance. |
| Clear problem, objectives and contributions: 15%, p.4 | Met in structure: explicit aim, three RQs, scope and four contributions in Chapter 1. Claims are limited to configuration-level empirical evidence. |
| Comprehensive, critical and relevant literature: 20%, p.4 | Substantially addressed by a separate foundations chapter and thematic critical related work. Twenty relevant references, including fifteen peer-reviewed papers. No handbook reference-count quota. A cross-paper synthesis could strengthen this heavily weighted criterion. |
| Method explanation, justification and application: 15%, p.4 | Frozen protocol, three controlled conditions, executable tools, architecture, independent answer key, metrics and scheduling are specified. The source-description defect is now disclosed. |
| Results and interpretation linked to earlier chapters: 20%, p.4 | Results are traceable to records; Chapters 6–7 return to all three RQs. Null validator benefit, ceiling effects and representational sensitivity are stated. |
| Scientific writing, visuals, logic and Harvard referencing: 10%, p.4 | Seven chapters, numbered tables/figures, linked two-level contents and attributed literature. Citation repairs completed; exact local Harvard variant remains an external check. |
| Viva: 20%; ten-minute individual presentation plus ten-minute questions, p.4 | Ten slides and 600-second note allocation provided. Actual delivery and Q&A understanding unverified. Related-work and backup-slide guidance only partly addressed. |
| Pass each overall assessment element, pp.4,6 | Requires at least 40/80 dissertation and 10/20 viva. It does not imply a separate 50% minimum for each viva subcriterion. No grade prediction is made. |
| At least six supervision meetings, p.3 | Author reports the process went well. The supervisor's log is not in reviewed evidence; no log has been fabricated. |
| Ethics approval before collection, including secondary data, p.5 | Public secondary-data design and absence of recruited human raters are clear. Actual approval evidence remains the author's institutional record. |
| Permitted and declared AI assistance, p.5 | Substantial coding, drafting, evaluation and presentation assistance disclosed; professor permission confirmed by the author. Current institution-specific declaration wording is not independently checked. |
| Current Canvas deadline, first attempt, p.2 | Deadline and folder rules remain authoritative and unverified. The retake-specific ten-day draft rule does not apply to this first attempt. |
| Permitted CDS research type and technical contribution, p.7 | Development plus controlled empirical evaluation is within the permitted list. Tools, receipts, validation/repair and reproducible evaluation provide technical contribution beyond prompt wording. |
| Evidence of technical contribution, p.7 | Documented implementation and executable source ZIP are supplied. GitHub is given as an example in the handbook, not an exclusive requirement. Confirm whether Canvas specifically demands a repository link. |
| Structure and template guidance, p.8 | Foundations, related work, method, results, discussion and conclusion follow CDS guidance. Word is permitted; a specific font/template is not established as mandatory by the inspected wording. |
| CDS introduction should point to implementation, p.22 | Appendix C names the package and exact reproduction commands. A direct introduction pointer or personal repository link would improve discoverability; hosting is not fabricated. |
| Reproducibility and environment detail, p.23 | Dataset/version/checksum, model snapshot, parameters, schedule and package versions are retained. `environment.json` records Python/macOS/architecture; precise hardware model/RAM are absent. Timing is appropriately descriptive. |
| Baselines, evaluation, comparison and interpretation, pp.23–24 | Three local conditions and post hoc implementation challenges are present. No compatible external state-of-the-art benchmark was run; the thesis does not claim superiority over one. Such a comparison is recommended strengthening, not a fabricated result. |
| Harvard sources should be relevant, recent and reputable, p.24 | Primary ACL/ICLR/ICML/NeurIPS/JMLR/statistics sources and official documentation are used. Foundational statistics references remain appropriate; recent work includes 2025 studies. |
| CDS viva should cover prior work/gap and backup material, pp.24–25 | Main deck underrepresents visible related work and has no backup slides. Suggested improvement, distinct from the mandatory time and assessment requirements. |

## Research standards and evidence

The main design contains **twelve distinct questions**, five repetitions and three conditions: 180 interactions. Eighteen recovery trials use two questions with three repetitions per condition. The 198 records are not 198 independent research questions. Randomized matched scheduling reduces ordering bias but does not remove remote service variability or create a held-out test set. The improved prompt explicitly names tested semantic categories, so the main finding is adherence on a purposive benchmark rather than broad generalisation.

Primary outcomes were independently recomputed using a separate standard-library CSV/Decimal implementation, with all 198 strict task outcomes matching. Answerable task success is 30/30 and chart success 20/20 in every condition. Strict unsupported success is 0/30, 28/30 and 29/30; relaxed success is 15/30, 28/30 and 29/30. The change of denominator/contract is disclosed rather than replacing the frozen endpoint. Numeric unsupported assertions are 9/30, 2/30 and 1/30.

The evidence contains 583 unique benchmark response IDs, 385 calls and 69 chart files. The ledger has 584 settled entries including the interface check. Estimated token cost is $0.3251284 for the experiment and $0.325364 including that check. Local consistency does not independently authenticate the provider or reconcile a bill.

No recorded validator repair or blocking occurred. Therefore the small prompt-to-verified difference cannot establish a repair benefit. Eight deterministic implementation challenges are separate from the model experiment. All eighteen recovery trials succeeded after one explicitly retryable injected failure, a narrow result that does not demonstrate recovery from persistent or ambiguous errors.

Tool execution success is correctly separated from semantic tool choice and parameter correctness. Calls absent from a run receive no automatic full score; injected failures are excluded from ordinary denominators; profile calls have no analytical-parameter denominator. Within-question variance uses n−1, preserves missingness and distinguishes stable error from stable correctness. Only two of 36 binary groups have nonzero variance; one finite verified transaction-year assertion has undefined numerical sample variance.

The supplementary review is useful for locating failures but remains post hoc, unblinded and AI-assisted without independent human validation. A second agent audit does not turn those labels into human ground truth. The newly detected threshold error illustrates why annotation arithmetic and cryptographic bindings alone do not establish semantic validity. This boundary is central to a defensible viva.

## Detailed review scorecards

The counts below describe demonstrated unresolved defects in scoped units, not grades or accuracy percentages. Categories overlap and must not be summed. Zero defects does not mean every possible check passed. The coverage record identifies unverified institutional and semantic checks. Dashboard-only controls and interactions are not applicable to this dissertation.

### Dissertation usefulness and presentation

| Category | Observed defects | Assessment |
|---|---|---|
| Usefulness and completeness | 2 / 21 | The dissertation and technical evidence address the core assessment areas. Intentional title placeholders and missing visible viva prior-work/backup treatment remain; institutional checks are separate. Partial review: 5 scoped items have incomplete or stale evidence (M598 single-student dissertation: 12,000 words / 50 pages, p.4; At least six supervision meetings, p.3; Ethics approval before collection, including secondary data, p.5; and 2 more (see review notes)). |
| Clarity | 0 / 12 | Seven chapters, front matter and four appendices disclose denominators, scope and the corrected source premise. No remaining demonstrated clarity defect in these twelve sections. |
| Visual consistency | 0 / 20 | Seven tables, three figures and ten slides retain readable layouts. Changed renders were re-inspected and identical pages/slides reuse prior evidence. |

### Scientific and citation reliability

| Category | Observed defects | Assessment |
|---|---|---|
| Source authority | 0 / 23 | Twenty genuine primary references plus the handbook, source CSV and recorded study. Provider-side authenticity is outside local trace verification. Partial review: 1 scoped item has incomplete or stale evidence (Recorded provider interactions). |
| Value accuracy | 0 / 12 | Twelve requested metric areas are linked to exact denominators and reproducible calculations. Annotation arithmetic is verified separately from judgement validity. |
| Within-chart agreement | 0 / 4 | Two dissertation empirical figures and two native slide charts match the retained numerical outputs; native chart/workbook parts are preserved. |
| Source details | 0 / 20 | All twenty references are matched and retrievable. Undated documentation labels and title styling were repaired. Optional NeurIPS completion and exact departmental style remain minor caveats. |
| Cross-artifact consistency | 0 / 5 | Thesis, slides, executed notebook, HTML and archive report the corrected version-2 prose totals. Frozen primary outputs remain unchanged. |
| Data quality | 1 / 5 | The frozen supplied threshold remains inconsistent with the CSV and is disclosed as a historical design limitation. Assessment labels are repaired; complete independent semantic validation remains unavailable. Partial review: 1 scoped item has incomplete or stale evidence (Version-2 supplementary annotations). |
| Conclusion support | 0 / 7 | Three RQ answers and four principal interpretation claims remain bounded to the observed design. No incremental validator benefit or broad population performance is claimed. |

## Verification and artifact identity

The final verification receipt records artifact hashes, the unchanged frozen-record hashes, all seventeen reproduced CSV/JSON outputs, eighteen passing tests and the executed twelve-cell notebook. A fresh ZIP extraction receives the exact-checksum CSV separately, as the distributable archive deliberately excludes the source CSV because its redistribution licence is unresolved. Keys and local environments are excluded.

Rendered-page comparison reuses prior inspection only for byte-identical page images. Changed pages are inspected again; contents page numbers remain checked against the final rendering. The viva's native charts and original workbook parts are preserved. Neither the Word document nor the slides have been certified in the author's native Microsoft Office installation.

Use `submission/Kushal_Krishnamurthy_Dissertation.docx`, `submission/Kushal_Krishnamurthy_Viva.pptx` and `submission/Thesis_Project_Submission.zip`. Root-level convenience copies are synchronized with the current Office files after preserving the older copies. See [Submission_Verification.json](Submission_Verification.json) for final hashes and exact verification scope.

## What deserves attention before upload

Complete the personal fields and verify the actual Canvas/declaration/word-count rules. Read the corrected source-premise example and the semantic counterexample closely enough to explain them without relying on the slides. Rehearse the ten-minute presentation and the separate Q&A. A small related-work/gap addition, backup evidence and optional bibliography completion would strengthen presentation; another large feature or paid experiment is not needed to repair the findings from this audit.

The defensible conclusion remains that structured instructions improved unsupported-answer handling on this experiment, while receipt consistency did not ensure semantic correctness and incremental validator effectiveness was not established.
