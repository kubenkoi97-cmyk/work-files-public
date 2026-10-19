# MIXED Stage 50 — exhaustive second FILE color extraction and correct indoor/outdoor identification (2026-10-19)

**INTERMEDIATE; NOT IMPORT-READY.**

## True parent and workbook integrity
- Parent binary: `MIXED_356_77cols_STAGE47_KTLV15_EXACT_PIPES_2026-10-19.xlsx`, 640092 bytes SHA256 `91ce58730c4f8d27091d450aa3f58d213a9940fd4ba335e631ffc24b33e9ac48` (full original 47-sheet archive).
- New, actually exported and separately re-imported full product-data XLSX: `MIXED_356_77cols_STAGE50_FILE_SOURCE_16_COMPACT_2026-10-19.xlsx`, **393670 bytes**, SHA256 **`3ff08786d7999c677a4cfff8b311cecb33151759a29c7afaae24d2a4ff55bf68`**.
- Output exactly **356 products ×77 original columns**, original product codes/order unchanged. Cell-diff against Stage47: **16 formerly blank fields filled, 0 previously nonblank values overwritten**. Color filled **56→71**; Type of block filled **355→356**. Exactly **613** baseline core applicable blanks remain open.
- New compact file has **11 tabs**: original complete product table, original source descriptions and characteristics, extended Источники and Log, Карта сайтов, latest original 11-model conflict audit, new 613-core open ledger, 16-patch audit, 356-model report, 77-field report, and Historical Archive notice. Historic normalization and other prior QA tabs are NOT copied into the compact file but **all remain in the full unchanged Stage47 binary archive** (this is a deliberate documented compact migration after repeated `artifact_tool` RPC exporter failures on 47-sheet source; not a silent data loss).
- New XLSX reimport independently verified: 11 tabs, 357 output rows incl header, 77 columns, 71 white-body entries, outdoor Bosch code and 613-row open register. The binary is available as **ChatGPT sandbox attachment, NOT uploaded to GitHub**. GitHub connector cannot read local XLSX binary in this session. Do not fabricate remote XLSX availability; repository stores CSV/Markdown QA evidence.

## Verified individual source-to-column changes
- **9 Kentatsu KTGB** exact SKUs (Excel rows **101–109**) have literal `Цвет корпуса: белый` in their own original FILE sources `Сбор данных!F101:F109`. Wrote standardized `Белый` to column **22** for each.
- **6 Midea MI2-Q1DHN18(At)** exact SKUs (rows **274–279**) have literal `Цвет корпуса: белый` in their own original source `F274:F279`. Wrote standardized `Белый` to column 22.
- **Bosch MDCI 12-1** is explicitly described as `Исполнение: наружный блок мини-VRF` in `Сбор данных!F357`; column 54 already `наружные блоки`, while column **55** `Тип блока` was empty. Filled **`наружный`** only for exact row 357.
- All 16 changes preserved field-level origin cell, verbatim phrase, and pending independent web/market confirmation in `Источники` and `Log` plus [patch CSV](STAGE50_FILE_EXACT_PATCH_16.csv). This is **FILE_EXACT_TEXT**, not fake `OEM_PAGE_VERIFIED`.

## Important anti-skip: deliberately REJECTED 7 false positives
Seven **Midea MI2-Q4CDHN18(At)** SKU source texts (rows **280–286**) explicitly say **`Цвет панели: белый по продавцу; цвет скрытого корпуса отдельно не подтверждён`**. They cannot be filled as `Цвет внутреннего блока`; using panel color in body color would be a wrong specification. These **7 remain empty**. Detailed [rejected-candidate ledger](STAGE50_REJECTED_SOURCE_MATCHES.csv).

## Other fields and conflicting source scope
- Kentatsu **KZA30/KZA40HZAN1** has exact original FILE `Масса корпуса (нетто): 15,5 кг`, but earlier factory-catalog revision mass/heat/pipe conflicts exist. OEM 2025 catalog PDF was not visually opened and different seller versions disagree; **both remained blank**.
- Midea **MI2-22Q1DHN18(At)** exact standalone retailer lists 10 kg net, while a unit+panel set lists unqualified 12 kg; no unconfirmed or package value was transferred.
- Bosch MDCI 12-1 source says 95 kg and existing column 38 correctly identifies **outdoor unit weight 95 kg**. Do not mechanically populate an indoor-body net-weight field 37 from this outdoor value; avoid counting that as a genuine missing core mass.
- The existing 9 Midea refrigerant R32/R410A and two Daikin weight disputes and KTLV15 heat 1.8 vs1.5 remain OPEN. Newly filled fields did not close them.

## Next-stage priorities
Fully research remaining **613 baseline core applicable**: manufacturer warranty341, exact PDF links106, pipe pairs64, refrigerant63, panel dimensions20, body net masses3, dimensional parts16, nominal electric input0, plus all conditionally applicable parameters in columns1–77. Every nonapplicable field needs individual QA, not zero filling. Original PDFs must be visually inspected before elevating indexed-factory data to OEM_PAGE_VERIFIED. Stage50 was FILE recovery and global structure QA, **not completion of the per-model web second pass**.
