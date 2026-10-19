# Stage 47 — exact-model KTLV15 refrigerant piping, 2026-10-19

**PARTIAL — continue 356 × 77 anti-skip, not import-ready.**

Latest actual binary workbook: `MIXED_356_77cols_STAGE47_KTLV15_EXACT_PIPES_2026-10-19.xlsx`, **640092 bytes**, SHA-256 `91ce58730c4f8d27091d450aa3f58d213a9940fd4ba335e631ffc24b33e9ac48`. This XLSX exists as an actual ChatGPT sandbox output, *not* in this public GitHub repository. Parent: Stage46 full working workbook. GitHub connector cannot upload local binary. Do not conflate published text checkpoints with binary XLSX.

## Recorded edit
- Excel row **79**, Kentatsu `KTLV15HZBN1`, column **23** `Диаметр труб хладагента`: blank → `6,35/12,7` mm (liquid/gas). Source: https://pro-komfort.com/product/vnutrenniy-kanalnyy-blok-multizonalnoy-vrf-sistemy-kentatsu-ktlv15hzbn1/ ; full exact-model public technical card directly read. **RETAIL_VERIFIED_OEM_PENDING**; exact Russian manufacturer PDF page not viewed.
- **Important open contradiction:** the original exact FILE text reports heating capacity **1.8 kW**, while the exact seller page says **1.5 kW**. The existing heating value was **not overwritten**. Source claims `серебристый` colour for concealed duct unit; do not take it as factory-confirmed.
- The dealer's published warranty is **not** necessarily OEM manufacturer warranty. Did not copy.
- Exactly one previously blank output cell changed, 0 prior nonempty output cells changed. Model order (356) and 77 headers retained. Existing source history, Log and prior QA tabs preserved, new Stage47 three QA sheets generated.
- The Stage47 XLSX was re-imported by `artifact_tool` before the subsequent Stage48 export failed. Verified Stage47 diff and 613-record open register.

## Counts from reopened output audit
- CORE open **614 → 613**, because exactly one piping pair filled. Pipes **65 → 64**, warranty341, technical PDF links106, refrigerant63, panel20, net masses3, dimensions16, nominal electric input0.
- All 77 fields separately counted per SKU; a physical blank is not proof of applicability.
- Open registry [613 detailed exceptions](STAGE47_OPEN_613.csv), [356 model audit](STAGE47_AUDIT_356.csv), [77 field overview](STAGE47_77_COVERAGE.csv), [change patch](STAGE47_PATCH.csv).

## Next
Re-check exact OEM KTLV15 technical table to resolve 1.8/1.5 heating conflict and confirm piping. Continue FILE→WEB full pass and 613 applicable exceptions; prioritize pipe pairs, refrigerants and panels, with manufacturer documents and old SKU revision safeguards.
