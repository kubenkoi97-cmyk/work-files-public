# Stage51 — Kentatsu KZA 2025 vs later edition, dangerous value conflicts (2026-10-19)

**Evidence and import-quality checkpoint; NO technical numeric values changed.** The exact original manufacturer page for KZA was visually examined. **9 model-field conflicts** now marked red in the XLSX; two net mass blanks yellow. Both conflicting source versions retained without silent overwrite.

## Technical binary
- Latest verified binary: `MIXED_356_77cols_STAGE51_KZA_REVISION_CONFLICT_QA_2026-10-19.xlsx`, **395821 bytes**, SHA-256 `6ace1ba0771a6aebbb8819e1b981b5ae33e6b56c6d483c1833c75e707fd02ee0`; current-chat download only, NOT uploaded as binary GitHub.
- Parent Stage50 compact: 393670 bytes SHA-256 `3ff08786d7999c677a4cfff8b311cecb33151759a29c7afaae24d2a4ff55bf68` with 16 old-empty source-to-column fills. Historical full 47-sheet Stage47 remains untouched archive.
- Reimported Stage51 in a new runtime process: **12 sheets, 356×77 output unchanged, exactly 9 conflict rows, 613 still empty core applicable cells**. No previously nonblank number changed or removed.
- Added `QA51 версии KZA`, source and Log provenance appended; shaded disputed populated Excel fields red and two disputed net-mass blanks yellow. Stage51 is a safety/accuracy escalation, not a new numeric fill.

## Original factory documentation and competing values

**Version A, KENTATSU Russian DX PRO A catalog 2025, page 43, actually OPENED & visually screenshotted:** https://onokom.ru/dok/kentatsu/2025/catalog/2025-catalog-dx-pro-a-kza-vrf.pdf
Exact model rows KZA18/24/30/40/50/60 in one table. For **KZA30**: heat3.0 kW, air flow700/640/570, maximum acoustic 42dB(A), pipe 6.35/12.7 mm, unit mass15.5kg; **KZA40** heat4.3, air740/660/590, noise43/39/37, pipe6.35/12.7, body mass15.5kg. The XLSX has these 2025 values except mass left blank. This is `OEM_PAGE_VERIFIED_2025`, not automatically a match to later stock.

**Version B, different later/alternative indexed KENTATSU catalog page 86 (publication date not independently verified):** https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf; alternative https://daichi.business/support/documents/download.php?ID=27751. Search-indexed exact table:
KZA30 heat **3.2**, air **570/530/480/450**, noise **34/33/32**, gas pipe **9.52**, weight **13.5**; KZA40 heat **4.0**, air **650/620/560/540**, noise **38/36/35**, gas12.7, weight **14.5**. The 22 MB C-O-K PDF could not be visually opened due to size limit; Daichi download timed out. Status **OEM_INDEXED_PDF_VISUAL_PENDING**, not visually verified or a proven replacement for model/region of user's stock.

**Retail pages with apparently newer values**: https://kentatsuair.ru/catalog/vnutrennie_bloki_vrf_sistemy/kentatsu_kza30hzan1/ and https://klimato.ru/shop/vrf_sistemy/vrf-sistemy/vrf-kassetnye-vnutrennie-bloki/kentatsu-kza30hzan1/ list heating3.2 and gas9.52 on exact KZA30; this corroborates newer indexed edition but does NOT identify user's actual shipping/revision.

## Critical decision
Exact same printed SKU appears with materially different gas line diameter **12.7 vs9.52 mm**, heat and mass. **DO NOT IMPORT KZA30 / KZA40 product cards until identified physical manufacturing edition or official Russian OEM model/serial clarification**. Leave two mass cells blank; do not automatically change heating, pipes or acoustic and airflow values. Current Excel 2025 fields are kept **only because the 2025 original was verified**, not a claim they must be correct for a user's future delivery. Both variants recorded with priorities (visual original stronger source verification but later edition may take precedence for current product) and unresolved reason.

## Anti-skip counters and next
- CORE blank register **613** unchanged: manufacturer warranty341, docs106, pipe pairs64, refrigerants63, panel sizes20, unit net masses3, body dimensions16.
- All **356** rows / **77** headers preserved and general conditional applicability OPEN; two exact models and nine high-risk field conflicts reviewed in this stage.
- [Nine exact field conflicts CSV](STAGE51_KZA_2025_VS_LATER_REVISION.csv).
- Next: obtain the large later PDF as a legally accessible original page 86, confirm edition/date and serial rules, resolve KZA lines then retest all 77 applicable fields and seller/OEM prior values; separately continue 64 pipe blanks and 63 refrigerant blanks.

**Do not misrepresent a newer indexed catalog as a visually audited original.**
