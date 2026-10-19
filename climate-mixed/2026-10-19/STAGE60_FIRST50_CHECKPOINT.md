# Stage60 — First50 exact original IGC catalogue page visual checks (2026-10-19)

**INTERMEDIATE; NOT IMPORT READY. Only scope: first50 product rows2–51.**

## Important new source access
An original **IGC-branded** floor/ceiling catalog page **49 (PDF page 4, zero-index screenshot page 3)** was successfully **opened and VISUALLY INSPECTED** at https://onokom.ru/dok/igc/2024/catalog/2024-catalog-ims-floor.pdf. The four-page PDF is mirrored by Onokom, and the original page identifies the exact `IMS-QV…(DC)` suffix. Do not conflate manufacturer-authored page with manufacturer-domain hosting: this is **OEM_BRANDED_CATALOG_VISUAL_VERIFIED_MIRROR_HOSTED**, not unverified search snippet, and not proof of all current shipment-year revisions.

### Verified 8 exact IGC models (Excel rows27–34)
- `IMS-QV28NH(DC)`, `IMS-QV36NH(DC)`, `IMS-QV45NH(DC)`, `IMS-QV56NH(DC)`, `IMS-QV71NH(DC)`, `IMS-QV90NH(DC)`, `IMS-QV125NH(DC)`, `IMS-QV140NH(DC)`.
- For **each exact model** visually compared eight independently keyed fields of the 77: cooling kW (column16), heating kW (17), nominal electric input kW (18), HI fan airflow m³/h (20), HI sound pressure dB(A) (21), indoor `Ш×В×Г` dimensions (35), indoor **net** mass kg (37), both refrigerant line diameters liquid/gas mm (23).
- **Exactly 64 individually inspected comparisons; 64/64 match the existing Stage59 product cells.** No mismatch. See [row-and-field exact checks](STAGE60_FIRST50_64_VISUAL_FIELD_CHECKS.csv), archived as its own `QA60 IGC QV DC завод` workbook worksheet and appended `Источники`/`Log`.
- Manufacturer page shows an adjacent table for **models WITHOUT `(DC)`**; its different technical parameters were NOT copied into the exact requested `(DC)` products.
- This exact visual page does **not** confirm missing refrigerant type, original manufacturer's warranty validity per serial/market, Wi‑Fi/package accessories or other 77 conditional fields. **Not a claim that all 8 products are READY**.

## Actual binary and regression
- Parent `MIXED_356_77cols_STAGE59_FIRST50_IGC_OEM_BASIC_WARRANTY_35_2026-10-19.xlsx`, 714425 B, SHA256 `3e33f8e4a37c6fda98647e2661df200500c89fc50c5fbfa13be642e27ade8fe8`.
- **Stage60** `MIXED_356_77cols_STAGE60_FIRST50_IGC_QV_OEM_VISUAL_QA_2026-10-19.xlsx`, **718739 B**, SHA256 **`d060f03d7aec9aa0b2d4d609c5891351cc4239197662b162189d11ed32d5b2a2`**, contains Stage59 product values plus a new exact 64-field visual QA worksheet; exported with artifact_tool.
- Compared **all 356×77 output cells** between Stage59 and Stage60 using independent XLSX XML read: **0 output changes**, including all 306 outside-scope models. Exactly eight historical source rows and eight Log rows added plus QA60 sheet; existing history retained.
- Current Stage59/60 first50 physical fill **1562 of 3850** (not equal to verified ready); core open 41 (brandwide IGC warranty provisional); other conditional/source checks 826. **0/50 READY**.
- **GitHub connector cannot transmit local binary**; Stage60 actual XLSX exists as download from ChatGPT, while this text/CSV is published and verified remotely.

## Next
Continue *exclusively* first50: visually inspect relevant original IGC model-family PDFs for wall/duct/cassette and resolve unconfirmed exact refrigerants by compatible outdoor system; resolve Daikin regional suffix differences; Kentatsu KTGV24 exact tubes; document applicable original manufacturer warranty and accessories, conditional max current, protection IP, exchanger, 50 different seller-source prices (never invent commercial values). Do not publish production-import status without all applicable fields and original source/edition.
