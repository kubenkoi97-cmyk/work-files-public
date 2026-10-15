# Stage 7 — Kentatsu KTKB and Midea MI2-Q1 (15 October 2026)

**STATUS: PARTIAL QA; NOT READY FOR IMPORT**

- **18 models** examined: 12 Kentatsu KTKB and 6 Midea MI2-Q1(At).
- **36 previously blank fields filled**: Kentatsu 12 piping and 12 documentation PDF links; Midea 6 exact decorative panel sizes and 6 refrigerant pipe pairs.
- Kentatsu primary exact-model technical factory table: https://daichi.business/upload/iblock/33b/k7c17waovzhtqmwrlnt6g7tose2z123a/K2_2025_11.09.25_LQ.pdf.
- Midea Russian exact-model specifications for pipe sizes and panel part numbers T-MBQ1-01G/-02G/-03G; separately the **physical accessory dimensions** in manufacturer-group catalogue https://www.c-o-k.ru/library/catalogs/mdv/38445/141735.pdf, visually cross-checked on PDF page 50 (printed page 48). MDV specifications **not** treated as specification for MI2 models: only identical panel *part number* dimensions were used.
- Case-specific results: MI2-22Q1DHN18(At) Russian product page gives liquid 6.35 mm/gas 12.7 mm, body 700×425×178 mm, R410A, airflow 400 m³/h. Input power and exact net weight still unconfirmed and deliberately left empty.
- Maintained 356 rows and exactly 77 output columns, preserved prior Kentatsu KTGV50HZBN1 airflow 720 and Daikin FXKQ20A R410A.
- No conflicting existing nonblank values were overwritten; no substitutions from near model codes.
- This intermediate XLSX was created as ChatGPT artifact `MIXED_356_77cols_STAGE7_KTKB_MIDEA_Q1_2026-10-15.xlsx`; CSV is GitHub-resident but XLSX binary publication **not confirmed**.
- The required comprehensive 356-model × 77-applicable-field audit remains open; status is **not complete**.
- [36 field-level patch rows](STAGE7_FIELD_CHANGES.csv).

Next checkpoint: a global 356-model **applicability-aware** missing-field audit and exceptions list; continue exact-model confirmation in new groups.
