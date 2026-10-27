# Stage104 NEXT50 — completion of marketing area column

## Verified outcome
- Exactly 23 new source-traced area cells N79:N101, no numeric value overwritten. Full column for selected 50 now 50/50 occupied.
- First 8 areas inherited prior baseline and need later exact-model check. Retail area ≠ sizing engineering.
- Physical cell coverage 1584/3850; zero technically ready and import ready SKUs.
- Complete workbook: `MIXED_356_77cols_STAGE104_NEXT50_ALL50_AREA_SOURCES_AUDIT_2026-10-27.xlsx`, size 834581 B, SHA256 6c1c02b52e8252bfc38ca2306db9d81e9f5921b76c3d515fe187bd47141cf687, 74 worksheets.
- Stage103 preserved, one new QA worksheet; 306 protected goods unchanged, 0 unexpected changes across 27,412 product data cells.

## Retail provenance
- KTLV / KTKV: https://brand-climat.ru/konditsionery/vrf-sistemy/vrf-kanalnye-bloki/?limit=75
- KTHV: https://brand-climat.ru/konditsionery/?limit=75&page=110 ; https://brand-climat.ru/konditsionery/?limit=25&page=330 ; https://brand-climat.ru/konditsionery/?limit=48&page=232
- KTGB18: https://coolsochi.ru/product/kentatsu-ktgb18hzbn1/ ; https://ryazan.vsekondicioneri.ru/product/kentatsu-ktgb18hzbn1/
- KTLV15 second confirmation https://pro-komfort.com/product/vnutrenniy-kanalnyy-blok-multizonalnoy-vrf-sistemy-kentatsu-ktlv15hzbn1/
- KTHV72 second confirmation https://pro-komfort.com/product/vnutrenniy-napolno-potolochnyy-blok-multizonalnoy-vrf-sistemy-kentatsu-kthv72hzbn1/

## Open technical checks
- KTLV15 target max static pressure 50 Pa corresponds to original F79 10 (10–50) Pa, not an error caused by dealer nominal 10.
- KTKV80 target max 160 Pa corresponds to original F87 40 (10–160) Pa.
- KTHV72 marketplace heading mentions 80m² yet detailed area and second seller indicate 71m²; retained 71.
- KTLV15 some dealer description lists 1.5kW heat, whereas original own F79 and exact dealer list indicate 1.8kW; do not blindly overwrite.
- Missing accessible exact HZBN1 series OEM PDFs; indexed links 404; *no* older HQAN1 substitution.
- No unfounded commercial price, stock, image or warranty assertions.

Full 50×77 audit and authoritative 74-worksheet binary Excel available in ChatGPT Stage104 handoff ZIP; file hashes are given in the manifest.
