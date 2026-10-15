# Stage 9 — 19 Kentatsu model corrections and renewed global QA (15 Oct 2026)

**Status: INTERMEDIATE, NOT IMPORTABLE.**

### Specific product fixes
- Nine Kentatsu **KTGB18/24/30/40/50/60/72/80/90HZBN1**: previously absent airflows now filled from the exact-model 2025 manufacturer table: `460, 500, 540, 580, 720, 860, 1220, 1380, 1420 m³/h`. Nine factory catalogue PDF links additionally filled.
- Ten Kentatsu **KGA24/30/40/50/60/72/80/90/100/115HZAN1**: exact-spec factory table supplied heating capacity, net mass and PDF technical documentation.
- **48** previously blank applicable cells were filled in total.
- Exact 2025 manufacturer catalog KTGB: https://daichi.business/upload/iblock/33b/k7c17waovzhtqmwrlnt6g7tose2z123a/K2_2025_11.09.25_LQ.pdf.
- Exact manufacturer table KGA: https://www.c-o-k.ru/library/catalogs/kentatsu/37986/140011.pdf.

### Unresolved conflicting data
**KTGB18HZBN1 refrigerant gas line:** existing `6,35/9,52` based on retailer exact-model cards; a newer Kentatsu table indexed `6,35/12,7`. **Neither is silently overwritten; manufacturer's direct model-specific confirmation is required**. This is tracked in `QA9 конфликт KTGB18`.

### Repeated applicability-aware 356-model audit
- Stage8 missing applicable core cells: **1132**.
- Stage9 after these precise fills: **1084** (delta **-48**).
- Missing categories now: manufacturer warranty **341**, technical docs **299**, refrigerant **135**, refrigerant piping **105**, series **94**, cassette decorative panels **43**, net weights **26**, power supplies **10**, duct static pressures **8**, inside dimensions four model rows, hearing power **1**, electrical input **1**, sound **1**, and Bosch outdoor dimensions one model.
- All **356 model rows** and **77 column positions** preserved. `QA9 полнота 356 актуально` and `QA9 применимые пробелы` contain refreshed model-by-model and field-by-field exception reports.
- Checkpoints passed for KTGB90 1420 m³/h, KGA115 12 kW, retaining disputed KTGB18 original pipe.
- The workbook `MIXED_356_77cols_STAGE9_KTGB_KGA_2026-10-15.xlsx` is provided as a chat artifact; its binary is **not claimed uploaded to GitHub**.
- All *unconfirmed* fields remain `OPEN`. This audit of workbook cells **does not imply** external websites were fully checked for 356 SKUs.

### Next priorities
1. Fix last missing heating (Midea MI2-100Q4DHN18(At)), last input power (MI2-22Q1DHN18(At)), last sound (Daikin FXKQ63A), and four sets of block dimensions only after exact model source validation.
2. Continue cassette panel **43** and duct pressure **8**.
3. Solve code/version collisions and KTGB18 conflicting pipe, documenting decision in model-level Log.
4. Repeat quantitative 356-model audit after every following batch.

Detailed patch: [STAGE9_48_FIELD_CHANGES.csv](STAGE9_48_FIELD_CHANGES.csv).
