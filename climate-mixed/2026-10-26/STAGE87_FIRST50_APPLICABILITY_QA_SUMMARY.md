# Stage87 exact first50 × 77 applicability matrix — conservative audit (2026-10-26)

Original complete workbook: MIXED_356_77cols_STAGE87_FIRST50_IGC_QV56_EXACT_AREA_2026-10-26.xlsx, 793317 bytes, sha256 1376b700e160afe02f1b7895769df4c3f86926029291f0f517f292257c6f7615. Exported full workbook is available in ChatGPT, **NOT** as a GitHub XLSX binary.

Generated CSVs in ChatGPT: STAGE87_FIRST50_APPLICABILITY_3850_2026-10-26.csv (3,850 rows) and STAGE87_FIRST50_READINESS_50_2026-10-26.csv (50 SKU). The GitHub connector in this session cannot ingest the local CSV bytes directly, so this is the published QA digest.

| Classification | Cells | Interpretation |
| --- | ---: | --- |
| Present original model value, OEM final verification open | 1,323 | Do not claim OEM visually verified |
| Provisionally not applicable by refrigerant indoor unit type | 950 | **NOT** individually OEM verified N/A |
| Unfilled conditional / applicability open | 537 | Accessories and whole-system dependencies |
| Other open source/applicability | 396 | Need own SKU source or N/A proof |
| Owner-controlled commercial blanks | 300 | No internet-sourced substitutes |
| Owner-controlled commercial values present | 250 | Original preserved |
| IGC warranty existing, historic scope uncertain | 35 | Existing 12 months not automatically certified |
| Blocked old IGC DC refrigerant | 21 | Historic factory/outdoor system evidence needed |
| Blocked Daichi warranty contracts | 15 | Contracts/commissioning |
| Existing system-conditional values needing QA | 13 | Do not treat as verified system-independent |
| Blocked IGC BS45 cabinet dimensions | 4 | Independent factory drawing |
| Exact newly sourced marketing areas | 4 | Stage85 QV125/QV140, Stage86 FXKQ50, Stage87 QV56 |
| Exact new max operating currents | 2 | Stage84 KTGV24/KTGV60, OEM visual pending |
| **Total** | **3,850** | **50 × 77** |

**Physical fill** now 1627/3850, remainder includes N/A, conditional and shop-controlled fields; this is not a technical completeness percentage. 40 historic CORE blockers remain, plus regional edition and other technical QA. **0 READY_FOR_IMPORT, 0 technically certified TECH_READY_COMMERCIAL_BLOCKED**. Other 306 out of scope product rows remain unchanged according to independent full 356×77 Stage83→Stage87 comparison. This matrix is classification triage only, not individual OEM N/A certification.

Read source for details: STAGE87_CHECKPOINT.md, STAGE87_FIRST50_FIELD_PATCH.csv, STAGE87_SOURCES.csv, STAGE87_CONFLICTS.csv and SESSION_MANIFEST_87_FIRST50.md.