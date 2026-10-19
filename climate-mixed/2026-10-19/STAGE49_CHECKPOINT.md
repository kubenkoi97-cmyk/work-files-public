# Stage 49 — exact-model source-quality review (2026-10-19)

**Evidence only. No new XLSX and no technical cell modification.** The latest valid tested full workbook remains Stage47, `MIXED_356_77cols_STAGE47_KTLV15_EXACT_PIPES_2026-10-19.xlsx` (640092 bytes, SHA-256 `91ce58730c4f8d27091d450aa3f58d213a9940fd4ba335e631ffc24b33e9ac48`), available as a ChatGPT sandbox file. The binary was **not uploaded to GitHub**; do not provide a fabricated remote link.

## Midea exact model and net-vs-bundle weight

- **Midea MI2-22Q1DHN18(At)** (Excel row 275; column 37 net weight is still blank): exact individual indoor-unit dealer product page https://brand-climat.ru/midea-mi2-22q1dhn18-at lists **10 kg net** (and **12.5 kg gross**), keyed to the target suffix.
- **Midea MI2-22Q1DHN18(At)/T-MBQ1-01G**, a **combined indoor-unit and panel retail set**, https://kupikonder.com/catalog/detail/kassetnaya-vrf-sistema-midea-mi2-22q1dhn18-at-t-mbq1-01g/ lists **12 kg weight** without equivalent single-unit net-mass semantics. This is not evidence that the body weighs 12 kg; do not transfer bundle/package numbers into the individual unit net-mass column.
- Candidate 10 kg has evidence status `RETAIL_EXACT_MODEL_NET_WEIGHT_OEM_PENDING`. Because the staged workbook export service failed during Stage48 and original Russian factory PDF page could not be inspected, **no value was written to Excel**. The candidate is recorded for exact-series factory visual page confirmation and later safe insertion.

## Kentatsu decorative panel cross-series conflict

- An exact dealer card of Kentatsu `KTZV15HZBN1` identifies an accessory **KPU65-D3**; other older/indexed technical documents mention **620×65×620 mm** dimensions, while a **different KTVB family** retail page associates a similarly named panel with **950×53×950 mm**. These claims cannot be freely merged across block families, panel revisions or markets. Do not add panel dimensions without **exact target unit → compatible panel article → manufacturer-dimensional drawing** chain. Historical indexed OEM PDF was not visually inspected because PDF download exceeded access limits.

## Electrical current / protection distinction

- A Kentatsu `KTYV30HZBN1/KPU1M-D3` offer at https://mircli.ru/Kentatsu-KTYV30HZBN1-KPU1M-D3/ lists **0.52 A operating current** (cooling/heating) and **15 A circuit breaker**. Neither alone proves a `Максимальный ток, А` of either 0.52 or 15, so column 73 is not filled from these differently-labelled fields.

## Stable counts and technical limitations

- Stage47 real edit: one formerly blank pipe pair in row79, field23; 614→**613** open applicable core blanks.
- Stage48 source-only: KTZV24HZBN1 max-current **0.46 A** was search-indexed on an exact SKU product listing, but extended keyed current line not opened; `RETAIL_INDEXED_OEM_PENDING`, **not entered**. Artifact export RPC failed; **no valid Stage48 workbook was generated**.
- Stage49: additional **0** Excel cells edited; baseline remains **356 SKUs ×77 output columns** and **613** core blanks (manufacturer warranty341, technical documentation106, pipe pairs64, refrigerant63, cassette panels20, net weights3, dimensional fields16, power0). All 77 conditionally applicable properties and previously filled potential conflicts require further review.
- Existing high-risk conflicts remain **open**: nine Midea R32/R410A contradictions; Daikin FXKQ regional net weights; Kentatsu KTLV15 heating **1.8 FILE vs 1.5 seller**. These were not resolved by current evidence. No final import readiness or manufacturer-page verification is claimed.

## Next full technical checkpoint prerequisites

1. Restore/export a fully validated XLSX from the Stage47 book (never silently use old Stage39/42). Reimport and confirm 356×77 and exact before/after cell diff.
2. View original manufacturer manual tables for exact model/market; resolve pending KTZV24 max current, Midea MI2-22Q1 body mass, Kentatsu panel chain.
3. Resume per-model FILE→WEB recheck of all 613 core blanks and all 77 optional field applicability; record one source/URL/page/edition and conflict reason per value. Preserve earlier historical versions and source revisions.

[Stage47 confirmed source change](STAGE47_CHECKPOINT.md) · [Stage48 no-edit checkpoint](STAGE48_CHECKPOINT.md) · [Stage49 exact-model review CSV](STAGE49_SOURCE_QUALITY_CASES.csv)
