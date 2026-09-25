# Whole-document word-count audit

Updated 23 September 2026 (local time), after the author confirmed that **everything counts**.

The revised dissertation measures **12,000 words in LibreOffice Writer's complete-document count**, down from **15,525**, a reduction of **3,525 words (22.7%)** under the same editor method. The final rendering contains **47 pages**, down from 51, including preliminary pages, references and appendices. The title page now declares a complete-document count instead of a main-chapter subtotal.

The actual DOCX was converted to a temporary ODT in an isolated LibreOffice profile; the editor recalculated its statistics. No sections were selected or excluded. The original DOCX checksum was unchanged by verification. The conversion statistic, editor build and checksum are recorded in `Word_Count_Audit.json`.

## Scope and counter

The count includes the title page, abstract, AI declaration, contents, seven chapters, headings, tables, captions, all twenty references, and four appendices. Running headers and footers are handled by the editor. Its word counter does not OCR text embedded in raster figures or multiply a running header by every printed repetition. The three existing figures were preserved; no prose was converted to images to reduce the count.

This is a **native LibreOffice count, not a verified native Microsoft Word count**. Different editors can tokenize numbers, compounds, symbols and fields differently. The author's all-sections instruction resolves the earlier scope uncertainty; it does not make different software counters identical. Recount the completed upload file in the institution's accepted editor after filling the four personal-detail placeholders and refreshing fields. Adjust the declaration if that final count changes.

The supplied handbook specifies 12,000 words and a 50-page maximum for this route, with under/over-length penalties and no general ten-percent allowance. The current 47-page rendering is below 50 even with all preliminary and appendix pages included. The word target is met by the documented editor measurement; this is not a grade or institutional acceptance guarantee.

## What was shortened

Repeated explanations across the introduction, foundations, literature, results and discussion were consolidated. The essential research questions, implementation, experimental design, operational metric definitions, statistical qualifications, semantic counterexample and recent review disclosures remain. All six main tables retain identical cells. The complete bibliography remains unchanged and each of its twenty entries remains cited.

The appendices now give concise specifications and reproduction directions. Complete prompts, validator feedback and exact question wording are preserved in `documentation/Complete_Experimental_Materials.md`, alongside the original configuration and frozen source in the supporting ZIP. Appendix D still states the exploratory rubric, denominators and limitations; the complete rubric remains in `documentation/TRACE_REVIEW_RUBRIC.md`. The dissertation retains the material necessary to assess the method and results; the companion provides detailed implementation evidence.

All 198 experimental runs, collected traces, prompts, runtime, protocol, annotations, numerical outputs and notebook were preserved. Checksums of 308 frozen evidence files matched before and after this edit. No model observations, scores or citations were invented or removed to meet the target.

## Section cross-check

The following explicit alphanumeric-token counts are diagnostic subtotals, **not the editor's native count**. They concatenate formatting runs and count table cells once. Their full-body total is 11,966; including punctuation-only tokens gives 11,976. They exclude headers/footers and use a different tokenizer, explaining why they do not total 12,000. The seven-chapter subtotal is 9,715, and is no longer used as the submission declaration.

| Section | Diagnostic words |
|---|---:|
| Title page | 70 |
| Abstract | 213 |
| Statement of AI assistance | 107 |
| Contents | 348 |
| 1 Introduction | 754 |
| 2 Foundations | 880 |
| 3 Related work | 1,440 |
| 4 System design and research method | 2,836 |
| 5 Results | 2,209 |
| 6 Discussion | 1,200 |
| 7 Conclusion | 396 |
| References | 726 |
| Appendix A Prompt specification | 94 |
| Appendix B Question specification | 91 |
| Appendix C Reproduction and artifacts | 159 |
| Appendix D Supplementary assessment rubric | 443 |

## Verification and repeatability

All 47 rendered pages were visually inspected. All 59 contents entries were checked against their rendered destinations. Seven numbered tables and three numbered figures remain; six main tables match the previous DOCX cell for cell. There are no tracked insertions/deletions or comment ranges in the delivered document.

Run `python scripts/count_dissertation_words.py` for the diagnostic section counts. Run the following for a fresh complete-document LibreOffice verification, substituting the local executable path:

```bash
python scripts/verify_document_word_count.py --office /path/to/soffice --expected 12000
```

The verifier returns the source checksum, editor build, actual count and whether it matches the target; it leaves the original DOCX unchanged. The title-page number is a declaration, not an automatically updated field, so the independent recount is required after edits. The historical recount is retained in `documentation/audit_history/Word_Count_Audit_before_optimization.*` and is explicitly superseded by this report.

Current DOCX SHA-256: `4159bf68338bf1de28306d965ef33ef55c7cbdf1a88d49e3e5111565f5021f07`.
