# Stage 14 — Decorative panel exact-accessory cross checks
Date 2026-10-15. **WORKING — NOT IMPORTABLE.**

- **17** formerly missing cassette panel dimension cells were written in working stage14 XLSX. Original 356 models, 77 target columns and previous 13 stages preserved.
- Families: Kentatsu KTYV (5), KTZV (2), KTVV (1); Midea MI2-Q4DHN18(At) (9).
- For each update, Russian exact model/cassette assembly SKU was cross-checked with a named physical accessory, then the same named accessory's dimensions in a factory catalog were used. **This confirms the accessory dimension, not that every retailer sells the accessory bundled with the standalone block**.
- Important edition sensitivity: KTVV90 KPU95-D3 has 950×53×950 specified in 2025 factory table for this panel while another KPU95-D3 model lists thickness 50 mm; model/edition is flagged for revisit, not marked final.
- **Do not generalize** panel information to unknown KTYV18/72, KTZV15/30/40/50/70, KTVV30–180 or MIH160/180 with competing panel editions.
- Source-by-model mapping and exact dimensions: [STAGE14_17_PANELS.csv](STAGE14_17_PANELS.csv)
- Rebuilt applicability-aware core exception list: 925 → **908**. Includes 17 actual fills, no removal of falsely applicable fields and no rewrites of preexisting nonblank data.
- Web field-level and all-priority-domain full search for 356 models remains OPEN.
- Chat XLSX: `MIXED_356_77cols_STAGE14_PANELS_2026-10-15.xlsx`. Binary not uploaded to GitHub; field CSV and audit checkpoint are GitHub-resident.
