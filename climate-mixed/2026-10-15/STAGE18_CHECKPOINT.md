# Stage 18 | IGC model-family coding
Date 2026-10-15. **INTERMEDIATE, NOT FOR IMPORT**.

- Base workbook Stage17, 356 products ×77 columns; no rows reordered.
- 17 genuinely blank Series cells filled for exact IGC model families 1T (6), 4T-Q (1), QV (8), AHU (2), derived explicitly from each exact SKU and manufacturer's family-grouped technical tables.
- Source https://www.c-o-k.ru/library/catalogs/igc/38333/141247.pdf was discoverable with its exact model-indexed technical tables; PDF viewer did not render the full document due file size. Family labels reflect model code, **not independently certified commercial series marketing names**. Keep this QA caveat.
- Field trace: [STAGE18_IGC_17_FIELDS.csv](STAGE18_IGC_17_FIELDS.csv).
- Regression: 356x77 kept; open core technical fields 860 → **843**, no overwrite of a nonblank field. Remaining field-by-field web passes NOT COMPLETE.
- Complete workbook in ChatGPT: `MIXED_356_77cols_STAGE18_IGC_SERIES_2026-10-15.xlsx`; binary GitHub upload is not verified.
