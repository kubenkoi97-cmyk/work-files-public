# MIXED climate catalog — Stage 4 (2026-10-14)

**Status: PARTIAL QA — not ready for import.**

## Scope and verified counts
- Original scope: 356 selected products out of 744; other 388 not processed.
- This batch: **31 models** — Kentatsu KTGV (8), Kentatsu KTYV (7), Midea MI2-G/DP (16).
- **81 tracked field changes**: 77 initially empty fields filled, 4 existing values corrected.
- Product export still has 356 rows and exactly 77 columns.
- Workbook structure preserves the earlier IGC/Daikin work, adding Stage 4 model-by-model QA and a change history.
- No Excel formula error tokens found in the latest scan.

## Fields updated
- Color (21), area (15), series (12), electrical input (7), refrigerant (7), line diameters (6), net mass (6), airflow (3), maximum current (2), warranty (2).
- KTGV50HZBN1: 720 m³/h, 0.03 kW, 11.5 kg; technical product card independently found.
- KTGV72HZBN1: 1220 m³/h, 0.05 kW, piping 9.52/15.9 mm.
- KTYV18–72: exact product cards corroborate R410A and white case; cassette decoration panel size is **not** equated to body dimensions.
- Midea MI2-G and DP variants remain segregated. Variant-specific details are **not** transferred between base and DP unless directly supported.

## Key exact-model source examples
- https://mircli.ru/Kentatsu-KTGV18HZBN1/
- https://brand-climat.ru/kentatsu-ktgv24hzbn1
- https://brand-climat.ru/kentatsu-ktgv72hzbn1
- https://brand-climat.ru/kentatsu-ktyv18hzbn1
- https://brand-climat.ru/kentatsu-ktyv72hzbn1
- https://kondiair.ru/product/kentatsu-%D0%B4%D1%8D%D0%B8%D0%BA%D1%81-%D0%BF%D1%80%D0%BE-%D0%B1%D1%8D%D0%B9%D1%81%D0%B8%D0%BA-dx-pro-basic-ktgv-ktgv50hzbn1/
- https://mircli.ru/Midea-MI2-56GDHN18-At-/
- https://mircli.ru/Midea-MI2-45GDHN18-At-DP/
- https://air-midea.com/support/marketing/download/11964/

## Open QA gates
- 31 model audit rows explicitly list each main unresolved attribute.
- Exact-series technical documentation links in the target TECH_DOCUMENTATION column are not yet verified.
- KTGV24HZBN1 and KTGV80HZBN1 piping is still missing; KTYV24–72 piping and the separate panels also require confirmation.
- Warranty references may reflect different retailer policies. A seller warranty must not automatically be represented as manufacturer warranty.
- Individual priority domain coverage and full web-pass across all 77 applicable fields still pending. A missing field in this stage must **not** be interpreted as proven unavailable.
- **No final/complete claim.**

## Artifacts
- [31-model audit CSV](STAGE4_MODEL_AUDIT.csv) — independently published on GitHub.
- Full Excel working copy: `MIXED_356_77cols_STAGE4_KENTATSU_MIDEA_QA_2026-10-14.xlsx` — made available to the user in ChatGPT. This report does not claim that binary XLSX has been uploaded to GitHub.

## Next action
Continue exact-model search for every applicable empty field and every undecided conflict, with the prescribed domain-order and source-by-field log. Do not import the current intermediate file.
