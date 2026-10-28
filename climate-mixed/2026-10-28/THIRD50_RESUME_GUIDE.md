# MASTER RESUME GUIDE — MIXED THIRD50 products 101–150
**Date 2026-10-28. New owner decision overrides Stage101–108 older prompts.**

## Mandatory scope and protected data
Process ONLY product numbers 101–150, corresponding to rows 102–151 in the existing worksheet `Наполнение MIXED`.
Freeze previous products 1–100, rows 2–101, **as-is**. Freeze future products 151–356, rows 152–357. This totals 306 protected records. Never silently fix, delete, sort, move, rewrite old descriptions/SKUs/images/prices or assign READY_FOR_IMPORT to frozen products. Stage108's 29 open pipe pairs belong to PREVIOUS protected batch 51–100; they remain open in historical audit, NOT part of this third-batch workload. Owner's freeze is an administrative scope decision, not verified technical readiness.

## Canonical source
Latest complete binary XLSX is `MIXED_356_77cols_STAGE107_NEXT50_EXACT3_SYSTEM_INVERTER_COLOR_2026-10-27.xlsx`, SHA256 `0332af716d9284fdb270d01464e1aca65420fdd1ccff9900a9b0e2a9cadfec19`, size 1,106,927 bytes, 79 worksheets, 356 goods x77 fields. Full workbook is in this ChatGPT conversation's verified handoff ZIP; **NOT available as a GitHub binary**. Stage108 was audit-only and did not change the canonical XLSX. Do not recreate the 79-sheet workbook from GitHub CSV/MD files. New actual full export normally starts at Stage109 (only after verified save); name with THIRD50_101-150 and actual date.

## Exact roster; only these series
KTGB: 8 (24,30,40,50,60,72,80,90) products 101–108
KTYB: 7 (18,24,30,40,50,60,72) products 109–115
KTDB: 6 (24,30,40,50,60,72) products 116–121
KTZB: 7 (18,24,30,40,50,60,70) products 122–128
KTVB: 12 (30,40,50,60,72,80,90,100,115,140,160,180) products 129–140
KTLB: 10 (18,24,30,40,50,60,72,80,90,115) products 141–150
Each SKU ends with HZBN1. Exact row-by-row mapping is in `THIRD50_EXACT_ROSTER_50.csv` in this repository path.

**IMPORTANT**: For the preceding second batch, old KTYB/KTVB/KTLB manufacturer tables were rejected since those 51–100 products were *V-series* (KTYV/KTVV/KTLV). Here products 101–150 **ARE B-series**. These factory catalog tables may be directly relevant now, but only if the printed row has EXACT SKU/revision and measurement conditions. Do not conflate KTKB with KTLB. Same numerical capacity is not exact provenance.

## Verified Stage107 baseline for this active 50
* 50 x 77 = 3850 fields, 1508 physically filled and 2342 empty, status not yet certified.
* 50/50 exact SKUs exist in same-row `Сбор данных!C102:C151` and match titles and lowercased symbolic codes; target `Наполнение MIXED!F102:F151` is **50/50 blank**.
* Pipe pair W: 50/50 physically filled; **review truth**, do not add old unrelated 29 missing.
* Inverter M 0/50, area N 0/50, contractual warranty AO 0/50.
* Panel dimensions AZ 32/50, max external static pressure BA 10/50 (category dependent).
* Tech documentation AQ and detailed description AT both physically filled 50/50: must validate exact SKU, accessibility, content, accuracy.
* Availability AU=100 and purchase AV=0 and retail AX=0 across 50 are **150 placeholders, not validated commerce**. Never mark ready by assuming genuine inventory/price.
* `Сбор данных!B:C:D:E:F:G:H:I:J` all populated for these 50 rows. Read full same-row data, product-specific links in G and historical QA before web search.

## Immediate first real pass
1. Hash-check and open full 79-sheet workbook, preserve 356×77 positions and all current sheets, compare exact 77 headers.
2. Protect product ranges 2:101 and 152:357 read-only and snapshot them.
3. Cross-check each exact code `Сбор данных!C<row>` against `Наполнение MIXED!B/C<row>`; if matching, restore exact literal article in `F102:F151` (50 expected changes). Do not alter normalization of final article string.
4. Expand each source row E/F/G into atomic technical facts, measuring conditions, own model and URLs. Fill already proven empty fields in same target SKU only. Existing populated fields require provenance review, not automatic acceptance.
5. Full WEB/OEM pass: consult Kentatsu DX PRO VII exact B-series factory tables; source candidate https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf and Daichi https://daichi.business/support/documents/download.php?ID=27751. They were present in original source; open, inspect PDF page/table and exact variant. Search same-row vendor pages such as MirCli, CoolSochi, effect-nn. A PDF indexed snippet is not OEM visual confirmation.
6. Work series in batches KTGB8, KTYB7, KTDB6, KTZB7, KTVB12, KTLB10. For cassettes verify body vs separately ordered panels/controls (bundle SKU != indoor SKU), drain, dimensional orientation. For ducted KTLB verify nominal ESP vs maximum ESP. Confirm pipes W, max current BU vs operating current, exact electrical ratings, sound pressure vs sound power, manufacturer warranty, real images.
7. For every product make field-level 77 QA with EXACT_OEM / EXACT_RETAIL / FILE_NEEDS_OEM / CONFLICT / CONDITIONAL / TRUE_NA / OWNER_COMMERCIAL. Two anti-skip passes: file facts -> field mapping and each applicable target field -> exact proof. No guesses, no silent N/A, do not take V-series figures for B-series.
8. Verify full export after writing using independent OOXML read and compare ALL 356 x 77 = 27412 product positions. Expect changes only in rows 102–151, **zero changes in 306 protected products**, previous 79 sheets intact. Changes in populated cells must carry old->new patch, exact SKU proof and conflict reason. Formula/format checks.
9. Publish full valid new Stage109 XLSX and truthful source/patch/readiness/conflicts logs; post checkpoint in existing public repo `kubenkoi97-cmyk/work-files-public`, path `climate-mixed/<current date>/` naming `THIRD50_101-150`, verify readback. Only upload public work technical material; no confidential data. If binary cannot be uploaded to Github, provide verified ChatGPT download and state GitHub has only text logs. Never claim work queued or website published without evidence.
10. Report in Russian: exact models, real newly filled fields, corrected values, OEM verification, blockers, TECH_READY and READY_FOR_IMPORT (do not invent), 306 protected unchanged, working XLSX/ZIP links and verified GitHub links.

## Evidence and terminology pitfalls
- Exact suffix HZBN1 and exact series, DX PRO VII, actual factory table row and region/revision required. KTYV ≠ KTYB; KTVV ≠ KTVB; KTLV ≠ KTLB; KTKB ≠ KTLB.
- Liquid/gas in W ordered millimetres; do not substitute drain, water thread, pipe run or analogous family.
- R nominal input kW ≠ BT maximum kW ≠ BU max current A. 0.5 A operating current is not automatic max current.
- AC AD AE AI are body W×H×D; AZ is face panel; mounting hole and package sizes differ. Panel in exact dealer bundle URL does not mean it is included with standalone indoor unit.
- BA means maximum external static pressure on ducted unit; distinguish nominal and adjustment range.
- N retail recommended room area is not engineered space sizing; no kW×10 inference.
- Inverter belongs to VRF system, not separate compressor in indoor evaporator. Wi-Fi option != factory-installed.
- AO warranty is contractual; AU, AV, AX are CMS owner data, existing 100/0/0 are placeholders. Do not publish without validation.

## Deliverables after each substantive package
- `MIXED_356_77cols_STAGE109_THIRD50_101-150_...xlsx` as genuine full workbook.
- `STAGEXX_THIRD50_FIELD_PATCH.csv`, `STAGEXX_THIRD50_SOURCES.csv`, `STAGEXX_THIRD50_FIELD_QA_50x77.csv`, `STAGEXX_THIRD50_OPEN.csv`, `STAGEXX_THIRD50_CONFLICTS.csv`, `STAGEXX_THIRD50_READINESS.csv`, `SESSION_MANIFEST_XX_THIRD50.md`, `STAGEXX_CHECKPOINT.md` plus full ZIP.
- Real SHA256 / file size / number of sheets and 27412-cell regression. Only TECH_READY_COMMERCIAL_BLOCKED after tech proof; READY_FOR_IMPORT only when both technical+commercial gates truly passed.

**Start doing work now: full book preflight, article restoration F102:F151, then grouped exact OEM verification and verified Stage109. Do not ask for instructions already in this handoff.**
