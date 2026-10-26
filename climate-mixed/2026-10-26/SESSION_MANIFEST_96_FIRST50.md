# MIXED — canonical Stage96 for first 50 (2026-10-26)

**Latest validated FULL workbook:** `MIXED_356_77cols_STAGE96_FIRST50_DAIKIN_FXKQ63_EXACT_AREA_2026-10-26.xlsx` — **814190 bytes**, SHA256 **`82112cbfa6a01b0cb971bcca051f30c61c79fca6d81124fe06831fca1625cd8c`**, **67 sheets**. User-facing XLSX is in ChatGPT only, NOT uploaded as GitHub binary.

**Parent full workbook Stage95:** `MIXED_356_77cols_STAGE95_FIRST50_IGC_QV90_AREA_1T60_INDEXED_QA_2026-10-26.xlsx`, SHA256 `24b5ff469fc2202cac8fbba74f955b128ed2a7972899dec0baf42280d999bdfc`.

Stage95: one exact IGC `IMS-QV90NH(DC)` marketing area `N32=90`, 60 exact-model manufacturer-indexed 1T old DC fields matched (visual PDF original remains pending); all other 306 unchanged.

Stage96: one exact Daikin `FXKQ63A` **own exact** seller-marketed area `N42=71` from https://mircli.ru/Daikin-FXKQ63A/; this is **not** copied from FXCQ63A or FXKQ63M. Confirmed existing P/Q/T/U on exact seller but other values conflict: original workbook electric `0.118kW` versus retailer `0.095kW`, `R410A` vs `R32`, and warranty merchant 1yr vs contract Daichi. Did not overwrite any of these; require manufacturer's actual production region full SKU/lot and contract.

**Independent Stage95→96 regression on 356×77=27412 product cells: exactly one cell N42 changed; 0 changes among all 306 protected SKU rows52–357, all original 66 sheet values kept, added 1 QA96 sheet.** First50 physically filled **1636 / 3850** (physical blanks include N/A/controlled commercial); 40 historic CORE still open = 21 historic IGC DC refrigerant +15 contract warranties +4 old IGC BS45 cabinet sizes. Other per-model OEM/version applicability issues remain.

**0/50 READY_FOR_IMPORT; 0/50 TECH_READY_COMMERCIAL_BLOCKED certified.** Continue Stage96 full XLSX, never reconstruct binary from these patches or revert to Stage83.

GitHub records are checkpoints, text patches, source logs, conflicts and QA summaries. Binary full working XLSX delivered in ChatGPT only.