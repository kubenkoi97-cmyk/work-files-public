# MIXED Stage55 — full 356 × 77 field-applicability and regression QA (2026-10-19)

**Status: INTERMEDIATE. NOT READY FOR PRODUCTION IMPORT.**

## Current actual workbook
- New complete binary **`MIXED_356_77cols_STAGE55_REAUDIT_356x77_2026-10-19.xlsx`**, 423302 bytes, SHA256 **`83c1e0414c75af3b38d766e9434bc80a9433fa8f64c96a0c3b1fc7b434ab6bcf`**.
- 356 original product records, 77 exact ordered headers, 17 sheets. Parent Stage54, same product-data values; Stage55 adds two independently generated QA sheets: `QA55 аудит 356` and `QA55 аудит 77`. Reopened exported Stage55 and verified all 356×77 product cells bytewise-equivalent in value to Stage54. No new technical values or commercial fields changed at Stage55.
- Compare Stage51 baseline → Stage55: **exactly 31 changes** (column62 heat exchanger =23, column68 installation type =8), **all previously blank** and none previously nonempty overwritten. Model identities and original output field sequence unchanged. Original source text and append-only `Источники` and `Log` retained in Excel; historical Stage47 (47-sheet full archive) and Stage51 checkpoint remain intact.

## Core vs conditional and applicability
- Previous original **613 CORE applicable blank cells** were individually checked against current Stage55 XLSX and all **613 remain physically empty**.
- Their statuses are 610 `OPEN_CORE_APPLICABLE` + 2 `OPEN_CORE_WITH_CONFLICT` (KZA mass) + 1 `OPEN_CORE_REFRIGERANT_CONFLICT` (Midea T2). The separate risky *already populated* fields (Midea R32/R410A, KZA gas/heat/weight, KTGB18 pipes, Daikin mass, KTLV15 heating) must NOT disappear from QA merely because they are nonblank.
- Additional **8,957 physically blank cells** are `OPEN_CONDITIONAL_APPLICABILITY_OR_SOURCE`: **NOT 8,957 confirmed missing technical fields**. The figure includes optional, blank commercial/service fields and fields not individually classified, and is an upper bound requiring field-by-SKU investigation. Do not equate a blank service ID or price sorting field with a missing HVAC parameter.
- **7,228 physically blank cells** provisionally classified as evidently not applicable **by equipment class** (hydronic pressure, water inlet/outlet, compressors for 355 indoor units, cassette panels for non-cassettes, duct static pressure for non-duct units, indoor-vs-outdoor-only dimensions). This is a *mechanical preliminary classification only*: verify on actual product/model documentation before final N/A.
- Unconditional existing filled fields remain **10,614** across 27,412 product field positions; this **does not mean all 10,614 are technically verified**. Need targeted second-pass source audits.
- New all-SKU audits: local full-detail 27,412-row `STAGE55_DETAIL_356x77.csv` (~6 MB), 356-model and 77-field summaries, 31-change regression CSV. Local files attached in this chat, not published to GitHub as binaries by the available connector.
- The GitHub summaries `STAGE55_356_MODEL_COVERAGE.csv` and `STAGE55_77_COLUMN_COVERAGE.csv` reflect actual stage-to-stage filled/blank counts, while detailed applicability statuses live in local full-detail CSV and QA55 sheets. They should not be misrepresented as visually verified manufacturer research.

## Three-stage session 52–54
- Stage52: 14 exact Midea MIH-GHN18(DP) / MIH-BHN18 coil entries from original FILE model engineering text, source and PDF verification status recorded. Conditional exchanger filled18→32.
- Stage53: eight exact Midea MI2-DLDHN18(At) installation modes `под потолком или у пола`, directly from exact source rows. Installation field filled63→71.
- Stage54: nine Kentatsu KTGB C-shape exchanger values from nine exact original FILE descriptions; exact web card [KTGB90](https://mircli.ru/Kentatsu-KTGB90HZBN1/) independently confirms C-type, rest still OEM pending. Conditional exchanger now 41.
- **TOTAL: 31 formerly empty conditional technical cells filled; zero prior nonempty overwrites.** No falsely closed critical source conflict.
- No generic seller warranty, unqualified R410A/R32 split, ambiguous bundle weights or different regional models were used for arbitrary edits. Two Daichi PDF links were not accessible (timeout), so never mark them `OEM_PAGE_VERIFIED`.

## Remaining critical search / validation queue
1. KZA30 gas tube **12.7 vs 9.52 mm** and KZA30/KZA40 mass/airflow/heating from different manufacturer catalog editions. Identify actual supplier edition and serial context before import.
2. Nine Midea ATOM B refrigerant R32/R410A conflicts (some stored values nonblank) and MI2-80T2 blank; keep import block.
3. 64 CORE refrigerant pipe pairs and 63 refrigerants, exact `(At)` / `(DP)` / `HZBN1` code + Russian manufacturer manual visual checking. Do not infer from neighbor.
4. 20 panels (exact interior unit → exact compatible panel → dimensions); 3 indoor masses (two KZA conflict, one MI2-22Q1 10kg unit vs 12kg bundled), 16 dimension parts, 106 exact model technical documents, 341 OEM guarantee statements.
5. Continue all conditional field-scope verification (esp 57–77), and revisit currently populated potentially wrong values; record domain/search status per model and register unresolved evidence.
6. Re-run all 356×77 and field-level old→new diff after each actual workbook patch. Preserve historical archives and prior GitHub records.

**GitHub publication limitation:** Current true Stage55 binary is attached in ChatGPT; available GitHub connector does not ingest local container binary. The GitHub repo receives audit/patch/checkpoint as plain-text files. Do not claim remote XLSX is published or that archive has been deleted.
