# MIXED Stage99 — 900 exact SKU/field applicability decisions, 2026-10-26

**Latest verified complete XLSX:** MIXED_356_77cols_STAGE99_FIRST50_900_APPLICABILITY_CLOSED_2026-10-26.xlsx, **821594 bytes**, SHA256 **002163d4294cb1829964ca511a58edb118dc6d392a550b4eb3f464b50c1e899e**, **70 sheets**. XLSX binary is available in ChatGPT, NOT on GitHub.

Parent Stage98 is 819326 bytes, SHA256 4eeaa175ddfe9b77d21ae8ae38f944c0e4187f1918c199f3674ce7525895e0c8; parent Stage97 is 816004 bytes SHA256 3824cdcc6cfa0fd8167d2c5c0f776634c68dd223ad21769d44e82549ab12bd77.

Every exact original source file row 'Сбор данных!B2:B51' labels the precise SKU as a separate **Внутренний блок ... VRF/VRV системы**. Exactly **18 columns** are consequently not properties of the standalone refrigerant-DX indoor SKU: outdoor cabinet and mass (32,33,34,36,38), non-existent water heating/cooling hydraulic circuit including connections and outlet temperatures (58,59,60,61,63,64,65,70,71,74), and compressor / condenser cooling / outdoor source of heat (66,67,69). This is **18 x 50 = 900** model-field N/A decisions, tagged NOT_APPLICABLE_BY_EXACT_FILE_INDOOR_DX_TYPE. Evidence level is exact original FILE unit category + physics, NOT 900 separately opened OEM PDF pages. Leave those 900 product cells **empty**, never insert zeros, never substitute drain pipe as hydraulic loop.

Old provisional N/A for the remaining 50 cells in column 77 (Тепловая мощность) is **reopened** as OPEN_HEAT_OUTPUT_SEMANTICS. Determine whether this field duplicates column17 or means another system parameter before blank-versus-duplicate decision.

**All 3850 field statuses** recategorized in downloadable chat sidecar STAGE99_FIRST50_3850_FIELD_QA.csv. **900 detailed per-model N/A records** in downloadable chat STAGE99_FIRST50_EXACT_UNIT_NA_900.csv and will be archived as GitHub index. There are **1636 physically populated values** among first50 (unchanged). Historical 40 critical blank cells remain 21 old IGC refrigerants +15 contractual Daichi warranty +4 exact BS45 dimension; further Daikin region, IGC old K unit W/H/D axis, source/OEM QA remain open.

Independent OOXML check across all original 356 x77 =27412 cells, every source/history original cell and full 68 Stage97 sheets found **0 differences** after Stage98 and Stage99 export/re-import. The other 306 product rows52-357 have **0 differences**. New QA sheets: QA98 выпуск 50, QA99 N-A 900. Total 70 sheets. Certified READY_FOR_IMPORT=0/50, TECH_READY_COMMERCIAL_BLOCKED=0/50.

These stages certify blank-field applicability from exact original user file, NOT new engineering measurements. Resume from Stage99 full binary, never stage83/96/97; do not copy other suffix models, do not write uncertain refrigerants, weights or acoustic values.