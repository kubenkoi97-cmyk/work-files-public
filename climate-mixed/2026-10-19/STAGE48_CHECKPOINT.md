# Stage48 — Kentatsu KTZV24HZBN1 electrical-value evidence, 2026-10-19

**EVIDENCE ONLY — no validated new XLSX. This checkpoint does NOT supersede Stage47 binary.**

- Target workbook: exact Kentatsu `KTZV24HZBN1`, Excel row 61, column 73 `Максимальный ток, А` physically blank.
- Search-indexed content from exact SKU product card https://coldcontrol.ru/catalog/detail/kassetnyy-blok-vrf-kentatsu-ktzv24hzbn1/ states **0.46 A maximum current**. The fetched live page confirmed this SKU, its net weight, airflow and dimensions but **did not expose the full extended specifications table** with the current line. Treat only as `RETAIL_INDEXED_OEM_PENDING`, not `WEB_EXACT_FULL_TABLE_VERIFIED` or `OEM_PAGE_VERIFIED`.
- The factory original regional document/edition was not visually opened. Value **0.46 A has NOT been written to the released technical book**, pending full-page or OEM confirmation. It remains a candidate in [source-quality queue](STAGE48_EXACT_KTZV24_SOURCE_QA.csv).
- A draft Stage48 workbook update was attempted after successfully building Stage47, but `artifact_tool` lost its RPC connection during two separate export attempts. No valid final Stage48 XLSX exists and no source file was overwritten. The actual latest usable workbook remains Stage47, SHA256 `91ce58730c4f8d27091d450aa3f58d213a9940fd4ba335e631ffc24b33e9ac48`, 640092 bytes.
- Count remains **356 ×77**, **613** CORE blanks, 0 additional confirmed cell changes for this evidence-only stage. Do not claim new field count or new XLSX until export and reimport succeed.
- Next: manufacturer exact model PDF page or independent correctly-labelled maximum-current table (not current in heating/cooling or circuit-breaker current). Also verify KTZV15 & KTZV60 historic 0.46/0.65 A.
