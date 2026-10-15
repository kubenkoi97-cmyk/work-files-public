# MIXED Stage 13 — re-audit + 39 field corrections
Date 2026-10-15. **PARTIAL; NOT READY FOR PRODUCTION IMPORT.**

## Verified patches
- **38 blank Series fields restored** from the exact product's original technical description and linked family manuals: Kentatsu KLA HFAN1 AC (6), KLA HZAN1 DC (6), KTA (6); Midea MIH-B V8 (8), MIH-Q2 V8 (6), MIH-Q4 V8 (2), V8 T1 (4).
- **Midea MI2-100Q4DHN18(At) heating = 11.2 kW**, corroborated across exact Russian catalog pages:
  - https://brand-climat.ru/midea-mi2-100q4dhn18-at
  - https://mircli.ru/Midea-MI2-100Q4DHN18-At-T-MBQ4-01F/
- Original product line order and output 356 rows × 77 columns unchanged.

## Critical applicability correction
Eight floor/ceiling Kentatsu models **KCA50/60/72/80/90/115/125/140HZAN1** had been wrongly counted in QA10 as requiring `Макс. напор, Па`. Per user configuration this applies to **duct units only**, not floor-ceiling type. These eight cells were left BLANK and removed from the "mandatory applicable missing" count. `QA13 не применимо` tracks every model and rationale.

## Current open core-field audit
Count: **925**, down from stage12 initial **972** = 39 true field fills + 8 false-positive mandatory flags removed. This count is the **core applicability-aware checklist**, **not complete coverage of all 77 columns**.

| Remaining required field category | Missing |
|---|---:|
| OEM warranty months | 341 |
| Exact model technical documentation | 241 |
| Refrigerant | 135 |
| Liquid/gas pipe diameters | 104 |
| Cassette panel dimensions | 37 |
| Series | 30 |
| Unit net weight | 20 |
| Unit width, height, depth and combined dimensions | 4 each |
| Cooling-mode electric input | 1 |

## Open conflicts and quality barriers
- Midea international vs Russian MI2 model code collision including Q4C and Q4. Must use Russian exact model/edition for capacity.
- MIH160Q4HN18/MIH180Q4HN18 cassette panel thickness 55 mm vs 65 mm in two manufacturer-source versions; do not fill till revision determined.
- Daikin FXMQ200A/250A power/size/mass differ between regional catalogs; don't overwrite existing values blindly.
- Kentatsu KTGB18HZBN1 refrigerant gas line 9.52 vs 12.7 mm conflict.
- IGC IMS-BS45NH(DC) unit-vs-package dimensions conflict.
- Full priority-site deep exploration by model and independently documented web-pass for 77 applicable columns remain **OPEN**. Existing product data and PDF links may be indexed not visually audited; don't claim final.

## Files and resumption
- ChatGPT workbook: `MIXED_356_77cols_STAGE13_LONG_SESSION_2026-10-15.xlsx` (binary upload to GitHub **not confirmed**).
- ChatGPT CSVs: `MIXED_STAGE13_AUDIT_356.csv` and `MIXED_STAGE13_OPEN_925_FIELDS.csv`.
- [Stage13 full 39-field patch](STAGE13_39_FIELD_PATCH.csv).
- [Prior stage11](STAGE11_CHECKPOINT.md), [stage12](STAGE12_CHECKPOINT.md).
- To resume: re-open chat XLSX or reconstruct from previous stage10 XLSX plus the linked patches; check 356×77, confirm open 925 core fields, process model-specific high-priority gaps (pipes 104, refrigerant 135, panel 37), refresh 356-model QA, publish GitHub patch/checkpoint immediately after every batch.
