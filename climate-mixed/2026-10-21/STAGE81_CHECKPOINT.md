# MIXED Stage81 — first50 exact Kentatsu max currents (2026-10-21)

**Real XLSX edit; exact original models only; intermediate NOT import-ready.** Parent Stage79 full binary `MIXED_356_77cols_STAGE79_FIRST50_DAICHI_CONDITIONAL_WARRANTY_EVIDENCE_QA_2026-10-21.xlsx` 772215 bytes SHA256 `2e5ddc254c967d5c7faa9489d73ae8bfc4f9c78ccfe4b7636a1d7c5ecdec36c8`.
Actual Stage81 binary `MIXED_356_77cols_STAGE81_FIRST50_KTGV_EXACT_CURRENTS_2026-10-21.xlsx` 774182 B, SHA256 `8e8c63085d4f57812647a11ebcb4389a213bfbc1b4fa58d846b31cdd77cbc4a4`. Available as ChatGPT sandbox download, **NOT transferred as binary XLSX to GitHub**.

Exact old→new product patch:
- Excel row 45 **KTGV18HZBN1**, col73 `Максимальный ток, А`: BLANK → **0.28 A**. Two exact-SKU independent retailer **search-indexed** spec sources: `https://tdkomfort.ru/shop/product/vnutrenniy_blok_vrf_sistemy_kentatsu_ktgv18hzbn1/` and `https://coldcontrol.ru/catalog/detail/nastennnyy-blok-vrf-kentatsu-ktgv18hzbn1/`. Full specification current row not accessible in live expanded page. `RETAIL_EXACT_TWO_INDEXED_SOURCES`, factory original PDF pending.
- Excel row 51 **KTGV72HZBN1**, col73 BLANK → **0.69 A**. Independently **directly opened exact SKU full technical tables** `https://multisystems.ru/catalog/vrf-nastennye/kentatsu-ktgv72hzbn1` and `https://envok.ru/catalog/konditsionery_split_sistemy/vrf-sistemy/vnutrennie-bloki-vrf/vnutrenniy-blok-vrf-sistemy-kentatsu-ktgv72hzbn1-daichi-28740/`. `RETAIL_EXACT_TWO_DIRECT_FULL_TABLES`, factory original PDF pending.
These are maximum *operating current*, NOT circuit protection amperage, maximum refrigerant charging load or outdoor unit current. No current guessed for KTGV24 or KTGV60.

Imported and updated complete workbook with `artifact_tool`, exported and reopened, appended exact-source records to `Источники`, `Log` and new QA81 worksheet, total 48 sheets. **Independent OOXML 356×77 cell-level diff from parent: exactly TWO previously empty fields BU45 and BU51 filled; ZERO existing nonempty overwritten, original model IDs and all 77 columns preserved, ZERO changes to 306 out-of-scope SKUs rows52–357.**
Historical 40 CORE applicable gaps from Stage80 remain unchanged because col73 maximum current is an additional conditional field. No model is certified fully READY. [Exact two-field reproducible patch](STAGE81_FIRST50_KTGV_2_EXACT_CURRENTS.csv).
