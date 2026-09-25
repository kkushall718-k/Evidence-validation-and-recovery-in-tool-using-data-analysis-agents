# Historical annotation authoring evidence

These files preserve the original AI-assisted authoring workflow. The two Python sources have a `.py.txt` suffix intentionally: they are inert historical evidence, not current evaluation commands. Do not run them against the live project. The version-1 helper would overwrite current labels, and its current rubric lookup would no longer identify the original rubric. The correction script requires version-1 input and is also historical.

The inventory records 198 final explanations; the signature mapping contains 55 distinct tool/argument patterns. The version-1 helper encodes fixed exceptions and specialised rules. Its record list was compared, with its write step disabled, against the archived version-1 annotations and matched exactly. This proves materialisation consistency, not independent semantic validity. The complete interactive Codex instructions and evaluator model settings were not retained.

Use the current `scripts/trace_review_analysis.py` for analysis of version-2 annotations. See `documentation/Trace_Review_Provenance.md` for the methodological disclosure and `documentation/Source_Description_Correction.md` for the correction. The original file bytes were copied without modification; the following hashes identify them.

- `record_annotations_v1.py.txt`: `9464efd23d59f1c6ad8c49c16575a74d19687d652014b1a9075a3534a3d6a8f2`
- `trace_inventory_v1.jsonl`: `04a90a35fa65f5369b3897b6b8d5102fd1559e7c83bc7008a392670be04c62fc`
- `tool_signatures_v1.json`: `ca9f0f5e2f1d008cbdc76dd5f8ce0362fb40d41397349c08e30be2a8291ea414`
- `apply_annotation_correction_v2.py.txt`: `53bf3b610fa9790ade82844012b823745faeb470f46cd717e5f8e6651cda88d8`
