# STAGE 16 — Midea exact SKU refrigerants and families (2026-10-15)

**INTERMEDIATE; NOT PRODUCTION-READY.**

- Continued user's 356 selected products from stage15, with 77 columns and prior patches intact.
- **10 exact model SKUs, 20 previously blank fields filled**: 10 series values and 10 R410A refrigerant values.
- Models MIH36/45/56/71/80GHN18(DP) have `MIH-G(DP) (V8)` from exact Midea product cards on user priority iclim.ru, each explicitly confirms R410A.
- Models MIH22/28/36/45/56Q1HN18(A) have `MIH-Q1 (V8)` and `R410A`, each from exact product+panel card on user priority mircli.ru.
- **No model values copied** from MIH Q1 without `(A)`, or DP variants without `(DP)`. No `MIH90GHN18(DP)`, `MIH18Q1HN18(A)` or `MIH71Q1HN18(A)` values invented: missing until exact match.
- Exact links and 20 field changes: [STAGE16_20_MIDEA_FIELDS.csv](STAGE16_20_MIDEA_FIELDS.csv).
- **Remaining applicable core field gaps: 883** (stage13 925 → stage14 908 → stage15 903 → stage16 883).
- Current open categories: warranty 341 (manufacturer vs retailer distinction), exact technical docs 241, refrigerant 125, pipes 99, series 20, cassette panel dims 20, block net weight 20, 4 units missing body W/H/D/combined (16 total), one input power.
- The complete 356 x 77 field-level WEB pass, all priority websites, exact factory technical documentation, and independent verification of seller-only sources remain OPEN.
- Chat workbook `MIXED_356_77cols_STAGE16_MIDEA_EXACT_2026-10-15.xlsx` preserves all prior stages and has `Изменения этап 16`, `QA16 применимые пробелы 883`, `QA16 сводка Midea`; binary **not committed to GitHub**. Chat CSV `STAGE16_OPEN_883.csv` is full field-by-field exceptions.
