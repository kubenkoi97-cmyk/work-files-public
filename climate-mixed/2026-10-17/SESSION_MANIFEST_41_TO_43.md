# SESSION MANIFEST — MIXED stages 41–43 (17 October 2026)
**Current active file: STAGE43 (binary XLSX created locally; not verified on GitHub).**
Do not treat this catalog as final/import-ready.

## Provenance and checkpoint chain
1. Stage39 verified published, original baseline: [binary XLSX](../2026-10-15/MIXED_356_77cols_STAGE39_MIDEA_DEEP_QA_2026-10-15.xlsx). 356 models ×77 columns; 625 open core applicable blanks.
2. Stage40: source/warranty standards audit only, no changes in output.
3. Stage41: FXKQ20A / FXKQ25A two previously blank net unit weights filled as 18 kg from Daikin EEDEN241 technical data; core 625 ->623. Local XLSX `MIXED_356_77cols_STAGE41_DAIKIN_OEM_QA_2026-10-16.xlsx` (506886 bytes; sha256 `328be7bfa1e203c759669e7a244e13555d79684112dc370d747caa8e232b8040`). [Stage41 report](../2026-10-16/STAGE41_CHECKPOINT.md).
4. Stage42: eight exact Kentatsu KTGV18/24/30/40/50/60/72/80HZBN1 technical catalogue links added in previously empty `TECH_DOCUMENTATION` column 43. 623 ->615. PDF text indexing confirms exact models; large-document page visual QA pending. Local XLSX `MIXED_356_77cols_STAGE42_KENTATSU_KTGV_DOC_QA_2026-10-17.xlsx` (530361 bytes; sha256 `c5ef0d54aadd3ef7d5735668adfc881d38c51f6e7d0c6ff49953714e786047ff`). [Stage42 report](STAGE42_CHECKPOINT.md); [exact 8 field patch](STAGE42_EXACT_MODEL_DOC_PATCH.csv).
5. Stage43 **current active**: no value updates, only highlighting of conflicting cells, 11-model QA tab, new source/log entries, full QA open, per-model, per-column review. Local XLSX `MIXED_356_77cols_STAGE43_REFRIGERANT_REVISION_CONFLICT_QA_2026-10-17.xlsx` (555300 bytes; sha256 `eef2987a6e4bb6bd0fc8779029ef647a571bf82bad5081af06626da378d4409b`). [Stage43 report](STAGE43_CHECKPOINT.md); [11 open conflicts](STAGE43_CONFLICT_QA_11_MODELS.csv).

**Only text CSV and markdown checkpoints verified published in public GitHub; Stage41–43 binaries exist as chat attachments, NOT verified on GitHub.** Do not replace Stage39 binary or claim otherwise. Preserve historical copies.

## Latest QA exports in public repository
- [615 exact pending core fields](STAGE43_OPEN_615.csv)
- [356-model row-by-row audit](STAGE43_AUDIT_356.csv)
- [77-column raw coverage audit](STAGE43_77_COVERAGE.csv)
- [11 high-impact conflicts (Daikin 2 + Midea 9)](STAGE43_CONFLICT_QA_11_MODELS.csv)
- [Latest checkpoint](STAGE43_CHECKPOINT.md)

## Fixed scope, invariants and status
- 744 original products, 356 selected where description and characteristics both populated, remaining 388 ignored.
- Brand distribution: Kentatsu 213; Midea 99; IGC 35; Daikin 8; Bosch 1.
- 77 columns exact order; no row reorder, duplicate SKU substitution, invented values or vendor prices.
- Stage42 regression exactly 8 formerly blank cells populated, no other output changes. Stage43 output values identical to Stage42, formatting highlights only. XLSX valid ZIP: CRC check passed; 39 ZIP members; no formula-error tokens in previous Stage42 output and no changes to those values.
- **615 base applicable blanks**: warranty 341, exact technical docs 106, refrigerant 63, pipe pairs 66, panel dimensions 20, unit net weight 3, four units ×4 component dimensions = 16; nominal electrical input 0. **Sum: 615**.
- These counts are not all applicable gaps in all conditional 77 fields. E.g. raw raw-fill audit shows some 77 columns all empty but may be intentionally not applicable or source-restricted; do not falsely treat all blank cells as defect.
- Import BLOCKED on 11 highlighted source conflicts (Daikin 2, Midea 9). Exact manufacturer's market/year document needed.

## Mandatory next work packages
A. Reconcile Daikin 18 kg technical EEDEN241 (2024) vs Daikin Austria 2026 catalog 17 kg for `FXKQ20A`, `FXKQ25A`. Preserve both, verify regional and revision variants; no forced overwrite.
B. Resolve Midea nine R32/R410A conflicts by exact Russian VRF outdoor pairing, model suffix and manufacturer's dated PDF. Seller voting and broad certificates are inadequate. Review conflicts in CSV; retain red/amber warnings.
C. Confirm technical document applicability/visual table for eight Stage42 Kentatsu model links, plus other 106 missing docs and 20 panel dimensions.
D. Verify 66 pipe pairs, 63 refrigerant blanks, three net mass, sixteen component dimensions; web-pass all user-priority sites and ≥5 additional available domains when needed, record last checked source.
E. Manufacturer warranty 341 empty: authenticate market-specific OEM terms, not reseller marketing.
F. Continue exhaustive 356×77 field-by-field applicability and WEB-pass; each change must include exact page URL, PDF page when possible, before/after, full QA regression and permanent stage checkpoint.

## Latest source evidence
- Daikin technical manual: https://easyspec.daikin.fr/EasySpec/VRV/Documentations/UI/J4_FXKQ-A/Manuel%20technique/ManTech_J4_FXKQ-A.pdf
- Daikin Austria 2026 conflicting catalog: https://www.daikin.at/content/dam/DACE-AT/document-library/catalogues/ac/vrv/Daikin_Katalog_VRV_2026.pdf
- Kentatsu KTGV exact technical table (indexed): https://www.c-o-k.ru/library/catalogs/kentatsu/37986/140011.pdf
- Midea 2026 RF declaration with distinct suffix X (not proof of refrigerant): https://xn----7sbajahheyaepn1ca0aveqcb0fxl.xn--p1acf/document/eaes-n-ru-d-cnra08v0854326/

## Upload status
Stage 41–43 binary XLSX still requires a means to upload true binary to GitHub without corrupting workbook. Text audit is fully published. Do not attempt to commit XLSX as UTF-8 text.
