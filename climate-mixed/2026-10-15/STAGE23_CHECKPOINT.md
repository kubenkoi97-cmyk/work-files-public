# Stage 23 — Kentatsu exact-model R410A confirmation

**Intermediate / full technical QA remains OPEN.**
- Scope untouched: 356 selected products, exactly 77 target columns.
- **39** formerly empty refrigerant cells in factory DX PRO A model sheets filled `R410A`: KKA HFAN1 (10), KRA HFAN1 (7), KLA HFAN1 AC (6), KLA HZAN1 DC (6), KTA HFAN1/HZAN1 (6), KZA HZAN1 (4).
- Reviewed the **actual full page screenshots** for each of the six one-page PDFs. The corresponding exact SKU is explicitly printed in the model table, and the header identifies the series as `R410A`. [Per-model source and value CSV](STAGE23_39_REFRIGERANT.csv).
- Strict scope exclusion: KRA HZAN1 variants were **NOT** inferred from the KRA HFAN1 manual. No Midea R410A/R32 "either/or" assigned as a single refrigerant.
- Stage22 base 693 open core → **654** core remaining. No existing nonblank cell overwritten and no unrelated change.
- Earlier conflicts of KZA weight and gas line across editions remain unresolved; this pass changed refrigerant only.
- GitHub checkpoint ensures change trace. Cumulative XLSX will be committed next, with separate QA22 and QA23 sheets and updated Log.
- This result does not imply all 77 applicable fields or all priority web domains have been checked for every product.
