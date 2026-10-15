# Stage 21 — Full-scope structural + applicability audit

**Date:** 2026-10-15. **STATUS: OPEN / NOT READY FOR E-COMMERCE IMPORT.**

## File and exact integrity
- [Stage 21 full working XLSX (direct public download)](https://raw.githubusercontent.com/kubenkoi97-cmyk/work-files-public/main/climate-mixed/2026-10-15/MIXED_356_77cols_STAGE21_FULL_QA_2026-10-15.xlsx), file size **866,917 bytes**, Git blob SHA `62ceee2eba731e7685c26475c37cc62333aaf3b3`, SHA-256 `bf59693ad963ed19edcd41065f1a4d32b807b4ed6cfa40c52a725130776a49f5`.
- **Binary XLSX published as a real file**, not base64 fragments; GitHub directory listing was read back and returned the same blob SHA and length. Local Git SHA computed independently and matches remote.
- Workbook has **356 selected product rows ×77 exact output columns**, identical headers/model ordering to stage17. All 388 nonselected source products excluded from this task.
- Exactly **60** formerly blank cells filled across stages18–20, **zero** nonblank prior values overwritten. 38 distinct product rows modified.
- Full workbook-wide scan: **zero Excel error tokens**; 356 HTML descriptions retain required five-section structure and no `<b>`/`<strong>`; inverter values if present lowercase; mode `тепло-холод`; panel only for cassette, pressure only for duct.
- Updated existing `Источники` source attribution and appended **60** granular rows to `Log`. Audit worksheets `QA18`, `QA19`, `QA20`, `QA21` track fields, changed cells, exception evidence.
- Added `QA21 356 моделей`, `QA21 пробелы 800` and `QA21 поля 77` in the XLSX.
- Full public, editable CSV audit snapshots: [all 800 open applicable basic fields](STAGE21_OPEN_800.csv), [356-model audit](STAGE21_AUDIT_356.csv), [77-column coverage + applicability classification](STAGE21_77_COLUMNS_COVERAGE.csv).

## Remaining base-core required cells: 800
| Field | Open |
|---|---:|
| Manufacturer warranty months (seller claims not acceptable as OEM evidence) | **341** |
| Exact product technical documentation link | **221** |
| Refrigerant type | **117** |
| Liquid/gas pipe pair | **74** |
| Decorative panel dimensions | **20** |
| Indoor block net weight | **10** |
| Individual width/height/depth and combined body dimensions | **16** (4 models × 4 columns) |
| Electric input | **1** |
| **TOTAL** | **800** |

Open gaps by brand: Kentatsu 450, Midea 281, IGC 60, Daikin 8, Bosch 1.

**Caution:** these 800 are from the *core equipment-specific checklist*, NOT all potentially applicable blanks among the 77 source columns. Conditional fields like `Максимальный ток`, `Защита IP`, `WI-FI`, `Диапазон рабочих температур` still need per-model confirmation, and hydronic fields often do not apply to VRF indoor units. The 77-column coverage CSV explicitly distinguishes these.

## Session checkpoints
- [Stage18](STAGE18_CHECKPOINT.md) + [17 IGC model-family field changes](STAGE18_IGC_17_FIELDS.csv).
- [Stage19](STAGE19_CHECKPOINT.md) + [18 Midea MIH-Q1(A) factory-field changes](STAGE19_18_MIDEA_Q1_FIELDS.csv). Exact manufacturer 2026 brochure was actually **opened and page-image visually checked**: https://mideacaucasus.com/storage/zZ0MqaM6HbLkLXeI7toeFXdTPHzce1-metaUERfTWlkZWFfVjggTmV3IE9uZS13YXkgQ2Fzc2V0dGVfVlJGX0Jyb2NodXJlXzIwMjYtMDEtMDdfVjMucGRm-.pdf
- [Stage20](STAGE20_CHECKPOINT.md) + [25 Kentatsu/Midea field changes](STAGE20_25_FIELDS.csv).
- Stage21 is full integrity and gap audit, no speculative technical fills.

## Persistent conflicts to resolve BEFORE final
1. **KZA30HZAN1** factory catalog editions disagree on 9.52 vs 12.7-mm gas line. Current value 12.7 mm is flagged revision-specific, not indisputably correct. Catalog 2025 June: https://daichi.business/upload/iblock/b4d/5rjf3831ekyb4cqv2gz363d324reihkb/K2_DX-PRO-A_2025_180625.pdf ; second OEM catalogue https://www.c-o-k.ru/library/instructions/kentatsu/kondicionery-promyshlennye/37986/140011.pdf.
2. **KZA30/40** net masses differ by manufacturer catalog revision. Left empty, except for KZA18/24 and KZA50/60 where both editions agree. Panel mass is NOT indoor body mass.
3. **MIH18Q1HN18(A)**: heating is 2.0 kW in 2026 brochure; older engineering revision indicates 2.2 kW. Current 2.0 retained but flagged.
4. **MIH90GHN18(DP)**: gas pipe 15.9 vs 19.9 between engineering/marketing versions. Left empty.
5. Earlier: Midea MI2-Q4/Q4C market-code power collision; Daikin FXMQ200/250 regional mass/electric/size conflicts; Kentatsu KTGB18 gas pipe conflict; IGC IMS-BS45 body-vs-packaging dimension ambiguity; Midea MIH160/180Q4 panel thickness discrepancies.
6. All values newly accepted only from exact retailer SKUs, and OEM PDFs indexed but not visually reviewed, must be source-strength audited separately. **NO FINAL CLAIM.**

## Next priorities
1. Work by exact regional manufacturer SKU, not generic similar-series readings. Check all user priority domains first, expand exact product tabs, then >=5 supplementary accessible domains for missing key fields, recording last checked per field. These domain-by-domain deep passes remain open.
2. Re-audit the 7 Midea MIH-Q1(A) rows for 2026/2025 revision consistency before final; only pipes/panels/body dimensions were page-reviewed and confirmed. Refrigerant compatibility R410A/R32 is not a single uniquely specified refrigerant for a free-standing indoor unit.
3. Resolve the 74 pipe pairs and 20 panel dimensions via precise accessory/source link; investigate 10 masses and 16 dimensional gaps.
4. Manufacturer warranty must be documented separately from retail promises; leave blank if OEM term cannot be verified. Add exact-model tech documentation (221 gaps).
5. Repeat all 356 models × 77-column applicability audit and track first-party/retailer/parsed-index/page-reviewed confidence per field. Sync the next full XLSX as a true binary GitHub file using the proven create_blob→tree→commit→update_ref path; verify blob SHA/size by GitHub directory listing.
