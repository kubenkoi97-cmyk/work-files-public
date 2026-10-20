# Stage66 / MIXED first50 / 2026-10-20 — 6 exact-SKU retailer-declared coverage areas

**Intermediate, not import-ready. STRICT SCOPE: first50 output rows 2–51 only.** Parent: Stage63 actual full XLSX, 729740 bytes SHA256 `a2c95f15b9fde459c9a9f3143bb71752bcce003f97ac37b297a0205bd912a0d9`. Stage64 and65 were source-only checkpoints with no changed products.

## Actual product edits
Daikin six exact original SKUs, formerly physically empty `Площадь, м²` column14:
- FXKQ32A row39 = **36 m²**, directly opened exact product page https://mircli.ru/Daikin-FXKQ32A/
- FXKQ40A row40 = **45 m²**, directly opened exact product page https://mircli.ru/Daikin-FXKQ40A/
- FXKQ50A row41 = **56 m²**, indexed exact SKU product card visible within https://mircli.ru/Daikin-FXCQ50A/ ; primary exact page itself was unavailable, downgraded proof
- FXKQ63A row42 = **71 m²**, indexed exact SKU product card visible within https://mircli.ru/Daikin-FXCQ63A/ ; primary exact page itself was unavailable, downgraded proof
- FXMQ200A row43 = **224 m²**, directly opened exact SKU https://daikinair.ru/catalog/vnutrennie_bloki_vrf_sistemy/daikin_fxmq200a/
- FXMQ250A row44 = **280 m²**, directly opened exact SKU https://daikinair.ru/catalog/vnutrennie_bloki_vrf_sistemy/daikin_fxmq250a/

**Important semantics:** These are *retailer-advertised recommended coverage areas*, not manufacturer-certified climate-load, operational limits, or general guarantees that a given premises can be served. The area is always an application-dependent marketing estimate, even when exact SKU source gives a precise number. Four exact SKU pages opened, two exact SKU related-cards only indexed; two have weaker QA. Supplier-specific field provenance and caveat appended to sources/Log. No values derived by rounding cooling kW; no similar-model SKU transfer.

## Current binary and regression
`MIXED_356_77cols_STAGE66_FIRST50_DAIKIN_EXACT_RETAIL_AREA_6_2026-10-20.xlsx` **732069 bytes**, SHA256 `81a41139edd433624b75901732f00c5da688976a3d4ebb6a448903caf39959b2`. Actual artifact_tool XLSX export followed by reimport verification; 31 sheets; appended `QA66 Daikin 6 площадей`, six new source and six new Log records.
Independent direct OOXML product data diff over **356×77** values: **exactly six empty→value** cells N39:N44; **0 previously nonempty overwrites, 0 changes among remaining 306 products**, 77 original columns and exact model order unchanged. Parent original source worksheet untouched.

First50 physically filled **1562 → 1568** / 3850; existing historical 41 open CORE remains unchanged (the area column is a separate conditional/commercial user-facing field); **0/50 models certified import-ready**. Never use retailer estimates as OEM technical capacity or cross-assign different SKU suffixes.

GitHub stores real patch and this checkpoint. **The binary XLSX exists in ChatGPT sandbox; it has NOT been uploaded to GitHub** with current connector; do not claim a remote binary link.

[Exact six-field patch](STAGE66_DAIKIN_RETAIL_AREA_6_PATCH.csv). Next first50: validate critical refrigerants and Daikin revision conflicts and each remaining conditional applicable characteristic.
