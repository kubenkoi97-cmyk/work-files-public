# Stage 11 — IGC / Daikin / Bosch — 2026-10-15

**STATUS: INTERMEDIATE — FACTUAL COMPLETENESS AND FINAL WEB PASS OPEN.**

- Input: stage 10 workbook; kept 356 models and 77 target columns, prior patches intact.
- 69 formerly blank fields filled with exact-model related source references. Breakdown: **IGC 53**, **Daikin 10**, **Bosch 6**.
- IGC: 35 catalog PDF links taken from original exact-SKU source rows (manufacturer's multi-model specification or relevant exact SKU PDF), 6 confirmed J, 3 confirmed Y, 7 Q-type, 2 BH nomenclature; no assumed refrigerant added.
- Daikin: 6 FXKQ-A model-series names; two FXMQ-A model-series names plus 2 factory catalog links.
- Bosch MDCI 12-1: outdoor dimensions **900×1327×400 mm**, refrigerant liquid/gas piping **9,52/15,9 mm**, original Bosch Air Flux catalog link, supported by exact-model trade product card and manufacturer model list. The discrepancy in Bosch cooling/heating capacity between regions is NOT resolved and existing entries NOT overwritten.
- Crucial conflict: **FXMQ200A/FXMQ250A** have significantly different consumption, dimensions, net weight between regional Daikin catalogs. Daikin Russian catalog page 69 (printed 68) was **visually reviewed**. Original workbook numeric specifications NOT changed without reconciling catalog market/edition.
- **IGC PDFs: indexed tables and user-upload references checked, but browser PDF rendering not accessible for full visual examination**. Link addition is not a claim of a fully audited manual.

Artifacts:
- Chat Excel: `MIXED_356_77cols_STAGE11_IGC_DAIKIN_BOSCH_2026-10-15.xlsx`.
- [Every changed field (69 rows)](STAGE11_69_FIELD_PATCH.csv).
- XLSX **not uploaded to GitHub**: this checkpoint plus patch log provide recovery data.

**NEXT**: second batch Kentatsu/Midea unresolved equipment-specific panel/refrigerant data; rerun global 356-model applicable field audit and update exception log. Do not call this final.
