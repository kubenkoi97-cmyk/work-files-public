# MIXED STAGE110 / THIRD50 101–150 — 2026-10-29

**Status: PATCH_ONLY. The full Stage109 XLSX remains canonical.**

## Deliverables and verified state

- Full current baseline: `MIXED_356_77cols_STAGE109_THIRD50_101-150_ARTICLES_2026-10-28.xlsx`; SHA256 `e444a6ecefac57106ccf4d5bc57aa0b47e25c85b8ac4d4349f875cbb85014f26`; 356 products x 77 fields, 80 sheets.
- Stage110 independently exported **sidecar patch workbook**, `MIXED_STAGE110_THIRD50_101-150_PATCH_ONLY_2026-10-29.xlsx`; SHA256 `2856dedc043c1e4c720cc7b562e14ba6674ff560d8292685c3a616c1e8d75d6b`; 11,463 bytes; 2 sheets.
- Exactly 50 proposed `BP102:BP151` field additions: installation mode appropriate to individual exact SKU/series.
- Exactly 50 proposed `AT102:AT151` rewrites: individual SKU-specific descriptions with cooling, heating, indoor-unit input in watts, max airflow, acoustic min–max, housing dimensions, weight, fluid/gas tube diameters, R410A and precise optional compatible panel models.
- Proposed **100 cell changes**, **not yet merged** into the full workbook. `1558/3850` physically filled in canonical Stage109; `1608/3850` only after a successful future merge/regression test.
- Existing acoustic scalar `U` has **27 MIN vs 23 MAX** out of 50. Do not silently normalize U or confuse min and max. Exact paired data in `STAGE110_THIRD50_NOISE_SEMANTICS.csv`.
- 50 exact model/source records in `STAGE110_THIRD50_OEM_MODEL_INDEX.csv`. Full 100 proposed cell values in `STAGE110_THIRD50_FIELD_PATCH.csv`.
- Historical 8 area/warranty disputes remain OPEN. 50/50 commercially blocked (unverified quantity AU=100, purchase AV=0, retail AX=0), 0/50 READY_FOR_IMPORT. Other 306 products remain out of scope.

## Export blocker

Full export via `artifact_tool` of the old 80-sheet book failed first by timeout, then with `RPC connection closed by peer`. No new full Stage110 XLSX was falsely announced; **retain Stage109** and use the Stage110 patch file only as a sidecar. A ZIP handoff containing Stage109 baseline + sidecar + 3 audits + manifest is downloadable in the ChatGPT conversation, but the binary XLSX/ZIP files have **not been uploaded to GitHub**.

## Evidence

Manufacturer DX PRO VII catalog with model-specific B-series tables: https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf. Original model-specific internal source: `Сбор данных!C/F102:F151` of Stage109 baseline.

The ~22MB PDF could not be opened/screenshot in the browsing environment: **FILE_EXACT + OEM_INDEXED_NO_VISUAL**, not falsely claimed visual OEM certification. The acoustic ranges and full SKU pairing were verified against the model-by-model internal source and indexed manufacturer tables.

## Next

Merge 100 proposed changes into full workbook with a capable safe exporter; compare **all 356x77 cells** and original sheets. Do not modify rows 2:101 or 152:357. Continue OEM exact verification and owner commercial data requirements only after merge QA.
