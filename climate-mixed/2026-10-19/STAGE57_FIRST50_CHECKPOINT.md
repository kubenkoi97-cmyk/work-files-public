# MIXED Stage57 — first 50 only / 42 source-backed installation fields

## Scope and method
- Strict target: first **50** product rows of the actual 356-product output sheet, Excel rows **2 through 51** (IGC 35, Daikin 8, Kentatsu 7). Do not change the remaining 306 products.
- Stage56 manufacturer-warranty corrections remain in force; this stage only fills **42 previously empty** column 68 `Тип установки` fields, linked to each model's **own exact** original FILE source `Сбор данных!E/F[row]`.
- Four Daikin exact installation fields `FXKQ32A / FXKQ40A / FXKQ50A / FXKQ63A`, and four IGC `IMS-QV125NH(DC), IMS-QV140NH(DC), IMS-AHU220NH(DC), IMS-AHU280NH(DC)` were already filled. **All 8 have been preserved without re-writing.**
- Modes represent only manufacturer/product mounting class as evidenced by the original model-specific text: wall, concealed duct, cassette, ceiling cassette, floor-ceiling. They do not imply any remote control, wiring kit, or mounting hardware is bundled. Original model-specific OEM installation manuals and regional revisions remain to be checked.

## Actual technical workbook
`MIXED_356_77cols_STAGE57_FIRST50_42_INSTALLATION_MODES_2026-10-19.xlsx` (431818 bytes, SHA256 `db234bd02f6896312879857565517de2863ea7b3217c55b3bb844845e972f4e9`), descended from Stage56, whose exact original source texts and historical source/log sheets remain. Actual tested output diff across the 356×77 product area, after the subsequent Stage58 export, confirms exactly 42 formerly empty fields populated and **none of the remaining 306 products altered**.

The full binary workbook is available in ChatGPT sandbox but is **not confirmed as GitHub-uploaded binary**; GitHub stores the real [42-row reproducibility patch](STAGE57_FIRST50_42_INSTALLATION_PATCH.csv) and this status report. Continue with a 50×77 individual applicability audit in Stage58.
