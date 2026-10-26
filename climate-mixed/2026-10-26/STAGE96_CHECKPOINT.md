# MIXED Stage96 — FXKQ63A own exact-model marketed area (2026-10-26)

**Validated full XLSX:** `MIXED_356_77cols_STAGE96_FIRST50_DAIKIN_FXKQ63_EXACT_AREA_2026-10-26.xlsx` **814190 bytes**, SHA256 **`82112cbfa6a01b0cb971bcca051f30c61c79fca6d81124fe06831fca1625cd8c`**, **67 sheets**. Stage95 parent SHA256 `24b5ff469fc2202cac8fbba74f955b128ed2a7972899dec0baf42280d999bdfc` (66 sheets).

Only one product value changed: Excel row42 exact short `FXKQ63A`, column14 (`N42`) empty -> **71 m²**. Exact own SKU merchant page https://mircli.ru/Daikin-FXKQ63A/ literally identifies model and lists separate `Площадь, м²` = 71. This is marketing area; **not** thermal load calculation, and not borrowed from `FXCQ63A`, `FXKQ63M`, or another model. Previous Stage67 had removed unsupported different-model area; now this is a genuinely exact own-SKU source.

Existing values confirmed by same retailer as source-of-lower-confidence: cooling 7.1kW, heating 8kW, airflow 1290 m³/h, minimum sound 38.5dB(A). Retailer **contradicts** existing Stage95 `R42=0.118kW` with `0.095kW`, and `AA42=R410A` with `R32`. **NO editing these critical conflicted values.** Factory original market/production version is required. Merchant also states 1 year warranty; `AO42` remains empty pending Daichi supply contract and valid commissioning terms. Original factory sourcing > merchant single page, do not mix European VRV equipment and Russian shorter codes.

Independent full OOXML re-import of Stage95 and Stage96 compared all **356×77=27412** product cells: **exactly one changed N42**, **zero changes among protected other306 rows52-357**, all old 66 sheets' values preserved; one new `QA96 Daikin FXKQ63 exact 71` sheet added. Physical first50 filled **1635→1636** (includes N/A), 40 historic CORE still open and other Daikin conflicts. **READY_FOR_IMPORT 0/50**, no false technical readiness.

**Binary XLSX exists in ChatGPT download only**; repository text ledger is not the binary file.