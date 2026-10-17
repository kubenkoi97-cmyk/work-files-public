# STAGE42 — Kentatsu DX PRO BASIC / KTGV exact technical catalog links
**2026-10-17 — INTERMEDIATE; NOT READY FOR IMPORT**.

## Source and scope
- Base workbook: STAGE41_DAIKIN_OEM_QA_2026-10-16.xlsx (local verified file, prior work).
- Technical catalogue, from C-O-K indexed PDF: https://www.c-o-k.ru/library/catalogs/kentatsu/37986/140011.pdf ; alternate path https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf .
- Web index contains *exact KTGV_HZBN1 model table* for all selected 18,24,30,40,50,60,72,80 sizes; power, flow, noise, dimensions, pipe diameters and weights. [KTGV manufacturer-branded PDF indexing](https://www.c-o-k.ru/library/catalogs/kentatsu/37986/140011.pdf). Visual page verification of this large PDF is still open: mark PDF_VISUAL_QA_PENDING, **do not interpret link fill as final document QA**.
- Exact models (workbook rows 45–52): KTGV18HZBN1, KTGV24HZBN1, KTGV30HZBN1, KTGV40HZBN1, KTGV50HZBN1, KTGV60HZBN1, KTGV72HZBN1, KTGV80HZBN1. Added 8 HTML links in column 43 (technical documentation) *only where blank*.
- Source/log and QA42 per-model rows appended in the workbook; QA42 open-field sheet regenerated from actual Stage41 open cells.

## Regression
- 356 product rows ×77 output columns, exact ordering and existing text maintained.
- Exactly **8** changed cells in output range, all prior blanks in col 43; no nonblank overwritten, no formula-error string detected in output.
- Stage41 baseline open core 623 → Stage42 **615**; exact documentation remaining 114 →106; all **341** manufacturer-warranty unknown remain unfilled. Conditional 77-field audit remains unfinished.
- Exported full intermediate XLSX: `MIXED_356_77cols_STAGE42_KENTATSU_KTGV_DOC_QA_2026-10-17.xlsx`, size **530361 bytes**, SHA256 `c5ef0d54aadd3ef7d5735668adfc881d38c51f6e7d0c6ff49953714e786047ff`. **Local conversation file generated; binary GitHub publication NOT verified.**
- [Exact row/field patch](STAGE42_EXACT_MODEL_DOC_PATCH.csv).

## Open critical conflicts
- FXKQ20A / FXKQ25A 18 kg in Daikin manufacturer tech manual EEDEN241; indexed 2026–2027 French market catalogue shows 17 kg; this revision/market difference requires QA and import blocking.
- Daikin FXMQ200A/250A multiple conflicting editions, manufacturer version to settle.
- Midea MI2-T3, MI2-T2 and MI2-DLD R32/R410A conflicts; no automatic revision.
- 615 baseline applicable open fields and unresolved applicability of some supplemental columns.
