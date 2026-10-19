# MIXED STAGE 53 — 8 exact Midea MI2-DL installation fields (2026-10-19)

**INTERMEDIATE / NOT SAFE FOR IMPORT WITH OPEN REFRIGERANT CONFLICTS.**

## Exact FILE extraction
- Models `MI2-36/45/56/71/80/90/112/140DLDHN18(At)` on Excel rows 310–317; each has exact model code within **its own** original source characteristics `Сбор данных!F310:F317`, with direct statement `Способы монтажа: под потолком или у пола`.
- Column 68 `Тип установки` previously empty for **all eight** rows. Filled literal standardized `под потолком или у пола`. No nearby-SKU inference, no refrigerant or warranty value changes.
- Manufacturer PDF pages for the exact ATOM B Russian variants were **not** visually verified in this pass. Source status `FILE_EXACT_MODEL_INSTALLATION__OEM_PDF_VISUAL_PENDING`.
- The MI2-45/90/140 DL **R32 versus R410A conflicts remain OPEN** and those product cards **must not be imported** until resolved. The mounting fact is independent of refrigerant identification.

## Binary workbook and QA
- Latest complete XLSX `MIXED_356_77cols_STAGE53_MIDEA_DL_EXACT_INSTALLATION_2026-10-19.xlsx`, **401705 bytes**, SHA-256 **`6f80fe71ef21d645708aa62d76b86d437be8852b2a7284876ab16128a2a7f76b`**.
- Built on validated Stage52, retaining original 356 products ×77 headers, source texts, `Источники`, `Log`, KZA conflict and earlier QA tabs. Appended `QA53 Midea DL монтаж`; total **14 sheets**.
- Independently re-imported exported binary; cell-level full 357×77 header/output comparison: **exactly 8 previously empty cells changed**, zero prior nonempty overwritten; model identities and ordering stable.
- Conditional column 68 filled **63→71**. Historical 613 open CORE applicable fields unchanged; full conditional applicability and WEB passes not complete.
- Binary exists as current-chat sandbox artifact; **GitHub connector only uploaded this source journal and patch, NOT XLSX binary**. Do not invent remote binary URL.

[Exact-source patch](STAGE53_MI2_DL_INSTALLATION_PATCH.csv) · [Stage52 previous checkpoint](STAGE52_CHECKPOINT.md).
