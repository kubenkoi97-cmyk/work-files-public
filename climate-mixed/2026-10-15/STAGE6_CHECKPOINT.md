# Stage 6 — 15 October 2026

**STATUS: PARTIAL WEB QA. DO NOT IMPORT.**

- Further **19 models** (Kentatsu KTVB: 12, Midea MI2 Q4C(At): 7).
- **43 actual new field values** committed to the chat XLSX working workbook, maintaining 356 rows × 77 columns. Exact model QA rows and source URLs are included in its new sheets.
- The 2025 Russian Kentatsu factory model table https://daichi.business/upload/iblock/33b/k7c17waovzhtqmwrlnt6g7tose2z123a/K2_2025_11.09.25_LQ.pdf supplies individually matched KTVB panels, refrigerant pipes and masses. The international Midea catalogue https://www.midea.com/content/dam/midea-aem/id/PD-Midea-Atom-Catalogue-2024-12-25-V7-1.pdf supplies the panel's 620×65×620 dimensions and exact model strings, **but the power/capacity code means something different in the regional Russian catalogue**.
- The Midea 7 products remain flagged as unresolved conflict and are **not overwritten** with foreign-market cooling power, heating power, sound or pipe information. For example, MI2-15Q4CDHN18(At) is shown as 1.5 kW in Russian catalogue entries but as 4.5 kW in the Midea country-specific catalogue. The same code must not be assumed sufficient to disambiguate market variant.
- Evidence for local association between MI2 and panel T-MBQ4-03F: https://mircli.ru/kassetnye/2-2-9-kvt/Midea/ .
- Confirmed panel cross-check: T-MBQ4-03F; dimensions 620×65×620 mm.
- Seven conflicts documented in workbook's `Конфликты Midea рынок 6` worksheet. Other required checks across 77 fields remain open.
- The workbook `MIXED_356_77cols_STAGE6_KTVB_MIDEA_Q4C_2026-10-15.xlsx` is supplied as a ChatGPT artifact; GitHub stores the model audit and checkpoint **not the binary workbook**.

Next: resolve Midea with Russian-market precise passports, audit additional Kentatsu lines and separately check all applicable empty cells.
