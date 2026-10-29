# MIXED — Stage 112 / third batch products 101–150 (2026-10-29)

## Current verified full working baseline
- **[Download full Stage112 XLSX](MIXED_356_77cols_STAGE112_THIRD50_101-150_SERIES_NORMALIZED_2026-10-29.xlsx)** — 1,112,548 bytes; SHA256 `18c9cfc70a12c9e907701e098a602a64e256cbdbc287665cd3c4a6c982e710fd`; Git blob SHA `c8647ae8a099e56904a43a44f555227dbd8fbefc` (binary file actually committed and tree entry verified).
- Previous Stage111 baseline SHA256 `ea181eb7b0afccbd130da64943b7aba5b982b168945614b81fce1dffabd16fae`.
- 356 products x 77 columns; 80 original sheets; 306 protected products unchanged.
- Working batch 101–150 (Excel rows 102–151): 1,608 of 3,850 nonempty cells (41.77%); this stage fixes existing metadata, **not 35 additional fields**.

## Completed / backed by manufacturer taxonomy
- 7 KTYB product series K110:K116: `DX PRO VII` → `KTYB`.
- 6 KTDB product series K117:K122: `DX PRO VII` → `KTDB`.
- 12 KTVB product series K130:K141: `KTVB (DX PRO VII)` → `KTVB`.
- 10 KTLB product series K142:K151: `Kentatsu KTLB / DX PRO VII` → `KTLB`.
- 15 KTGB/KTZB product series were already correct, unchanged.
- Manufacturer 2025/2026 product taxonomy: https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf . Correct distinct series; DX PRO VII remains the product family in descriptions, not the series property.

## Regression QA and exact patch
- Exactly 35 allowed cells changed: column K of the named target rows; 0 other product cell changes.
- Existing formulas unchanged; all 79 other original worksheet XML parts byte-identical; names/order and 80 sheets preserved.
- [QA JSON](STAGE112_THIRD50_QA.json) | [35-cell exact patch](STAGE112_THIRD50_SERIES_PATCH.csv).

## Unresolved / no invented specifications
- **0/50 ready for CMS import**. Commercial values are unverified placeholders (quantity AU100, buy AV0, retail AX0) on every model. GTIN, price, stock, warranty, images need verified owner/CMS sources.
- Old noise scalar U mixes MIN for 27 products and MAX for 23; exact dual values are tracked in [Stage110 noise audit](STAGE110_THIRD50_NOISE_SEMANTICS.csv), pending CMS field semantic definition. No automatic conversion.
- 8 historic disagreements on area/warranty remain unresolved; no unsubstantiated N area, M inverter flag, BU current or package claims added.
- Publisher PDF too large for web screenshot; text search confirms exact series names but independent original-page visual QA remains OPEN.
- Scope lock: never edit 306 products outside rows 102–151.

Next: model-specific OEM table verification and commercial owner data; keep Stage112 as the single current full XLSX.
