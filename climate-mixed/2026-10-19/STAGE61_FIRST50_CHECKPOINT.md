# Stage61 — first50 IGC exact wall DC original PDF visual check (2026-10-19)

**Intermediate; 0 READY, only first50 scope rows2–51.** The manufacturer-authored wall-unit catalog at https://onokom.ru/dok/igc/2024/catalog/2024-catalog-ims-wall-dc.pdf was **actually opened and visually inspected**, **printed page 40 / PDF page 3** (screenshot pageno2). This is manufacturer-branded original page **mirrored by Onokom**, not official manufacturer-domain hosting. Document page lists six exact original `IMS-K…NH(DC)` model suffixes.

## Six exact models and 48 model-field matches
Excel rows 2–7: `IMS-K22NH(DC)`, `IMS-K28NH(DC)`, `IMS-K36NH(DC)`, `IMS-K45NH(DC)`, `IMS-K56NH(DC)`, `IMS-K71NH(DC)`.

For each individual exact model the following eight **already populated** output fields were rechecked against the actual visually viewed factory table: cooling kW col16, heating kW col17, nominal electrical input kW col18 (20/30/40W normalized 0.02/0.03/0.04), HI fan air flow col20, **LOW FAN sound pressure** dB(A) col21, body dimensions `Ш×В×Г` col35, net (not gross) weight col37, liquid/gas tube pair in mm col23. **48/48 comparison rows MATCH exactly.** The existing row2 27dB and row7 37dB are LOW fan noise, not HIGH fan noise: e.g. model IMS-K22 source says 38/33/27 (High/Mid/Low), output field currently uses 27. Preserve current values, but note the semantics for downstream site display and any future recheck.

The source does not provide conclusive full-system refrigerant identity or historical OEM warranty policy applicability, so these remain OPEN. No warranty or gas guesses from neighboring DC5. No source numerical value was changed.

## Tested binary and scope
- Stage61 full workbook `MIXED_356_77cols_STAGE61_FIRST50_IGC_WALL_OEM_VISUAL_QA_2026-10-19.xlsx`, **722275 bytes**, SHA256 `99712ecda0dee9d90e115c7fc98152bc4b14fc0a61529a65b765a6647561191e`.
- Parent Stage60 `MIXED_356_77cols_STAGE60_FIRST50_IGC_QV_OEM_VISUAL_QA_2026-10-19.xlsx`, 718739B, SHA256 `d060f03d7aec9aa0b2d4d609c5891351cc4239197662b162189d11ed32d5b2a2`.
- Stage61 added `QA61 IGC WALL DC завод` sheet containing 48 exact checks, eight-column source trace appended for the 6 SKUs to `Источники` and `Log`. Independent XLSX-XML full **356×77 value regression equal** (0 product-value changes, 306 other SKU untouched). Full old history/source work preserved.
- In combination with Stage60 floor/ceiling OEM visual checks: **14 distinct first50 exact IGC models × 8 fields =112 individually verified already-populated technical values**. These are verified *specific fields*, not 14 production-ready models.
- Stage59 figures unchanged: 50 targeted SKUs, **1562/3850 physically populated**, 41 core warranty/doc/refrigerant and other high-risk issues, 826 conditional/whole-system additional investigations (not 826 confirmed missing applicable values). **0/50 READY**.
- XLSX exists as ChatGPT downloadable file only, **NOT** GitHub binary. GitHub contains this checksum, 48-field source evidence CSV and historical versions.

[48 field checks](STAGE61_FIRST50_48_VISUAL_FIELD_CHECKS.csv) · [Stage60 floor/ceiling 64 checks](STAGE60_FIRST50_64_VISUAL_FIELD_CHECKS.csv) · [Stage59 manufacturer warranty stage](STAGE59_FIRST50_CHECKPOINT.md).

## Next
Further original visually-audited PDF pages for other 21 IGC exact block models, plus eight Daikin and seven Kentatsu; particular risks: IGC (DC) refrigerant and BS45 body vs gross package sizes, Daikin region suffix, Kentatsu KTGV24 tubes, OEM warranty applied to actual production year and warranty start, commercial source prices (original zero). Do not edit any of the excluded 306 SKU.
