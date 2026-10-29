# MIXED Stage113 — THIRD50 101–150 — 2026-10-30

**Current verified full local baseline:** `MIXED_356_77cols_STAGE113_THIRD50_101-150_OEM_FEATURES_2026-10-30.xlsx`; SHA256 `b61cf7c3ab01e4124b06008a418ada6b2e93512c994bf71bead5c51697b8a58a`, 1,112,877 bytes. Previous Stage112 SHA256 `18c9cfc70a12c9e907701e098a602a64e256cbdbc287665cd3c4a6c982e710fd`.

### Implemented
- **16 precise existing description revisions**, `AT117:AT122` for KTDB six and `AT142:AT151` for KTLB ten.
- KTDB: manufacturer indexed feature of built-in drain pump and condensate lift up to 1,200 mm.
- KTLB: manufacturer indexed built-in drain pump, supplied G1 air filter, exact maximum external static pressure 50 Pa for KTLB18/24/30/40/50/60/72 and 80 Pa for KTLB80/90/115.
- Exact model identity cross-checked against each existing full-SKU row, source `https://daichi.business/support/documents/download.php?ID=27751`.
- Evidence class **OEM_INDEXED_SERIES_FEATURE_NOT_VISUALLY_SIGNED**; PDF web viewer timed out, so **no claim of visual OEM verification**.

### Hard QA
- Entire 80-sheet source workbook exported successfully via artifact_tool.
- Exactly 16 product cells altered; no added nonempty product field, no formula changes, no changes to any of the 306 protected products.
- All 79 other worksheet XML parts byte-identical to Stage112. Model subset remains 50×77 with 1,608/3,850 fields physically filled (41.77%).
- READY_FOR_IMPORT **0/50**. Stock=100 and prices=0 remain unverified placeholders and must never be assumed real. Warranty, product images, exact technical audit, area disagreements, noise column MIN/MAX remain open.
- History retained; Stage112 stays as archived predecessor, Stage113 is the newest verified in-chat full XLSX.
- Full binary Stage113 XLSX and ZIP are available via ChatGPT artifacts. They are **not claimed to exist on GitHub unless independently verified**.

### Files
- `STAGE113_THIRD50_FIELD_PATCH.csv`: complete before/after, 16 exact SKU models.
- `STAGE113_THIRD50_READINESS_50.csv`: readiness by model.
- `STAGE113_THIRD50_QA.json`: regression and exact checks.
- `STAGE113_THIRD50_OPEN.csv`: unresolved technical/commercial work.

### Next
Do not revise 306 protected rows. Preserve all technical field distinctions between indoor and outdoor unit; manufacturer per-model PDF checks continue, no guessed stock/prices, warranty, inverter, coverage, or noise-scalar normalization.
