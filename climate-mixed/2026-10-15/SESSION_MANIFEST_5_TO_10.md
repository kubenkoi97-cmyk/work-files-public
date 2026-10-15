# MIXED — 356 HVAC products / 77 columns — SESSION MANIFEST
Date: **2026-10-15**. Current stage **10**. **PARTIAL — NOT FIT FOR PRODUCTION IMPORT**.

## Nonnegotiable data contract
- Source workbook tab `MIXED — обработка`, exactly **744 original product rows**.
- Only **356 selected** rows with both `Описание товара` and `Характеристики` filled; **388 excluded**, untouched.
- Keep exactly 77 final output fields (user's attached 77-column reference overrides earlier 56-column standard); preserve order, values, model identities, parenthetical suffixes, SKUs and all previous audited data.
- MIXED FILE→WEB: exhaustive parsing of every source field first; exact-model manufacturer documentation plus web-pass per empty/uncertain/applicable field. No estimates and no value substitution from adjacent SKU or different country edition.
- Only fields applicable to equipment class must be present; e.g. cassette panel only for cassette; static pressure only for duct; outdoor dimensions only outdoor. Unconfirmed field must remain blank and tracked, never forcibly completed.
- Trace field-level source, version, conflicting evidence and audit status. HTML product description conforms to user's five-section, <br>, no <b>, no numeric specification lists.

## Completed checkpoints in this session
| Stage | Model passes | New exact-source fields | Checkpoint | Field patch |
|---|---:|---:|---|---|
| [5](STAGE5_CHECKPOINT.md) | 14 Kentatsu KTYB/KZTB | 42 | linked | [CSV](STAGE5_FIELD_CHANGES.csv) |
| [6](STAGE6_CHECKPOINT.md) | 19 Kentatsu KTVB + Midea Q4C | 43 | linked | [model audit CSV](STAGE6_MODEL_AUDIT.csv) |
| [7](STAGE7_CHECKPOINT.md) | 18 Kentatsu KTKB + Midea Q1 | 36 | linked | [CSV](STAGE7_FIELD_CHANGES.csv) |
| [8](STAGE8_GLOBAL_AUDIT.md) | All **356** core applicability audit | 0; global QA | linked | Chat CSV with 356 rows |
| [9](STAGE9_CHECKPOINT.md) | 19 Kentatsu KTGB/KGA | 48 | linked | [CSV](STAGE9_48_FIELD_CHANGES.csv) |
| [10](STAGE10_CHECKPOINT.md) | 12 Kentatsu KLA + Daikin FXKQ | 23 | linked | [CSV](STAGE10_FIELD_CHANGES.csv) |

**192 filled previously blank fields** this session. **82 model-check passes** across patch stages; not equivalent to 82 fully completed 77-field model audits. Every full-audit run covers the same 356 products. Model-exception counts: **1132 → 1084 → 1061** (stage8→stage9→stage10), independently regenerated after changes.

## Current latest workbook
`MIXED_356_77cols_STAGE10_KLA_DAIKIN_2026-10-15.xlsx` (approx. 584 kB, ChatGPT user downloadable, NOT uploaded as XLSX to GitHub). Includes all 356 rows, 77 columns, cumulative stage 1–10 results, QA sheets and latest 356-model applicability-aware audit and missing field worksheets.

Complementary chat files:
- `STAGE10_FIELD_CHANGES.csv`
- `STAGE10_GLOBAL_AUDIT_356.csv`
These exist in the chat; CSV partial checkpoints are independently published above.

## Stage10 live open-field counts — 1061
- Manufacturer warranty 341 (must distinguish seller vs OEM / Russian market).
- Exact-model tech documentation 287.
- Refrigerant 135.
- Refrigerant piping 105.
- Series 94.
- Cassette decorative panel 43.
- Net weight 26.
- Duct external static pressure 8.
- Four indoor models missing individual W/H/D/combined dimensions (4 each).
- Midea MI2-100Q4DHN18(At) heating capacity 1.
- Midea MI2-22Q1DHN18(At) electric input 1.
- Bosch MDCI 12-1 outdoor W/H/D/combined dimensions 1 each.
- Most voltage and noise category gaps from stage9 are **resolved**; do not undo.

## Explicit unresolved contradictions
1. **Midea MI2-Q4CDHN18(At)**: seven model codes collide between Russian and other Midea country catalogues; e.g. `MI2-15Q4CDHN18(At)` means 1.5 kW in Russia but 4.5 kW in a foreign-language catalog. Do not transfer cooling/heating, noise, refrigerant or mass from international list without factory proof of exact Russian market suffix. [Stage6 conflict](STAGE6_CHECKPOINT.md).
2. **Kentatsu KTGB18HZBN1**: gas-line size in Russian retailer card `6,35/9,52` vs 2025 factory catalogue `6,35/12,7`; preserve current and do not override until OEM clarification. [Stage9 conflict](STAGE9_CHECKPOINT.md).
3. **Daikin FXKQ-A**: catalog revisions disagree about some mass/airflow/consumption values; manufacturer documentation per revision needed. Other verified fixes (FXKQ-A R410A, FXKQ63A low noise 38.5 dBA) must remain.
4. **IGC IMS-BS45NH(DC)**: unclear body dimensions vs package dimensional conflict from earlier stages.

## Priority sites user requested
Common: mircli.ru, iclim.ru.
Kentatsu: kentatsu.group, kentatsu-kondicioner.ru, kentatsurussia.ru.
Midea: midearussia.ru, air-midea.com, midea-air.ru.
Daikin: daikin.com, daikinair.ru, daikin.ltd, daikin-russia.com, daikinofficial.com, daikin-online.ru, russia-daikin.com, informteh.ru.
Bosch: bosch-group.ru, bosch-centre.ru, russia-bosch.com.
IGC: igc.com.ru, vozduhoff.ru, fancoil-kkb.ru, clima-vent.com, informteh.ru, iclim.ru.
Search all requested priority sites appropriately per model, and additional authoritative sources as needed. Prior stage checks are NOT evidence every priority domain was opened deeply.

## Next batch workflow
1. Open the most recent stage10 XLSX, verify 356 rows, 77 fields, and contents of `QA10 полнота 356 текущая` plus `QA10 пробелы текущие`.
2. Choose model families by shared manufacturer technical catalogue and exact model suffix, prioritizing Midea Q4C conflicts, 43 panels, 105 piping, 135 refrigerants, then 287 technical docs; avoid manufactured warranty values.
3. Capture exact source URL and PDF edition per model and value, distinguishing body vs panel, indoor vs outdoor, cooling vs heating.
4. Record before/after field changes and valid source, check unrelated rows untouched, generate new checkpoint **and publish its Markdown+CSV to GitHub immediately** before the next batch.
5. After each several batches, rebuild 356-row applicability audit; compare missing counts and regressions, retain history.
6. Deliver the latest XLSX to user in ChatGPT and state clearly that GitHub checkpoint is *not* same as binary XLSX; don't pretend GitHub binary exists until verified.
