# Stage46 — Kentatsu KTZV60HZBN1 / conditional max current / 2026-10-19

**IN PROGRESS, NOT IMPORT-READY.** The user requires repeat anti-skip passes across every applicable one of 77 characteristics.

## Exact-model verification

- Target source Excel row **65** = exact `KTZV60HZBN1` (Kentatsu KTZV VRF 600×600 cassette block).
- Target field column **73** `Максимальный ток, А`: was empty, set to **0.65 A** from a directly-opened **exact-SKU** dealer specifications table [Envok](<https://envok.ru/catalog/konditsionery_split_sistemy/vrf-sistemy/vnutrennie-bloki-vrf/vnutrenniy-blok-vrf-sistemy-kentatsu-ktzv60hzbn1-daichi-28775/>); QA status `RETAIL_VERIFIED_OEM_PENDING` (not certified manufacturer visual). The page says **0,65**; output stored numeric **0.65**.
- Cross-check original FILE source and existing Excel **cold capacity 5.6 kW / heating 6.3 kW / R410A / existing liquid+gas 6,35/12,7** against same exact seller specification. Those values match.
- **Critical source text discrepancy:** seller's generic opening prose claims a 1.5 kW block, contradictory to keyed KTZV60 capacity of 5.6 kW. This appears to be reused from KTZV15. Do not take any numerical descriptions from reused marketing prose; use only exact row-level specifications and continue OEM validation. This caveat is recorded in `STAGE46_VENDOR_TEXT_MISMATCH.csv` for importer QA.
- No other fields were modified. No vendor warranty generalized or SKU cross-fill.

## Actual Excel artifact and QA

- Complete updated workbook `MIXED_356_77cols_STAGE46_KTZV60_EXACT_CURRENT_QA_2026-10-19.xlsx` **622738 bytes**, SHA256 `b72b39a87933256e0eaaeda73ae93cebf4f1219770c063a716d8dfd9c9b85d1c`.
- **Created on top of Stage45**, which itself descended from latest technically edited Stage43 (not obsolete Stage39/42 snapshot).
- `artifact_tool` export and **reimport** verification performed: **356 output SKUs ×77 exact column headings**; previous 40 workbook sheets preserved, added 4 new QA sheets, now **44 sheets**. 356×77 workbook output regression: exactly **one** old-empty→new numeric change at BU65, **0** previously nonempty overwritten, unchanged product order, no changes to other output cells.
- QA46: `QA46 точный ток KTZV60`, `QA46 77 колонок`, `QA46 356 повторный аудит`, `QA46 сводка`. Original `Источники` and `Log` append-only entries updated for this exact value. CORE open ledger `QA44 открытые 614` revalidated: each of 614 exceptions remains an actually empty cell.
- **GitHub connector limitation**: binary workbook exists as ChatGPT sandbox file but was NOT actually transferred as .xlsx to GitHub. Only this markdown, patch, audits and manifest are published in GitHub. Do **not** mislabel the Stage39 historical workbook as current.
- Manufacturer original catalog page was **not visually examined** for maximum current.

## Three-stage batch totals (Stage44→46)

| Metric | Result |
|---|---:|
| Newly filled cells across Stage44–46 | **38** |
| Prior nonempty changes | 0 |
| Stage44 newly filled | 2 (KTZV15 col23 pipes; col73 current) |
| Stage45 newly filled | 35 (exact original FILE color) |
| Stage46 newly filled | 1 (KTZV60 current) |
| Exact output product rows | 356 |
| Header columns | 77 |
| Color filled | 56 (Stage43 baseline 21) |
| Max current filled | 26 (Stage43 baseline 24) |
| CORE applicable blanks Stage43→46 | 615→**614** (color/current not in old core denominator) |

Open CORE: warranties **341**, technical docs **106**, pipes **65**, refrigerant **63**, cassette panels **20**, net masses **3**, body dimensional values **16**, nominal input **0**. **614** total core only; additional conditional applicable fields await exact model determination, including 330 physically blank max-current cells with unknown relevance. Previously flagged nine Midea R32/R410A disagreements, two Daikin FXKQ 17 vs18 kg and one Kentatsu KTLV15 1.8 vs1.5 kW remain open. Stage46 adds a seller-description internal contradiction (not necessarily a distinct model specification conflict), which must not be used as a source of false 1.5 kW.

## Next exact searches
1. Obtain original Kentatsu model-specific OEM Russian document `KTZV60HZBN1`, verify **maximum 0.65 A** and panel/accessory applicability, resolve inaccurate seller prose; do not confuse automatic protection ratings with electrical max current.
2. Repeat FILE→COLUMN extraction for remaining 356, especially 65 piping / 63 refrigerants / 20 cassette panels / 3 masses / 16 dimensions. For each unresolved field, log actual model code and domain/source outcomes, not blanket `NOT_FOUND`.
3. Revisit 35 Stage45 FILE-only white-color values with exact regional manufacturer/retailer execution and whether panel colour is independent.
4. Complete actual all **77 columns per item** applicability classifications; one blank does not imply missing if not applicable, nor does populated guarantee correct. Recheck previously filled potentially wrong data just as actively.
5. Archive complete binary & logs after each patch; keep previous versions immutable. The current binary itself is available through ChatGPT sandbox, GitHub text logs preserve reproducible changes.
