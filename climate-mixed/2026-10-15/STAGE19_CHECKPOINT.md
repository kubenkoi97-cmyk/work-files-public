# Stage 19 — Midea MIH-Q1(A) visual OEM verification
Date 2026-10-15. **PARTIAL. DO NOT IMPORT.**

- Seven exact `MIH18/22/28/36/45/56/71Q1HN18(A)` models inspected on actual **Midea Group 2026 brochure PDF page 1 (page index 0)**. URL: https://mideacaucasus.com/storage/zZ0MqaM6HbLkLXeI7toeFXdTPHzce1-metaUERfTWlkZWFfVjggTmV3IE9uZS13YXkgQ2Fzc2V0dGVfVlJGX0Jyb2NodXJlXzIwMjYtMDEtMDdfVjMucGRm-.pdf.
- For these seven SKUs, restored **7 pairs** of liquid/gas pipe dimensions (18–56 `6,35/12,7`; 71 `9,52/15,9`), plus **7 complete HTML technical documentation links** to the OEM brochure.
- Two missing `MIH-Q1 (V8)` series restored for MIH18 and MIH71; existing other five were not overwritten.
- The exact `MIH90GHN18(DP)` had family name and model-indexed factory tech reference https://air-midea.com/support/marketing/download/9074/; **index-only** status, original PDF visual check open.
- **18** prior blank cells filled, **843→825** previously defined applicable-core missing cells. Same 356 products ×77 output columns.
- Midea Q1(A) body/panel dimensions and input/airflow were crosschecked for all seven against the actual PDF; already matched, no changes.
- New conflict `MIH18Q1HN18(A)` heating is **2.0 kW in 2026 Midea brochure**, while at least one older engineering table indicates **2.2**. Current 2.0 preserved with revision caveat; do not silently substitute.
- `MIH90GHN18(DP)` gas pipe differs across available engineering/marketing sources; **left blank**, not guessed.
- Refrigerant is not uniquely determined by this brochure for a particular outdoor system. No assumed refrigerant additions or changes.
- [Exact field patch (18)](STAGE19_18_MIDEA_Q1_FIELDS.csv), with OEM page-reviewed/indexed flags.
- Chat workbook: `MIXED_356_77cols_STAGE19_MIDEA_Q1_FACTORY_2026-10-15.xlsx` with QA19 exact-field and conflict worksheets. Binary GitHub publication NOT confirmed.
