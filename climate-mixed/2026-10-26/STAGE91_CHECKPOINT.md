# MIXED Stage91, 26 October 2026 — precise old IGC DC model technical verification

## Full working book
- **Current complete validated XLSX:** `MIXED_356_77cols_STAGE91_FIRST50_IGC_DC_OEM_4_AREAS_11_DOCS_2026-10-26.xlsx`.
- **802105 bytes**, SHA256 **`16e71acb4889ab8c75f6acf9541642393b86c6334f017452696dd7ff70ed1a90`**, **60 sheets**; original Stage90 full SHA256 `ee476daee694713e44320a24a7c7bd2679649967814715525878af4a1c30d176`.
- Workbook is **available as ChatGPT binary file, not yet a GitHub XLSX binary**. These text files are not the XLSX.

## Exact product changes (15)
- **4 new physical data cells** — Excel rows 27,28,29,31, `N` marketed area: 28,36,45,71 m², respectively, exact `IMS-QV28NH(DC)`, `IMS-QV36NH(DC)`, `IMS-QV45NH(DC)`, `IMS-QV71NH(DC)` per IGC Russian authorized dealer exact literal SKU. **Marketing coverage only, not thermal load calculation**. No data copied from DC(5) or non-DC editions.
- **11 technical documentation links** appended at `AQ`: 8 old `IMS-QV...(DC)`, 3 exact `IMS-BS...(DC)`. Existing original URLs kept. New link is brand-printed original IGC catalogue exact factory SKU table; original printed pages 49 (floor QV) and 53 (duct BS), PDF page index 3. Original PDFs were **visually viewed**, not merely indexed.
- 101 model-specific comparisons between already-filled values and visually read OEM values: **101 MATCH, zero conflicts** (8 QV × 10 properties + 3 BS × 7 properties). No double-counted fills.

## Full independent OOXML regression
- Exactly **15 changed** of **356×77 = 27412** product cells, precisely four `N` and eleven `AQ` named in CSV.
- **0 changes in 306 protected SKU rows 52–357.** All Stage90 original 59 sheets retained identical cell values; additional `QA91 DC 11 OEM 4 areas` sheet. Model order and headers unchanged.
- First50 filled fields **1627 → 1631** (out of 3850; physical blanks include N/A/commercial).

## Still unverified
- **40 historical CORE** remain: 21 exact old DC IGC refrigerants, 15 contractual Daichi warranties, 4 disputed BS45 body-size cells. IGC catalogue exact QV/BS technical tables **do not provide refrigerant**, no assumptions permitted. The BS45 body-size anomaly (identical 700 mm width across markedly different packaging) remains unresolved even though OEM PDF printed it; don't propagate.
- Other regional edition / manufacturer QA remains open, **0/50 READY_FOR_IMPORT**.
