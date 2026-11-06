# MIXED — full 744-product consolidated catalog, 2026-11-07

## Deliverable
- File: `MIXED_FULL_744_STAGE113_MERGED_2026-11-07.xlsx`
- SHA-256: `11f42853e6e292dce465529f37e3389f050a516c7a8e5e6341cd7e9cc7965c98`
- Size: 1,604,452 bytes
- **Binary delivery:** generated as a ChatGPT downloadable file. **The XLSX binary has not been uploaded to GitHub**; do not treat this manifest as a binary download.

## Consolidation inputs
1. Full original 744-product workbook `MIXED_Термотрейд_IGC_этап41_MIH_Q4_T1_IGC_AHU_реаудит.xlsx` (2026-10-14).
2. Latest verified 356×77 workbook `MIXED_356_77cols_STAGE113_THIRD50_101-150_OEM_FEATURES_2026-10-30.xlsx`.

## Counts
- 744 original SKUs, five brands (Kentatsu 296, Midea 283, IGC 121, Daikin 32, Bosch 12).
- 356 selected in original MIXED branch, 388 deferred due to empty source descriptions and characteristics.
- Within selected 356: batches 1–50 and 51–100 administratively frozen, 101–150 Stage113 active, 151–356 prefilled but not deeply audited.
- All 744 output SKUs explicitly populated in the **new consolidated** catalog: 206 previously blank CML2_ARTICLE fields in selected products 151–356 were restored from matching same-row `Сбор данных!C`; 388 deferred SKUs came from original `Модель (поиск)`. The previous Stage113 sheet remains unchanged.

## Contents (86 sheets)
- Previous 80 sheets of Stage113 carried forward.
- `00 ОБЗОР 744`: summary, warnings and brand balance.
- `01 КАТАЛОГ 744`: 744 original-order records and 77 import-schema columns.
- `02 КОНТРОЛЬ 744`: provenance and status per original row.
- `03 SOURCE AB 744`: original full source description/characteristics and QA.
- `04 SOURCE CARD 744`: original 15-column raw catalog.
- `05 PATCH ARTICLES 206`: exact original-source article recovery audit.

## Validation
- Workbook ZIP integrity PASS.
- Exact source row mapping: 356/356 model and original-title matches; 388 deferred stay intact.
- 744/744 unique SKU codes in new combined sheet.
- All 356 technical rows copied from Stage113 except the explicitly logged 206 new **combined-sheet-only** article cells. No modification to original Stage113 356-row sheet.
- Original 744 A/B source and original 15-column source catalog preserved exactly in new raw sheets (normalized scalar values).
- No claim that filled fields are automatically OEM verified.
- **0 product groups certified READY_FOR_IMPORT**. Quantity/price placeholders, old original prices, images, manufacturer warranty and OEM edition checks remain blockers.

## Next
Use the new consolidated sheet for all-744 overview, but continue actual technical research on exact original Stage113 target scope 101–150 without editing frozen 306 historical product rows. Never infer specifications for deferred 388 products.
