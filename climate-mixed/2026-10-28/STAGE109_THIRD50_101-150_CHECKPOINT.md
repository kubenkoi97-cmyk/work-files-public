# MIXED Stage109 — THIRD50 101–150 — exact article restoration (2026-10-28)

## Canonical source
- Input: `MIXED_356_77cols_STAGE107_NEXT50_EXACT3_SYSTEM_INVERTER_COLOR_2026-10-27.xlsx`
- Original bytes: 1106927; SHA256 `0332af716d9284fdb270d01464e1aca65420fdd1ccff9900a9b0e2a9cadfec19`
- Output: `MIXED_356_77cols_STAGE109_THIRD50_101-150_ARTICLES_2026-10-28.xlsx`
- Output bytes: 1109787; SHA256 `e444a6ecefac57106ccf4d5bc57aa0b47e25c85b8ac4d4349f875cbb85014f26`
- **Full binary workbook is not uploaded to GitHub by this checkpoint.** This is a transparent provenance record; source/output XLSX and full QA ZIP are delivered as ChatGPT file artifacts.

## Authorized scope and change
- Exact 50 target products 101–150 = Excel rows 102–151, series KTGB(8), KTYB(7), KTDB(6), KTZB(7), KTVB(12), KTLB(10).
- Wrote precisely 50 missing `Наполнение MIXED!F102:F151` article values from same-row `Сбор данных!C102:C151`.
- For every row, matched original article against complete SKU in name B, lowercase symbolic code C and source C. Every match succeeded.
- Product-field fill 1508/3850 -> 1558/3850 (40.47%). **No claims of 50 tech-ready or import-ready items**.
- Unchanged: all protected 306 products (rows 2–101, 152–357). Independent OOXML regression: original 79 worksheet XMLs preserved byte-for-byte except `xl/worksheets/sheet1.xml`, with **exactly 50 cell nodes changed**, all target F102:F151; new QA sheet number 80 added.
- 356 products x77 columns still intact.

## Source provenance and risks
- Exact SKU from own `Сбор данных` sheet is FILE_EXACT_TRACEABLE.
- OEM DX PRO catalog indexed: https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf — indexed pages show exact B-series, but visual PDF cross-check not yet possible; DO NOT classify indexed table as OEM_VISUAL_VERIFIED_EXACT.
- 8 historical dealer/marketing conflicts kept open: KTGB24 (area, warranty), KTGB30 (area, warranty), KTGB40 (area), KTGB50 (warranty), KTGB60 (area), KTGB72 (area).
- Existing W pipe values physically 50/50; not old Stage108's 29 missing (old second batch is frozen).
- Fields AU (100), AV (0), AX (0) are 150 unverified commercial placeholders. Prices/inventory, guarantee AO, images and detailed technical verification remain blockers.
- Active batch readiness: TECH_OPEN 50/50, READY_FOR_IMPORT 0/50. Previous products 1–100 administratively FROZEN_BY_USER, not technically certified.

## Next-stage work
1. Visual OEM exact-SKU table audit of KTGB/KTYB/KTDB/KTZB/KTVB/KTLB, including value/units and accessories vs included.
2. Each SKU dual pass: `Сбор данных!E/F/G` to target and 77 target fields to evidence/applicability. Review conflicts.
3. Add only evidenced values, create Stage110 after true field changes and full regression; no fabricated inverter meaning, area, operating current, price or inventory.
4. Obtain real commercial owner/CMS values before import.

GitHub checkpoint is a **text-only stage record**, not a substitute for verified binary workbook.