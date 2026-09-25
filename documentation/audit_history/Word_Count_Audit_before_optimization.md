# Dissertation word count audit

23 September 2026. This recount applies to the current canonical `Kushal_Krishnamurthy_Dissertation.docx`, SHA-256 `bae286cf616097b4a3b22b15586277ae441efaece5f404fe55e0162fa7db94cf`. The identical outer-folder convenience copy and the DOCX inside the submission ZIP have the same text.

**The report of more than 15,000 words is correct for the complete document.** The previously quoted 12,000 is a custom count of Chapters 1–7, not a full-document Microsoft Word count. A separate editor check also shows that the custom main-text count is not identical to an editor's count. Word-limit compliance is therefore **unconfirmed**, pending the institution's counted-section rule and its accepted electronic counting method.

## Independent recount of the actual DOCX

| Counted scope | Project's documented alphanumeric-token count | Simple whitespace count | LibreOffice Writer count |
|---|---:|---:|---:|
| Main chapters 1–7, including their headings, tables and captions | 12,000 | 12,010 | 12,018 |
| Complete document body, including preliminary pages, references and appendices | 15,492 | 15,502 | 15,520 |
| Full editor document including running header/footer content | Not used by project counter | Not used by project counter | 15,525 |

The ten-token difference between the project's two token counts is exactly ten standalone `/` symbols in tables. That explains the earlier 12,010 observation; it does **not** explain away the more-than-15,000 full-document count. The extra body material contributes 3,492 tokens under the project method. The editor applies its own word-boundary rules, so the project's count must not be presented as the native Microsoft Word result.

The five-word difference between the editor's full-document and body-only checks is running header/footer content. These checks used the bundled LibreOffice Writer build, not Microsoft Word. No exact Microsoft Word count is claimed. The original DOCX was not changed or saved through LibreOffice; conversion and selection files remained in the private working directory.

## Where the additional words are

This breakdown uses the project's documented alphanumeric-token method consistently. Each heading is included in its section; the contents page includes the displayed headings and page numbers.

| Section | Words |
|---|---:|
| Title page | 66 |
| Abstract | 271 |
| Statement of AI assistance | 107 |
| Contents | 399 |
| Chapter 1 Introduction | 1,044 |
| Chapter 2 Foundations | 1,217 |
| Chapter 3 Related work | 1,785 |
| Chapter 4 System design and research method | 3,067 |
| Chapter 5 Results | 2,460 |
| Chapter 6 Discussion | 1,802 |
| Chapter 7 Conclusion | 625 |
| References | 726 |
| Appendix A Complete prompts | 427 |
| Appendix B Question inventory | 484 |
| Appendix C Reproduction and artifacts | 237 |
| Appendix D Supplementary assessment rubric | 775 |
| **Complete document body** | **15,492** |

Thus the main chapters are 12,000; preliminary material is 843; references are 726; appendices are 1,923. The complete body is **12,000 + 843 + 726 + 1,923 = 15,492**. The main-chapter count includes in-text citations, main-text tables and figure captions. Text contained inside raster images is not extracted as body text. No footnote, endnote or comment parts were found in the current DOCX.

## What the supplied handbook establishes

The supplied Dissertation Module Handbook, page 4, specifies **12k words (50 pages)** for one M598 student. It states a penalty of one mark per started 100 words above or below the stated limit, capped at ten marks, and refers to an electronic word count. It does not explicitly define whether the abstract, contents, references, appendices, headings, tables or captions are excluded. It does not grant a general ten-percent tolerance in that passage.

Consequently, there is no basis in the supplied handbook for certifying that the entire 15,000-plus-word file is acceptable merely because its main chapters meet a custom 12,000 count. Equally, there is no basis for deleting required supplementary evidence before establishing whether it counts. Older third-party handbook copies or another university's conventions do not settle this submission's rule.

The current dissertation remains 51 pages in the previously verified full rendering. The word-count-only ODT conversions were not used to assess page count or layout.

## Required resolution

1. Obtain the current counted-section rule from Canvas, the assessment instructions or the supervisor. A clarification was requested during this recount because the supplied handbook does not resolve the exclusions.
2. Check the permitted selection in **desktop Microsoft Word**, if that is the accepted counter, using the actual current DOCX. Microsoft documents that selecting text gives a count for that selection as well as the whole document: [Show word count](https://support.microsoft.com/en-us/word/training/show-word-count).
3. Revise according to that rule. If only Chapters 1–7 count, the current LibreOffice measurement is **18 words over**, so at least a small correction is needed under that counting method; the final Microsoft Word selection count still needs checking. If all material counts, the current full-editor count is **3,525 words over**, requiring substantive shortening. These are scenarios under the stated methods, not assumed university decisions.
4. Update the title-page declaration to the accepted count and scope, then regenerate and recheck the document. Do not silently change the counter, remove required references, or assume appendices are excluded to make the displayed number fit.

No dissertation prose, citations, experimental records, annotations or numerical results were changed during this recount. The supporting audit and readiness records are updated so the outstanding word-limit question is visible.

## Reproduction

Run `python scripts/count_dissertation_words.py` for a read-only section recount directly from the DOCX. It concatenates formatting runs without inserting artificial spaces, includes table cells once in document order, and reads displayed contents text while excluding field instructions, running headers/footers and image alt text. It does not emulate Word's internal tokenizer or define institutional policy.

`documentation/Word_Count_Audit.json` retains the section counts, original DOCX checksum, editor counts, editor version and hashes of the temporary ODT conversions. The original DOCX metadata contains a stale zero word-count field and was not used as evidence. The independent editor counts came from statistics recalculated during conversion, including separate temporary main-only and full-body-only documents. No API requests or external file uploads were made.
