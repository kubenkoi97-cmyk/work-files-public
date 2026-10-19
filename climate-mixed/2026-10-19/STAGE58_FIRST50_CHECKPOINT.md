# MIXED Stage58 — FIRST 50 ONLY — field applicability, evidence quality and import gate

**Date 2026-10-19. Intermediate; no SKU is marked READY FOR IMPORT.** Source working book was Stage55, never restarted from Stage39/42. The changed product area is *strictly rows 2–51*; rows 52–357 (306 items) were verified unchanged in an actual cell-by-cell diff.

## Actual binary outputs (local ChatGPT sandbox, not GitHub binaries)
- **Stage56**: `MIXED_356_77cols_STAGE56_FIRST50_SELLER_WARRANTY_CORRECTION_2026-10-19.xlsx`, 425283 B, SHA256 `498f055b55806eb9c0b7994fb3bf1c4c535e0685055b6e7dae8a1ab5b22e190b` — removed 8 existing 12-month seller-only warranties incorrectly appearing as manufacturer's guarantee; complete original source / old value kept in append-only Log and QA56.
- **Stage57**: `MIXED_356_77cols_STAGE57_FIRST50_42_INSTALLATION_MODES_2026-10-19.xlsx`, 431818 B, SHA256 `db234bd02f6896312879857565517de2863ea7b3217c55b3bb844845e972f4e9` — added 42 formerly empty installation-mode cells from *each exact model's* original FILE descriptions, preserved 8 installation cells already filled.
- **Stage58 (LATEST)**: `MIXED_356_77cols_STAGE58_FIRST50_50x77_DEEP_QA_2026-10-19.xlsx`, **704681 B**, SHA256 **`bc2544a8967faaf9c6754db60871f1824a5cefc2c04487ba9125cf28d978a389`** — 23 sheets with complete original 356×77 product data, original source tab unchanged, append-only `Источники`/`Log`, and new QA56, QA57, QA58 sheets. Export reopened with `artifact_tool` and by independent XLSX XML comparison.

### Scoped regression outcome
- **50 product-cell changes total** against Stage55: 42 old-empty→new installation, **8 old seller warranty→blank**. No other nonempty technical value overwritten. No product order/header change.
- **0 changes to any of the remaining 306 product rows** (each of their 77 fields verified individually). The entire original `Сбор данных` worksheet was also compared bytewise at logical cell/value level: unchanged.
- 50 selected SKU: IGC35, Daikin8, Kentatsu7; first `IMS-K22NH(DC)`, last `KTGV72HZBN1`.
- **3850 field-specific QA rows** (50×77) exist in `QA58 50x77 применимость` and accompanying ChatGPT CSV; includes 50 model readiness rows, OEM revision log, source/coverage notes.
- **50/50 models still NOT_READY.** A populated field is not automatically OEM-verified; a non-applicable field must be supported per equipment class and finally validated per model.

### 3850 individual field classifications (do not misread physical blanks)
| Group | Cells |
|---|---:|
| Physically populated | **1527** |
| Blank, provisional N/A by indoor-unit class | **1071** |
| Blank, commercial/source-owned and not WEB-replaceable | **350** |
| Blank CORE high-risk or previously invalid manufacturer warranty | **76** |
| Blank remaining, applicability/OEM investigation or whole-system dependent | **826** |
| **Total** | **3850** |

The 1071 N/A are *provisional by class*, not final model-specific exclusions. The 826 are NOT 826 certified missing technical specs; this includes accessory/system dependence and source applicability. All 50 retail prices are 0 in original FILE (commercial source-only), so **price confirmation** remains a separate website-import blocker, not permission to scrape new prices.

### Important source conflicts and further work
- **IGC 35**: original `(DC)` suffix is not `(DC4)`, `(DC5)` or `(DC7)`. Exact historical OEM PDF tables can be retrieved as search-indexed text, but the actual original PDF fetch returns **502**. Six wall-unit refrigerants and others cannot be copied from other revisions. `IMS-BS45NH(DC)` body dimensions are uncertain: indexed exact-source lists body 700×470×200 against 1305×580×275 packaging; original visual and edition QA remains OPEN.
- **IGC manufacturer warranty new lead**: an indexed manufacturer-hosted `Full DC Inverter` manual says **12 months factory warranty** plus conditional 36 months (maintenance), corroborated by full official dealer warranty policy. However the PDF original was 502, and the exact old `(DC)` market/year applicability is not yet verified. **No blanket 35-warranty fill.**
- **Daikin 8**: opened manufacturer engineering tables for full codes `FXKQ20AMVEB` … `FXKQ63AMVEB` and `FXMQ200AXVMB/250AXVMB`. The user's short `FXKQ20A`, `FXMQ200A` codes must not be assumed to represent the same regional execution: differing nominal input/size/weight are tracked; old-filled numbers retained until exact edition proof.
- **Kentatsu 7**: `KTGV24HZBN1` missing refrigerant pipe pair remains blank; no model-specific OEM PDF page visual available yet. Other stored values continue factory-revision QA.
- Equipment-class conditional checks remain for heat exchangers, IP grade, maximum currents and actual compatibility with outdoor VRF; never treat 15 A breaker as max electrical current, or a DC fan as inverter compressor.
- `0` retail price / `100` nominal stock entries should be confirmed by original commercial source, never replaced by internet sellers.

## Files in GitHub
- [Stage56 source corrections](STAGE56_FIRST50_WARRANTY_8_PATCH.csv), [Stage56 report](STAGE56_FIRST50_CHECKPOINT.md).
- [Stage57 42 additions](STAGE57_FIRST50_42_INSTALLATION_PATCH.csv), [Stage57 report](STAGE57_FIRST50_CHECKPOINT.md).
- [Stage58 50 product coverage](STAGE58_FIRST50_50_MODEL_COVERAGE.csv), [source events](STAGE58_FIRST50_SOURCE_QA.csv), this Stage58 report and handoff.

**Binary publication limitation:** GitHub connector writes UTF-8 text files, but cannot read/transmit local XLSX bytes. Therefore GitHub **does not contain the new XLSX binary**. The exact current binary and full 3850 CSV are available as this ChatGPT's sandbox downloadable files; do not fabricate GitHub links. Next resumed worker must work from Stage58 binary, not older Stage55, and preserve all historical snapshots. 
