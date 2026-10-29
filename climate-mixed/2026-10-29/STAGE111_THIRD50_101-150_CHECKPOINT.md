# MIXED Stage111 — THIRD50 101–150 (2026-10-29)

**STATUS: VERIFIED FULL XLSX — Stage111 is the current full working baseline.**

## Artifact

`MIXED_356_77cols_STAGE111_THIRD50_101-150_MERGED_2026-10-29.xlsx`
- SHA256: `ea181eb7b0afccbd130da64943b7aba5b982b168945614b81fce1dffabd16fae`
- Size: 1,112,533 bytes. The exact XLSX is downloadable from the accompanying ChatGPT conversation, **not published as a binary GitHub file**.
- Full ZIP handoff in ChatGPT: `MIXED_STAGE111_THIRD50_101-150_FULL_HANDOFF_2026-10-29.zip`, SHA256 `a06b2cdd8f7cdd23a0309cfb6efed9df525566beda08edfa099c1f0e9aeaf1dc`.
- Previous current Stage109 full XLSX SHA256: `e444a6ecefac57106ccf4d5bc57aa0b47e25c85b8ac4d4349f875cbb85014f26`.
- Stage110 was PATCH_ONLY; all 100 Stage110 changes have now been applied to this full book using artifact_tool.

## Verified regression

- Exactly **100** target cell updates: `AT102:AT151` 50 model-specific descriptions, `BP102:BP151` 50 installation methods.
- Every patch's old and new cell value independently matched the source and destination workbook (100/100).
- 356 items × 77 columns preserved, 80 worksheets same names and order; other 79 worksheet XML parts byte-for-byte unchanged.
- Changed XLSX package entries: product sheet1.xml; workbook.xml and two relationship files regenerated without changed sheet contents.
- Protected 306 items (rows 2–101 and 152–357) untouched; all existing worksheet formulas unchanged.
- Physical fill 1,558/3,850 → **1,608/3,850** (41.77%); 50 net filled cells, 50 HTML cells rewritten.
- Regression JSON: [STAGE111_THIRD50_MERGE_QA.json](STAGE111_THIRD50_MERGE_QA.json).

## Evidence/known limits

- Numeric same-row SOURCE_FILE_EXACT reconciliation 500/500 passed at Stage110: [STAGE110_THIRD50_NUMERIC_AUDIT_500.csv](STAGE110_THIRD50_NUMERIC_AUDIT_500.csv).
- Exact 100 input patch values: [STAGE110_THIRD50_FIELD_PATCH.csv](STAGE110_THIRD50_FIELD_PATCH.csv).
- Noise-semantics: [STAGE110_THIRD50_NOISE_SEMANTICS.csv](STAGE110_THIRD50_NOISE_SEMANTICS.csv): 27 minimum vs 23 maximum reported as unnormalized scalar in old field U. Not changed.
- 2026 Kentatsu series brochure confirms 2026 B-series taxonomy, including `KTGB` wall and `KTLB` low-static duct, distinct from older 2025 descriptions: https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf ; https://daichi.business/upload/iblock/f68/trfx2yykfe00hc4mv0r7x0s2j6gesyzg/K3_2026_DK26_02.01.03_11.02.26_low_resolution.pdf.
- Catalog online indexing is not the same as visually checked exact model page; independent visual PDF auditing remains open.

## Still open

- 8 historic dealer disputes on coverage/warranty.
- All 50 SKU: AU=100, AV=0, AX=0 are invalid commercial placeholders; real price, inventory, GTIN/ID, pictures and warranty need confirmed owner data.
- 0/50 READY_FOR_IMPORT. Do not claim certified or publish the products in CMS.
- Continue only rows 102–151 and keep old stages/historical QA.

**GitHub state:** checkpoint, patch source and QA logs committed as public text. Binary workbook and ZIP remain available as ChatGPT downloads; no binary GitHub URL is asserted without a verified commit.