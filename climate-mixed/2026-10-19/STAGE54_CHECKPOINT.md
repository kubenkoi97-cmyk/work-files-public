# MIXED Stage54 — Kentatsu KTGB C-type heat exchanger (2026-10-19)

**INTERMEDIATE, NOT ALL APPLICABLE FIELDS CONFIRMED.**

## Exact source evidence
- Models `KTGB18/24/30/40/50/60/72/80/90HZBN1`, original Excel rows **101–109**. Each distinct source description `Сбор данных!E101:E109` states `теплообменник С-образной конструкции`. The output column 62 `Теплообменник` was empty for all nine.
- Filled those **nine previously blank** cells with `С-образная конструкция` (one value per exact SKU), without extrapolating from another product.
- Exact independently opened [MirCli KTGB90HZBN1 product page](https://mircli.ru/Kentatsu-KTGB90HZBN1/) explicitly describes `Теплообменник С-типа`; the remaining eight are FILE-exact observations and are **not** misrepresented as individually OEM page verified.
- QA status `FILE_EXACT_MODEL_DESCRIPTION__WEB_EXACT_KTGB90_CORROBORATED__OEM_VISUAL_PENDING`. OEM original page/model-year verification still required.
- Never assume this permits copying refrigerant-tube diameters between KTGB variants; `KTGB18HZBN1` has independently flagged gas line dimension conflict (9.52 vs 12.7) which remains OPEN.

## Exact tested XLSX
- Parent Stage53 full XLSX 401705 B; new complete `MIXED_356_77cols_STAGE54_KENTATSU_KTGB_HEAT_EXCHANGER_2026-10-19.xlsx`, **404023 B**, SHA256 **`52053fb9d3cf64588a759f7de19e9568294aaaa27948ff3b94083185706962ee`**.
- Adds workbook sheet `QA54 KTGB C теплообменник`; the `Источники` and `Log` rows appended with source cell, exact URL and pending status. **15 total sheets**.
- Re-opened the XLSX after export and compared **all 356×77 product output fields** against Stage53: **exactly 9 previously blank column-62 cells** changed; no previous nonempty value changed, no SKU/reordering changes. Conditional `Теплообменник` coverage Stage51 **18 → 41** after Stages52 and54.
- Historic **613 core applicable blanks unchanged**. The 31 extra fills this session are conditional fields omitted from the old CORE 613 denominator. A separate full conditional applicability review is still necessary.
- GitHub contains patch + checkpoint only; actual XLSX binary remains a separate downloadable ChatGPT file, **not uploaded to GitHub as a binary**.

[Exact nine-row patch](STAGE54_KTGB_C_TYPE_PATCH.csv) · [Stage53 previous checkpoint](STAGE53_CHECKPOINT.md).
