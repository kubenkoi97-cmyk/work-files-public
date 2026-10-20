# MIXED Stage67 — FIRST50 / Daikin source quality correction (2026-10-20)

**Actual scope: Excel rows 2–51 only.** This stage fixes two weak Stage66 marketed-area entries and audits eight Daikin SKU-edition conflicts. Do NOT promote any other regional/model suffix to exact target SKU.

## Corrected previous Stage66 source quality
- Excel row41 `FXKQ50A`, col14 recommended area **56 → BLANK**. Only traceable source was FXCQ50A primary card, not an independently verified FXKQ50A card.
- Excel row42 `FXKQ63A`, col14 **71 → BLANK** for the same reason: FXCQ63A primary page.
- Clear evidence retained in `Источники`, `Log`, `QA67 пересмотр площади` and [actual old/new CSV](STAGE67_FIRST50_RETRACT_UNSAFE_AREA_2_PATCH.csv). These changes are **quality corrections, not arbitrary loss**. The other four Stage66 area values from directly opened exact-SKU pages remain classified as *retailer-advertised estimates*, not certified service limits.

## Exact manufacturer model-suffix conflict audit
- Daikin official [FXKQ-A engineering table](https://www.daikin.eu/en_us/products/product.table.html/FXKQ-A.html) explicitly describes `FXKQ20/25/32/40/50/63AMVEB` (FULL EU model suffix): R410A and masses [18,18,19,24,24,24] kg; input [0.026,0.026,0.039,0.047,0.073,0.118] kW. Current Excel has **short SKU** `FXKQ20/25/32/40/50/63A` with R410A and mass [18,18,18,23,23,23] and input [0.024,0.024,0.033,0.038,0.055,0.118]. These numerical differences show the suffix cannot silently be dropped. Direct exact-short [MirCli FXKQ32A](https://mircli.ru/Daikin-FXKQ32A/) and [FXKQ40A](https://mircli.ru/Daikin-FXKQ40A/) claim R32, whereas the longer EU-suffix original claims R410A; **no current refrigerant was changed**.
- Daikin official [FXMQ-A engineering table](https://www.daikin.co.uk/en_gb/products/product.table.html/FXMQ-A.html) describes `FXMQ200AXVMB`/`FXMQ250AXVMB`: masses105/115kg, electric input0.54/0.65kW, dimensions1490×470×1100mm. The user's shorter `FXMQ200A`/`FXMQ250A` retailer cards report 137kg and body470×1380×1100 mm, input around1.292kW. No assumption of equivalence; model-region revision remains OPEN.
- Eight exact Excel SKU comparison rows and alternative manufacturer full suffixes, links, edition caution: [Stage67 SKU register](STAGE67_FIRST50_DAIKIN_VARIANT_CONFLICTS.csv). Existing dangerous cells colored amber; NO numerical overwrites on them.

## Latest actual exported workbook
`MIXED_356_77cols_STAGE67_FIRST50_DAIKIN_REVISION_QUALITY_2026-10-20.xlsx`, **736334 bytes**, SHA256 **`7871f0c49e2076a51494886cd6421df39dfd14cb7bc4fe38a2c28fc42f2bfcee`**. It descends from Stage66 732069B. Exported using `artifact_tool`, **reimported** and independently compared original full output 356×77 OOXML values: **exactly two old-nonempty→BLANK corrections** at N41,N42 and **ZERO other product value changes** (including all 306 out-of-scope rows). Original source sheet and headers retained, 33 sheets.

**GitHub currently stores source patches and reports only; current XLSX binary is a ChatGPT sandbox downloadable file.** Do not fabricate a remotely published workbook.

First50 after correction: approx **1566 physically populated cells** out of 3850, **41 base CORE open** plus two additional reopened marketed-area blanks, 0/50 certified import-ready. Next Stage68 inspect original user FILE exact model value disagreements with currently populated values without choosing a conflicting revision prematurely.
