# MIXED Stage 41 — Daikin exact-model OEM review
Date: 2026-10-16. Status: **INTERMEDIATE — NOT FOR IMPORT**.

## Baseline and invariants
- Baseline: [Stage 39 XLSX](https://github.com/kubenkoi97-cmyk/work-files-public/blob/main/climate-mixed/2026-10-15/MIXED_356_77cols_STAGE39_MIDEA_DEEP_QA_2026-10-15.xlsx), 483,530 bytes, SHA256 `ed5918460aa74738c225fd15cc8b8426261ae0fea08bbb6053a951bc78c187d1`.
- Stage 40 was source/warranty quality-only, with no numerical changes.
- 356 scoped models / 77 output columns; 388 out-of-scope products untouched.
- Stage 41 local full workbook `MIXED_356_77cols_STAGE41_DAIKIN_OEM_QA_2026-10-16.xlsx`: 506,886 bytes, SHA256 `328be7bfa1e203c759669e7a244e13555d79684112dc370d747caa8e232b8040`. **This binary XLSX was generated and verified as a conversation attachment; GitHub binary publication is NOT confirmed.** Do not claim the GitHub repository contains it.
- Full workbook cell-level regression: exactly **two** changes in the 356x77 output range (both formerly blank), **zero overwritten nonblank values**; appended dedicated QA, source and log entries; no formula-error tokens detected.

## Verified patch
| Excel row | Exact model | Column | Technical field | New | Basis |
|---:|---|---:|---|---:|---|
| 37 | Daikin FXKQ20A | 37 | Net unit mass, kg | 18 | Daikin factory FXKQ-A technical manual |
| 38 | Daikin FXKQ25A | 37 | Net unit mass, kg | 18 | Daikin factory FXKQ-A technical manual |

Factory PDF: https://easyspec.daikin.fr/EasySpec/VRV/Documentations/UI/J4_FXKQ-A/Manuel%20technique/ManTech_J4_FXKQ-A.pdf ; model-specific weight table verified visually on PDF pages 4–5. 
Official Daikin product tables: https://www.daikin.eu/en_us/products/product.table.html/FXKQ-A.html and https://www.daikin-belarus.by/ru_ru/products/product.table.html/FXKQ-A.html .
**Unresolved conflict**: a dealer describes FXKQ25A as 17 kg (https://www.breeze24.com/Daikin-1-Wege-Deckenkassette-FXKQ25A-Blende-BYK32G-VRV-Raumgroesse-25-30-m-28-kW). OEM value 18 kg is preferred for this model/series, but Russian market edition/actual imported variant should be verified before production; both variants remain documented. No panel weight substituted.

Two exact delta rows: [STAGE41_EXACT_FIELD_PATCH.csv](STAGE41_EXACT_FIELD_PATCH.csv). In the Stage41 XLSX the entries are also in source, Log, and QA sheets.

## Measured remaining basic fields
Stage 39: 625 -> Stage 41: **623** unresolved *basic applicable* fields, as observed in actual blank output cells:
- Manufacturer warranty: 341
- Exact model technical documentation: 114
- Refrigerant: 63
- Refrigerant pipe pair: 66
- Decorative panel dimensions: 20
- Net weight: 3
- Component dimension fields: 16
- Nominal electric input: 0
Total = 623. This is not the total of every conditionally applicable field among all 77 columns.

## Preservation of conflicts and next steps
- Midea `MI2-28/36/45/56/71T3DHN18(At)` and `MI2-80T2DHN18(At)`: R32 vs R410A conflict, open pending factory model/year/market documentation.
- Midea `MI2-45/90/140DLDHN18(At)`: conflicting R32/R410A vendor listings, open.
- Warranty blanks must NOT be filled by extrapolating a 60-month distributor warranty from a different suffix, model, or contractual coverage.
- Daikin `FXMQ200A`/`FXMQ250A`: different catalogue editions/markets conflict; no automatic replacements.
- IGC `IMS-BS45NH(DC)`: unit-vs-packaging size ambiguity remains open, no insertion.
- Continue exact-model FILE -> WEB pass: inspect supplied priority domains and manufacturer documentation, handle all 77 conditional fields, record failed attempts and last checked source; verify old filled values and per-model applicability.
- Never infer from adjacent models/related SKU suffixes; no final site import until comprehensive row-by-row QA.

## Audit trail
This is a genuine verified two-cell continuation, not completion of all 356 model web checks. The generated full Stage41 XLSX is downloadable from the conversation; its binary GitHub publication is still an open delivery action. Preserve Stage39 historical file unchanged.
