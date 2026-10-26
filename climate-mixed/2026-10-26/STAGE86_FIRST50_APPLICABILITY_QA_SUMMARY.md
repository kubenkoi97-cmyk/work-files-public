# Stage86 — 50 × 77 applicability pass (2026-10-26)

This is a conservative **triage** over the exact exported Stage86 55-sheet workbook, not a declaration of OEM verification. Main product values in Stage86 remain unchanged by this external triage. Detailed 3,850-line and 50-model CSVs are delivered as ChatGPT attachments (binary local files cannot be read by GitHub connector). Use Stage86 XLSX SHA256 `0b3edd0aad15d2d3170e4e7186597a91209f4ae81d45365b0de383b0e5867c3a` as the auditable primary source.

## 3,850 exact model-field status entries

| Status | Cells | Meaning |
| --- | ---: | --- |
| PRESENT_OWN_EXACT_MODEL_SOURCE_OEM_QA_OPEN | 1323 | Physical data present; factory-region source still requires final exact-SKU verification |
| N_A_PROVISIONAL_INDOOR_REFRIGERANT_UNIT | 950 | Based on type of equipment, outdoor casing/hydronic piping/compressor fields appear not applicable; **provisional only**, not OEM-certified N/A |
| CONDITIONAL_OR_QA_OPEN | 537 | OEM accessory/system/technical applicability unresolved |
| OPEN_FIELD_SOURCE_OR_APPLICABILITY | 397 | Need exact source or proven N/A |
| SOURCE_OWNED_COMMERCIAL_OPEN | 300 | Original shop-admin fields left blank, no substitute external price or stock |
| SOURCE_OWNED_COMMERCIAL_PRESENT | 250 | Original FILE shop-controlled data retained |
| PRESENT_WARRANTY_IGC_SCOPE_QA_OPEN | 35 | Existing 12-month IGC requires historic edition/contract warranty scope check |
| BLOCKED_REFRIGERANT_OLD_DC | 21 | Exact factory refrigerant version not resolved |
| BLOCKED_DAICHI_CONTRACT_WARRANTY | 15 | Missing contractual warranty evidence |
| BLOCKED_BS45_CABINET_DIMENSIONS | 4 | Exact old DC dimension technical drawing needed |
| PRESENT_SYSTEM_CONDITIONAL_QA_OPEN | 13 | Existing value tied to system/accessory requires review |
| Five Stage84-86 exact-evidence additions | 5 | 2 maximum currents, 2 IGC rec areas, 1 Daikin rec area |
| **Total** | **3850** | 50 exact first rows × 77 original columns |

Exactly **40 historical CORE empty blockages**, and more unverified conditional values; there are **0 confirmed READY_FOR_IMPORT** or **TECH_READY_COMMERCIAL_BLOCKED**. Explicit caution: 950 provisional type-N/A positions are **not proven** visually for each model; this is a starting queue for actual technical certification. No blank count here is treated as the number of mandatory missing fields.

Per-SKU CSV locally named `STAGE86_FIRST50_READINESS_50_2026-10-26.csv` and per-field local `STAGE86_FIRST50_APPLICABILITY_3850_2026-10-26.csv`; user can download both from conversation. These are generated from the authoritative Stage86 XLSX and source row/model literal strings, **not** back-filled into the 77 working columns.
