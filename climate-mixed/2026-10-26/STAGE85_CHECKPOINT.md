# MIXED Stage85 — exact IGC QV model-recommended areas (2026-10-26)

**Parent full workbook:** Stage84 sha256 `68db42147ce5ccf5e529eef89bfb4d1625a4147b05fd07def88d73724235a07d`.

**New verified complete XLSX:** `MIXED_356_77cols_STAGE85_FIRST50_IGC_QV125_QV140_EXACT_AREAS_2026-10-26.xlsx` 791174 bytes, sha256 `4bbb2964fffdcf55aaea7c1b3fe6fb08926867d6228e03548d6fd1043706203a`. **Full 54-sheet book provided in ChatGPT, not hosted on GitHub**.

## Real changes
- Row33 `IMS-QV125NH(DC)`, col14 marketing recommended area blank→125 m², specifically exact SKU on official Russian IGC dealer https://igc.com.ru/catalog/vnutrennie_bloki_vrf_sistemy/igc_ims_qv125nh_dc/ .
- Row34 `IMS-QV140NH(DC)`, col14 marketing recommended area blank→140 m², specifically exact SKU on official Russian IGC dealer https://igc.com.ru/catalog/vnutrennie_bloki_vrf_sistemy/igc_ims_qv140nh_dc/ .
- These areas are seller-recommended, **not a verified heat load or engineering design**. No refrigerant or warranty data copied from these cards: historical SKU generation and old purchase/supplier contract still unresolved.

## Strict 356 × 77 regression
- Independently parsed OOXML of exported Stage84 and Stage85: exactly **two** product-cell changes, both listed above. Original 53 sheets preserved, audit sheet `QA85 QV площади 2` added. Zero changes to 306 rows52–357.
- First50 physical fill count Stage83 1621 → Stage84 1623 → Stage85 **1625**, nonzero actual fills = 4 total. Historic CORE remains **40** open (21+15+4). 0 verified READY_FOR_IMPORT, 0 technically certified release-ready (remaining edition and validation gates).
- IGC dealer lists 3-year warranty on affected QV product pages while legacy 12-month fields exist; don't overwrite until contractual/production scope is clarified.

## Delivery note
Github-connected API tool can write UTF-8 source/QA documents but cannot directly read the local exported XLSX binary; publishing Stage85 text QA is not proof the XLSX is present in this repo.
