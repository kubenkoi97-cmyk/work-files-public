# Stage45 — 35 missing color values recovered by complete FILE-to-COLUMN comparison (19 Oct 2026)

**INTERMEDIATE / NOT IMPORT-READY.**
## Baseline and field patch
Parent actual technical workbook: Stage44 `MIXED_356_77cols_STAGE44_KTZV15_PIPE_CURRENT_QA_2026-10-19.xlsx` (581672 B, SHA256 `3a1f08d2bccbeeeb6db4260355a81e402b9bd03542965b8b40ed4fcc442b7122`). The more recent Stage43 library book is the ancestor; **not** the older Stage39/Stage42 evidence-only binary.

On all 356 source lines, the model identity was normalized only for identity checking (spaces/punctuation around suffix), not to replace the exact output SKU. Compared each row's original `Сбор данных!F` with column 22 `Цвет внутреннего блока [PROP_34]`. **35 exact-SKU rows explicitly contain a line `Цвет: белый` or `Цвет: Белый` but previously had empty output color**. Patched precisely those 35 cells to standardized `Белый`. They comprise Kentatsu KTZV (7), KTVV (12), KTHV (8), and Midea MI2-Q4D ATOM B (8). Each patch is independently traceable by worksheet row and literal source evidence in [35-row patch CSV](STAGE45_COLOR_PATCH_35.csv). Status `FILE_EXACT_VERIFIED_WEB_PASS_OPEN` (confirmed in uploaded source text, not yet factory-web-verified for every SKU). Manufacturer/dealer visual-check is still required for market and panel/body color nuance; do not count missing web-pass completed.

## Exact integrity and anti-skip check
- Latest actual Excel `MIXED_356_77cols_STAGE45_FILE_EXACT_COLOR_35_QA_2026-10-19.xlsx`, **604689 B**, SHA256 `5e82ddad759c7ba1b0a51438b029ee41d3e398089c6b3f22eab1a15998a327f5`. Exported via `artifact_tool` and **re-imported**; verified 357 output rows including header / 77 columns / 35 patch rows / **40 workbook sheets** and 56 output color values. Available as a current ChatGPT sandbox download, **NOT published as binary via this GitHub connector**: do not invent or claim a remotely uploaded XLSX.
- Cell-by-cell diff from Stage44 over 356×77 shows **exactly 35 changes to previously blank column-22 cells**; zero previous nonempty values modified. Previous confirmed Stage43 and Stage44 data, order, and exact 77 headings preserved.
- Existing Log and Источники extended with 35 source entries, QA45 exact patch, 356-row anti-skip QA, 77-column fill coverage and QA45 summary.
- Base CORE applicable exception count remains **614** because color is additional applicable completeness work not listed in old CORE denominator. Color column filled **21→56**. Conditional all-77 web-pass remains open; 300 output color blanks may include genuinely irrelevant or as-yet-unresearched fields, not automatically all omissions.
- [Per-model refreshed audit 356](STAGE45_MODEL_AUDIT_356.csv) correctly adds 2 Stage44 fields on row60 and 35 Stage45 color fields to the authentic Stage43 baseline; old core exceptions and their pending web-pass remain untouched. [77-column refreshed coverage](STAGE45_77_COVERAGE.csv).

## New conflicting exact-model evidence
On Kentatsu `KTLV15HZBN1`, stored **heating 1.8 kW** is supported by original exact-SKU FILE data (`Сбор данных!F79`), but the exact seller product page https://pro-komfort.com/product/vnutrenniy-kanalnyy-blok-multizonalnoy-vrf-sistemy-kentatsu-ktlv15hzbn1/ says **1.5 kW heating**. This is **CONFLICT_OPEN**. Do NOT overwrite 1.8 or infer from similar models; obtain exact Russian OEM technical table and document edition. [Conflict row CSV](STAGE45_NEW_CONFLICT_KTLV15.csv).

## Continuing obligations
615→614 CORE from Stage43→Stage44; Stage45 remains 614: warranties 341, docs106, piping65, refrigerant63, panels20, masses3, 16 dimension parts, electric input0. R32 vs R410A Midea 9 conflicts and Daikin FXKQ 17/18kg 2 conflicts remain open. The Sep 2026 Russian EAEU model declaration lists Kentatsu variant suffix X and Midea variants, but it **does not prove technical properties such as exact refrigerant, color or heating output for each variant**. Manufacturer 2024 Indonesian ATOM source uses different market model-code mapping (e.g. MI2-28Q4DHN18(At) 8 kW), so do not import numeric technical values from foreign region.

**Next stage:** check non-color fields across every FILE source against target fields, re-run exact model WEB/OEM including 15–30 SKU group, inspect PDF original page if accessible, log domain outcomes, export full binary with repeat 356×77 preservation.
