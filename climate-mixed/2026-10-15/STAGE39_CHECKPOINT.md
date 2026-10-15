# Stage 39 — Full 356 x 77 regression and binary XLSX

**2026-10-15. INTERMEDIATE; NOT READY FOR CATALOG IMPORT.**

- Source book: `MIXED_356_77cols_STAGE33_QA_2026-10-15.xlsx` (existing immutable public backup).
- New book: **[MIXED_356_77cols_STAGE39_MIDEA_DEEP_QA_2026-10-15.xlsx](https://raw.githubusercontent.com/kubenkoi97-cmyk/work-files-public/main/climate-mixed/2026-10-15/MIXED_356_77cols_STAGE39_MIDEA_DEEP_QA_2026-10-15.xlsx)**.
- Published as a real binary XLSX, **483,530 bytes**, Git blob `16b8779680bdb25273e18b1f499219a29a5de297`, SHA256 `ed5918460aa74738c225fd15cc8b8426261ae0fea08bbb6053a951bc78c187d1`; checked GitHub public directory listing for exact blob and length.
- Exactly **356 products**, **77 output columns**, original row ordering and existing output values retained. Cell-by-cell old vs new comparison: exactly **13 changes**, all originally blank. No nonblank overwrite.
- **Stage36:** six core fields (1 electric input, 5 unit net mass). **Stage37:** seven additional conditional max-current fields. **Stage38:** three refrigerant conflicts tracked and highlighted, no value changes.
- Core applicable blank count **631 → 625**, counted from actual blank cells. All 625 open-field records point to cells still actually empty. They are *not* proof that all 77 conditionally applicable fields have been exhaustively reviewed.
- Additional audit sheets `QA36-37 точные поля`, `QA38 спорный фреон`, `QA39 открытые 625`, `QA39 356 моделей`, `QA39 77 колонок`, `QA39 сводка`, and appended model/field source URL evidence to existing `Источники` and `Log`.
- All product descriptions preserve existing five-section HTML; no new formula errors found by Excel pattern scan.

## Remaining 625 *core* applicable blanks
| Field | Count |
|---|---:|
| Manufacturer warranty | 341 |
| Exact model TECH_DOCUMENTATION | 114 |
| Refrigerant | 63 |
| Refrigerant tube pairs | 66 |
| Cassette panels | 20 |
| Net weight | 5 |
| Indoor/outdoor dimensional parts (4 models × 4 fields) | 16 |
| Nominal electric input | **0** |
| Total | **625** |

Saved audit CSVs: [13 changes](STAGE36_37_EXACT_MODEL_FIELDS.csv), [3 refrigerant conflicts](STAGE38_MIDEA_DLD_CONFLICTS.csv), [625 open cells](STAGE39_OPEN_625.csv), [356-model coverage](STAGE39_AUDIT_356.csv), [77-column fill overview](STAGE39_77_COVERAGE.csv).

## Unfinished QA
- Some dealer sources disagree on refrigerant, so full OEM market-version verification required, including pipes and warranty.
- Recovered technical manuals and many model-field entries from earlier sessions remain `PDF_VISUAL_QA_OPEN`; do not claim full completed file → WEB second pass.
- All user-listed priority sites for each model and all 77 conditionally applicable properties remain to be checked.
- Do not call final or production-import safe.
