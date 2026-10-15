# Stage 5 — Kentatsu KTYB / KTZB — 15 October 2026

**INTERMEDIATE / NOT READY FOR IMPORT**

The existing 356-row, 77-column working workbook was extended without changing the scope.

- **14 exact Kentatsu models** processed (KTYB18/24/30/40/50/60/72HZBN1, KTZB18/24/30/40/50/60/70HZBN1).
- **42 previously empty fields** filled: seven KTYB net masses, fourteen cassette decorative-panel dimensions, seven KTZB liquid/gas pipe sizes, fourteen HTML links to a technical catalog that explicitly includes these models.
- Verified matching technical catalog source: https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf.
- For KTYB the specific panels are KPU1S-D3, KPU1M-D3 and KPU1L-D3 as appropriate; KTZB uses KPU65-D3.
- Zero overwritten conflicting nonblank values in this pass; all other 356 rows and the 77-column order maintained.
- Regression checks: KTGV50HZBN1 airflow remained 720 m³/h and Daikin FXKQ20A refrigerant remained R410A.
- The 77-field audit, required priority-domain coverage and open web gaps are **not complete**.
- Excel created: `MIXED_356_77cols_STAGE5_KENTATSU_KTYB_KTZB_2026-10-15.xlsx` (chat artifact, binary GitHub publication not confirmed).
- Full per-field patch is published as [STAGE5_FIELD_CHANGES.csv](STAGE5_FIELD_CHANGES.csv).

**Next:** continue on Midea MI2 Q1 / Q4C / Q4, matching full model including At suffix and keeping the body dimensions distinct from decorative panel.
