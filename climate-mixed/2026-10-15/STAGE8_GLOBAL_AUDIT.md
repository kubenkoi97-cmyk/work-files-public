# STAGE 8 — COMPLETE ROW-WISE APPLICABILITY AUDIT (15 Oct 2026)

**Intermediate working workbook, not final/importable.**

## Scope
- **356 / 356** selected models rechecked in the resulting workbook (exact original product count preserved).
- All **77 header columns retained**; applicable HVAC technical columns distinguished from vendor metadata / fields for other product categories (hydronic, heat pump, etc.).
- **1132 blank applicable core field cells**, affecting 356 models. This number means **unconfirmed in the interim XLSX**, not provably unavailable and not confirmed web-searched.
- Separate worksheets created: `QA8 полнота 356` (one line for each model), `QA8 пропуски по полям` (one row per applicable missing field), `QA8 формат и риски` (format violations), with links to model rows and column numbers.
- **Zero format warnings** in the programmed checks (mode, inverter vocabulary, product-category role, pipe delimiter, HTML-structure, obvious panel/duct field misuse). This does **not** certify correctness of all data.
- Regression checks retained earlier confirmed IGC/Kentatsu/Daikin/Midea values. No original product rows removed or added.

## Missing, by applicable field (model count)
| Field | Missing |
|---|---:|
| Manufacturer warranty (months) | 341 |
| Exact model technical documentation | 318 |
| Refrigerant | 135 |
| Pipe sizes | 105 |
| Series | 94 |
| Cassette decorative panel dimensions | 43 |
| Indoor net weight | 36 |
| Heating capacity | 11 |
| Power supply | 10 |
| Airflow | 9 |
| Duct max external static pressure | 8 |
| Indoor width/height/depth/dimensions | 4 each |
| Noise | 1 |
| Input power | 1 |
| Bosch outdoor-only width/height/depth/dimensions | 1 each |

**Beware:** Model-specific compressor-inverter status is generally not a standalone property of an indoor unit. It was correctly left unforced; one outdoor Bosch model has the verified inverter field. The outsole Bosch model is excluded from `Тип внутреннего блока` and audited against outdoor dimensions. Marketing area/color/wifi and other conditional fields are tracked separately from fixed core counts.

## Current candidate priorities
1. Kentatsu KTGB18...KTGB90 — **nine** missing airflow values; check manufacturer's product tables, don't interpolate.
2. Kentatsu KGA24...KGA115 and Midea MI2-100Q4DHN18(At) — **11** heating capacities missing.
3. Daikin FXKQ32,40,50,63 and Kentatsu KLA24...KLA72 — **10** power supplies missing.
4. Midea MI2-22Q1DHN18(At) — input power and net weight still unconfirmed; do not borrow from the similar MDV/MIH variants.
5. Catalog-only specification gaps: refrigerant (135), piping (105), exact cassette panels (43).
6. Warranty and documentation require model-specific/region-specific evidence. A retailer warranty must not automatically be entered as an OEM warranty.
7. Previously documented Midea Q4C international-vs-Russian SKU power conflict remains **OPEN**.

## Status and artifacts
- Complete XLSX `MIXED_356_77cols_STAGE8_AUDIT_ALL_356_2026-10-15.xlsx` is attached in ChatGPT; binary GitHub publication not confirmed.
- Companion CSV `STAGE8_AUDIT_356.csv`, `STAGE8_MISSING_APPLICABLE_FIELDS.csv` produced as chat artifacts.
- This GitHub checkpoint preserves scope, calculations, model priorities, open risks and next action, **not** an assertion of a completed full web-pass.
- Continue model-specific WEB→FILE rechecking and periodically regenerate the same 356-model audit after corrections.
