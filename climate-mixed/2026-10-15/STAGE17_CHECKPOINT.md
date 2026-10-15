# Stage 17 — Midea B / G(DP) / Q2 (2026-10-15)

**INTERMEDIATE; NOT APPROVED FOR IMPORT.**

- Current stage covers the **same 356 models × 77 columns**.
- **23 previously blank fields** added, no existing nonblank data overwritten:
  - **6×** R410A for MIH15/22/28/36/45/56BHN18 based on exact manufacturer's Russian distributor table https://daichi.ru/catalog/multizonalnye-sistemy/vnutrennie-bloki-vrf-sistem/nastennye-bloki-vrf/mih-b-v8/.
  - **5×** piping MIH36/45/56/71/80GHN18(DP) individually from exact local SKU seller tables; never copy from no-DP suffix.
  - **12×** exact MIH22/28/36/45/56/71Q2HN18 gas/liquid pipe pairs and **net weight of indoor BODY** (not panel) from Russian Midea factory catalogue https://air-midea.com/upload/iblock/43b/0lq6fla7pf4pijetalxk0gyjb10xk3v2.pdf.
- **QA LIMITATION:** the Q2 Midea manufacturer's PDF was discoverable as indexed model-table text, but the PDF viewer timed out. **All 12 Q2 values are flagged `OEM_MODEL_INDEXED_PDF_VISUAL_QA_OPEN`, NOT independently page-image audited.** Next pass must review original pages and compare the six Q2 model versions before treating those entries as fully QA-approved.
- Q2 refrigerant `R410A/R32` in shared factory table is **not** a single model's refrigerant; all six Q2 refrigerant fields remain empty, to resolve exact Russian SKU cooling system/revision.
- Full field changes: [STAGE17_23_FIELDS.csv](STAGE17_23_FIELDS.csv).
- Working XLSX `MIXED_356_77cols_STAGE17_MIDEA_FACTORY_WEB_2026-10-15.xlsx` attached in ChatGPT, **binary XLSX not uploaded to GitHub**.
- Global applicable core blanks: **860**, from 925 (stage13) → 908 (14) → 903 (15) → 883 (16) → 860 (17).
- Unclosed: warranty 341, TECH docs 241, refrigerant 119, pipes 88, series 20, cassette panel 20, body weight 14, body dimension parts 16, power 1. Complete applicability and web pass for ALL 77 fields on all 356 models still OPEN.
