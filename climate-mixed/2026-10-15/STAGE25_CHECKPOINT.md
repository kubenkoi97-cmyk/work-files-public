# MIXED — Stage 25: cumulative audit and real Excel backup
**Date: 15 October 2026 | Status: INTERMEDIATE — NOT APPROVED FOR IMPORT**

## Scope and integrity
- Original source workbook: 744 products, of which **356** have both `Описание товара` and `Характеристики` populated. Other 388 untouched.
- Result: **356 × 77** product data rows/fields, original exact models, order, and all preceding stages maintained.
- Compared the Stage21 base 356×77 array cell-by-cell with Stage25: **152 changed cells**, *all previously empty*. No previously nonempty value overwritten; no unrelated cell changes.
- Rechecked the full product output against required formatting: mode `тепло-холод`, lower-case inverter, comma-decimal refrigerant pipe notation, HTML description sections and no bold markup, cassette-panel and duct-static-pressure applicability, and Excel error tokens. Programmatic warning count: **0**. Structural checks do **not** demonstrate all technical values are correct or all 77 conditional fields are complete.
- Added granular source/quality worksheets for stages 22–24, `QA25 источники 152`, `QA25 открытые 651`, `QA25 контроль 356`, `QA25 анализ 77`, and appended field-level `Log` entries.

## This session's exact-source modifications

| Stage | Fields | Evidence and QA tier | GitHub trace |
|---|---:|---|---|
| [Stage22](STAGE22_CHECKPOINT.md) | **107** | Recovered exact product-row technical PDF URLs from original FILE source rows: 76 Kentatsu and 31 Midea. URLs copied into TECH_DOCUMENTATION HTML, but source PDFs were **not all individually page-reviewed** and remain marked `PDF_VISUAL_QA_OPEN` | [patch rows](STAGE25_152_SOURCE_PATCH.csv) |
| [Stage23](STAGE23_CHECKPOINT.md) | **39** | R410A on exact models of Kentatsu KLA/KKA/KRA/KTA/KZA confirmed from screenshots of six genuine single-page manufacturer specification PDFs. No model-general extrapolation | [39-SKU record](STAGE23_39_REFRIGERANT.csv) |
| [Stage24](STAGE24_CHECKPOINT.md) | **6** | Exact Russian seller cards for KTVV30/40/80, three gas/liquid pipe pairs and three maximum current fields. OEM second-source review still pending | [6-field record](STAGE24_6_KTVV_FIELDS.csv) |
| **Stage25** | — | Full 356-model integrity, 77-column structural/conditional coverage, exact 152-cell diff and open-field reconciliation | [all 152 changes](STAGE25_152_SOURCE_PATCH.csv) |

## Current OPEN core applicable cells — 651
| Field | Missing cells |
|---|---:|
| Manufacturer warranty (not retailer promise) | **341** |
| TECH_DOCUMENTATION precise model/source links | **114** |
| Refrigerant | **78** |
| Refrigerant piping | **71** |
| Cassette panel dimensions | **20** |
| Indoor block net weight | **10** |
| Unit width / height / depth / combined dimensions | **16** |
| Electric input | **1** |
| **TOTAL** | **651** |

Distribution: Kentatsu 332, Midea 250, IGC 60, Daikin 8, Bosch 1. Started from **800** open core fields in Stage21; Stage22 -107, Stage23 -39, Stage24 -3 = **651**. The three maximum-current additions are outside the earlier core checklist. The 651 count is **not** complete coverage of all 77 conditionally applicable columns.

## Open conflicts — NEVER GUESS
1. Midea MI2 Q4/Q4C similar international/Russian model codes denote different powers; do not cross-copy.
2. Kentatsu KZA30 two manufacturer catalog editions disagree on gas pipe; KZA30/KZA40 net masses also differ.
3. Kentatsu KTGB18 gas piping 9.52 vs 12.7 mm editions.
4. Daikin FXMQ200A/250A regional catalogs vary in mass, dimensions and electric input.
5. IGC IMS-BS45NH(DC) unit body vs packaging dimensions.
6. Midea MIH160/180Q4 panel thickness 55 vs 65 mm in editions, and MIH90GHN18(DP) pipe editions.
7. OEM warranty distinct from regional distributor / seller warranty. Do not fill generic "3 years" blindly.
8. Stage22 PDF links trace to exact user's product source rows, but each linked document still needs exact model/edition and page-view audit.
9. Full domain-by-domain search on every one of the user's priority sites for all 356 models and second WEB-pass for all applicable empty/partial/uncertain values remain **UNFINISHED**.

## Durable public GitHub artifacts (confirmed)
- **[Complete Stage25 XLSX, direct raw download](https://raw.githubusercontent.com/kubenkoi97-cmyk/work-files-public/main/climate-mixed/2026-10-15/MIXED_356_77cols_STAGE25_QA_LONG_SESSION_2026-10-15.xlsx)** — actual XLSX **928,544 bytes**, SHA-256 `bd2d422fbf93e3ac718e10a9a6abc46682c6aecf8331776adcb5b8e1b51134e0`, Git blob SHA `eb8952e56f111501d30b0fb6d625e29b32eba63d`; created with Git binary blob and verified from repository directory listing.
- [152 field-level changes](STAGE25_152_SOURCE_PATCH.csv)
- [651 remaining core applicable cells](STAGE25_OPEN_651.csv)
- [356-model row audit](STAGE25_356_MODEL_AUDIT.csv)
- [77-column fill/applicability overview](STAGE25_77_FIELD_COVERAGE.csv)
- Current source of truth for continuation is THIS XLSX plus preceding immutable GitHub manifests and source/evidence logs.

## Next recommended model-family batches
1. Resolve 71 missing pipe pairs with exact Russian-model factory technical sheets and cross-check retailer-only Stage24.
2. Resolve 78 remaining refrigerant model/region values, without inferring a refrigerant from a shared indoor unit brochure listing multiple options.
3. Confirm 20 cassette panels with exact accessory SKU plus dimensions; 10 net weights and 16 body dimension entries with unit-vs-panel distinction.
4. Inspect all 107 recovered FILE PDF URLs for actual exact model and edition, replacing generic links if needed.
5. Confirm 341 manufacturer warranty terms only where OEM documentation explicitly applies, or leave unresolved with documented reason.
6. Regenerate all 356×77 structural, field-level applicability, and exception audits after every batch and publish next full binary XLSX plus file-level patch.
