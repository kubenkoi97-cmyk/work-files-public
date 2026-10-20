# MIXED Stage76 — first50 2026 Daikin sources and KTGV exact model recheck

**2026-10-21, QUALITY-ONLY, ZERO technical product edits.**

Parent: Stage75 `MIXED_356_77cols_STAGE75_FIRST50_50x77_UPDATED_AUDIT_2026-10-20.xlsx`, 760129 bytes, SHA256 `023ef9d655d59eeeb2513406cf77952dae249cb2ef9a271bf38fe714d5ed6a91`.
Stage76 full binary `MIXED_356_77cols_STAGE76_FIRST50_OEM_2026_CONFLICT_AND_EXACT_SKU_QA_2026-10-21.xlsx`, 765513 bytes, SHA256 `8cf1265794eba57fe08c275afbc2b8ed8c6217019cc2b41fe91616cafccd264c`; exported via artifact_tool, rechecked direct OOXML for **ALL 356×77 product cells**, exactly **zero differences**. It is an actual ChatGPT sandbox file; it is **NOT** uploaded as a GitHub XLSX binary.
Added 3 separate QA sheets: QA76 Daikin 2026 gas; QA76 KTGV exact fields; QA76 queue first50. Total 44 workbook sheets, original model/source headings preserved. NONE of the excluded 306 SKU data was touched.

## Crucial Daikin 2026 documentary inconsistency: six exact printed short FXKQ codes
Daikin official VRV professional 2026 page 134 text includes a block headed FXKQ-A and `R32` in its **extracted text**: https://catalogues.daikin.eu/flipbooks/EN/Air_conditioning/ECPEN26-200/134/
Daikin official General 2026 page 496 includes the exact short FXKQ20A/25A/32A/40A/50A/63A and states `R410A`: https://catalogues.daikin.eu/flipbooks/EN/General_catalogue/07vrv/496/
More importantly, the INTRODUCTION of the first 2026 Daikin VRV catalogue explicitly separates FXKA-A/R32 from FXKQ-A/R410A: https://catalogues.daikin.eu/flipbooks/EN/Air_conditioning/ECPEN26-200/index.html
Thus page134 is **not reliable standalone evidence to switch FXKQ from R410A to R32**. It could be an editorial, pagination, layout, or text-extraction anomaly; original visual brochure page or an exact model nameplate / factory manufacturer BOM/revision is required to resolve source interpretation and Russian market. The six existing catalog cells R410A were *retained*, but they remain import-blocking in light of Russia retailer R32 claims.
Six exact model source comparison rows are in `STAGE76_DAIKIN_2026_6_EXACT_REVISION_CONFLICTS.csv`; initial QA sheet reports published claims separately, not a newly factory-confirmed change in specification.

## Kentatsu KTGV exact SKU QA
Seven target rows45-51 independently compared using exact SKU retailer cards wherever accessible. KTGV30 current0.36, KTGV40 0.39, KTGV50 0.41 A matched previously populated values; **no new fills**. KTGV18 literal liquid/gas `6.35/9.52` matches exact Coolsochi card. KTGV24 gas 12.7mm indexed retail only, liquid unknown; do not transplant KTGA/KTGZ data. KTGV18/24/60/72 maximum current remains blank because no verified exact-model rated current found.
KTGV vendor source grade is **retailer exact model**, not claimed as inspected factory document. [seven-row model QA](STAGE76_KTGV_7_EXACT_QA.csv).

## Current status and next
Only first50 original data rows2-51 are in scope; all 306 other models untouched. First50 physically filled 1618/3850 (includes inapplicable field slots), no additional product cells filled. 0/50 certified import-ready; 21 old IGC exact DC refrigerants unresolved, KTGV24 piping, Daikin edition/market, IGC BS45 body drawing, manufacturer warranty and commercial original prices remain open.
GitHub publication of checkpoints/CSVs is distinct from XLSX binary availability. Do not claim complete workbook remotely uploaded.

[Stage77 corrected interpretation](STAGE77_CHECKPOINT.md) · [Daikin six models](STAGE76_DAIKIN_2026_6_EXACT_REVISION_CONFLICTS.csv) · [KTGV seven](STAGE76_KTGV_7_EXACT_QA.csv).
