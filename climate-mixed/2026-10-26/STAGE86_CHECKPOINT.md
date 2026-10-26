# MIXED Stage86: exact Daikin FXKQ50A market-recommended area (2026-10-26)

**Validated complete full XLSX**: `MIXED_356_77cols_STAGE86_FIRST50_DAIKIN_FXKQ50_EXACT_AREA_2026-10-26.xlsx`, **792356 bytes**, SHA256 `0b3edd0aad15d2d3170e4e7186597a91209f4ae81d45365b0de383b0e5867c3a`; 55 sheets, all Stage85 original 54 preserved, new `QA86 FXKQ50 площадь`.

### Actual newly filled value
Excel row41 `FXKQ50A` col14 recommended sales area blank→**56 m²**. Two exact SKU product pages [Climamarket](https://climamarket.ru/kassetnaya-vrf-sistema-daikin-fxkq50a) and [Lenklimat](https://lenklimat.ru/catalog/konditsionery/promyshlennye-konditsionery/multizonalnye-sistemy-vrf/vnutrennie-bloki315/kassetnaya-vrf-sistema-daikin-fxkq50a/) explicitly state 56; this is marketing service area, **not** OEM engineering load or heat balance. Earlier Stage67 FXCQ-related unjustified area was removed; this restoration uses only newly verified **FXKQ50A** exact pages. Not copying their R32/1y warranty or potentially mismatching body sizes.

### Regression
- Independent OOXML re-import and FULL 356x77 value comparison vs Stage85: **exactly one** target product cell change (row41 col14), zero changes in all 306 non-target rows52-357, all headers and source/history sheets preserved.
- First50 populated Stage83 1621 → Stage84 1623 → Stage85 1625 → Stage86 **1626**. Exactly **five actual fills**, no numerical rewrites to existing product values. 40 historical CORE fields remain unfilled; 0 confirmed READY_FOR_IMPORT, 0 confirmed TECH_READY_COMMERCIAL_BLOCKED.
- **Important:** Daikin FXKQ50A retailer R32 contradicts Daikin EU FXKQ-A technical table R410A (full European AMVEB). Production-region SKU identity not proven; don't edit gas, remaining critical issue.

**GitHub delivery:** QA/patch/checkpoint UTF-8 source only; full 792356-byte XLSX not published as binary, available as ChatGPT download; do not conflate markdown with actual XLSX.
