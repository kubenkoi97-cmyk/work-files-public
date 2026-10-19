# MIXED Stage59 — FIRST 50 ONLY: IGC manufacturer baseline warranty (2026-10-19)

**PARTIAL, NOT READY FOR CATALOG IMPORT.** Scope is strictly the first 50 product rows **2–51** of the canonical Stage55 lineage. Technical changes affect **only 35 IGC rows 2–36**. Other IGC, Daikin, Kentatsu and all **306 out-of-scope products are unchanged**.

## Independent manufacturer policy, evidence quality
- Two **manufacturer-domain** IGC older/full DC Inverter VRF instruction documents at https://igc-aircon.com/upload/iblock/4ac/n32mwonne52y8c1h825ug2ycqtqdtr0x.pdf and https://igc-aircon.com/upload/iblock/ff2/ff22eb7a63da51591eb951cb39c5e266.pdf explicitly state **standard manufacturer's warranty 12 months**, with **conditional extension to 36 months** requiring appropriately documented qualified maintenance.
- An independently opened [official authorized IGC dealer warranty policy](https://igc.com.ru/help/warranty/) corroborates 12 basic months and optional 36 months under maintenance conditions. Dealer terms are **not** treated as proof of unconditionally transferable 36-month manufacturer's warranty.
- The two OEM-hosted PDF documents were only available as **indexed text**; fetching original PDF returned HTTP502. Their exact effective model-year/market applicability to the historical `IMS-…(DC)` variants is **not yet visually confirmed**. Evidence status `OEM_MANUFACTURER_12_MONTHS_BRAND_WIDE_INDEXED_WITH_DEALER_CORROBORATION; ORIGINAL_PDF_VISUAL_PENDING; EXACT_DC_MARKET_CHECK_OPEN`.
- Applied the documented **12 basic months as a provisional manufacturer-wide claim** to **35 previously empty col41 fields** (IGC exact row identities) with source URLs and pending verification recorded in `Источники`, `Log` and an evidence QA sheet. **No 36-month extended warranty was applied**. If edition-applicability evidence contradicts standard policy, revise with documented old/new provenance; do not regard these provisional values as finally approved.

## Binary and regression
- Parent: `MIXED_356_77cols_STAGE58_FIRST50_50x77_DEEP_QA_2026-10-19.xlsx` (704681 bytes, SHA256 `bc2544a8967faaf9c6754db60871f1824a5cefc2c04487ba9125cf28d978a389`).
- Current exported workbook: `MIXED_356_77cols_STAGE59_FIRST50_IGC_OEM_BASIC_WARRANTY_35_2026-10-19.xlsx`, **714425 bytes**, SHA256 **`3e33f8e4a37c6fda98647e2661df200500c89fc50c5fbfa13be642e27ade8fe8`**; accessible as a ChatGPT sandbox file. **Not actually uploaded as binary to GitHub.**
- XML-level cell diff old/new confirms exactly **35 blank→12** column41 changes and **zero** changes to any of the **306 excluded SKU rows** (52–357) or other fields; source worksheet and 77 columns unchanged. Full 356×77 remains intact.
- First50 physically filled fields **1527→1562** (out of 3850); **core open 76→41**; 826 other conditional/whole-system applicability checks remain open in the Stage58 matrix. **0/50 products are certified READY**.
- Cumulative Stage55→Stage59 product changes first50: 42 installation blanks filled (Stage57), 8 prior seller-only warranties cleared (Stage56), 35 brand-basic-warranty values entered provisionally (Stage59) = **85 changed cells**; zero outside target scope. Thus 77 newly filled, 8 unsupported overwritten to blank.
- Old generic service/commercial empty cells and all other source conflicts are retained, no invented costs, no adjacent-revision refrigerants or technical values copied.

## Remaining first50 OEM blocks
IGC exact `(DC)` refrigerants not to be replaced with `(DC4/5/7)` data; IGC BS45 body/package conflict; exact manufacturer's PDF original visual/edition and manufacturer warranty; Daikin FXKQ/FXMQ short code vs full German regional codes; Kentatsu KTGV24 pipe pair; conditional maximum current, exchanger model coil construction/IP/accessories as applicable; all first50 original 0 commercial prices need original merchant confirmation.

**Reproducibility:** [35 field patch](STAGE59_FIRST50_IGC_OEM_WARRANTY_35_PATCH.csv) · [updated 50-model status](STAGE59_FIRST50_MODEL_COVERAGE.csv) · [Stage58 parent](STAGE58_FIRST50_CHECKPOINT.md).
