# MIXED latest verified full Stage95 — 2026-10-26

**Canonical working XLSX in ChatGPT:** `MIXED_356_77cols_STAGE95_FIRST50_IGC_QV90_AREA_1T60_INDEXED_QA_2026-10-26.xlsx` (812818 bytes; SHA256 `24b5ff469fc2202cac8fbba74f955b128ed2a7972899dec0baf42280d999bdfc`; 66 sheets). **Binary XLSX is NOT present on GitHub**; GitHub entries here are evidence and change ledgers.

Parent Stage94 SHA256 `ab4ca1cb95d12e8544c1a1f0f6d6296a67b00bc5d19616a693ed431757271a36`. Actual output change: **only Excel N32** (`IMS-QV90NH(DC)` recommended marketing area empty->90 m²), sourced from literal exact model seller field at https://igc.com.ru/catalog/vnutrennie_bloki_vrf_sistemy/igc_ims_qv90nh_dc/ . No other cells changed.

Six older exact IGC `IMS-1T...NH(DC)` models each have **10 prior technical values** compared with manufacturer indexed table: **60 MATCH, 0 conflicting**. See `STAGE95_IGC_1T_60_EXACT_FIELD_CHECKS_WIDE.csv`. Manufacturer PDF direct HTTP 502; mirror too large for visual open. This is **indexed-only QA, not OEM visual verification**.

Independent 356×77 OOXML re-import check: **exactly N32 changed**; headers and exact SKU order preserved; all 306 protected rows52–357 **unchanged**; all 65 old worksheet cell values retained, 1 new QA95 sheet. First50 physically filled **1635/3850**, including N/A and commercial blanks. **40 historical CORE gaps** persist (21 old exact IGC refrigerants, 15 supplier-contract warranties, 4 BS45 cabinet dimensions) and additional critical manufacturer/revision QA. **0/50 READY_FOR_IMPORT; 0/50 TECH_READY_COMMERCIAL_BLOCKED certified.**

**RESUME STAGE95 FULL XLSX**. Do not start from Stage83/Stage94 or try reconstructing full workbook from CSV patches.
