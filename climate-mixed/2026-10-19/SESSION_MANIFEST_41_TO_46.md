# MIXED continuation manifest — Stages 41–46, as of 2026-10-19

**Status: INTERMEDIATE, NOT IMPORT-READY.** Latest actually edited and verified complete workbook is `MIXED_356_77cols_STAGE46_KTZV60_EXACT_CURRENT_QA_2026-10-19.xlsx`, 622738 B SHA256 `b72b39a87933256e0eaaeda73ae93cebf4f1219770c063a716d8dfd9c9b85d1c`, exists as current-chat sandbox file. **The connected GitHub tool has not published the binary XLSX**, only confirmed CSV/Markdown files. Do not claim remote XLSX exists.

## Version chain and counts

- **Stage43 (2026-10-17)** actual newer technical base in user's Library: 356×77, 32 sheets, 555300 B, SHA256 `eef2987a6e4bb6bd0fc8779029ef647a571bf82bad5081af06626da378d4409b`, 615 CORE open, 10 previously empty cells more than Stage39. In other Oct19 context Stage41/42 were evidence-only and accidentally copied obsolete Stage39 blob; their Midea/IGC checks remain valid as provenance but do not use their workbook as baseline.
- **Stage44** 2026-10-19: Kentatsu KTZV15HZBN1 row60 2 exact dealer fields, pipes col23 `6,35/12,7`, max current col73 `0.46`. Core 615→614.
- **Stage45** 2026-10-19: extracted 35 **exact SKU white body color** entries from corresponding `Сбор данных!F` of 27 Kentatsu and 8 Midea, filled column22; output color21→56, original HTML and commercial fields unchanged; core unchanged614. New exact KTLV15 heating conflicting 1.8 in FILE vs1.5 retailer.
- **Stage46** 2026-10-19: KTZV60HZBN1 row65 col73 max current **0.65 A**, directly opened exact source https://envok.ru/catalog/konditsionery_split_sistemy/vrf-sistemy/vnutrennie-bloki-vrf/vnutrenniy-blok-vrf-sistemy-kentatsu-ktzv60hzbn1-daichi-28775/, full FILE capacity comparison. Vendor text mistakenly says 1.5kW whereas actual exact-model specification says 5.6kW; distinguish boilerplate from keyed technical data. Factory OEM pending.
- All stage44–46: **38 old blank→filled**, 0 old nonblank changed, original selected product order 356, headers77, current44 sheets, latest output reimport QA confirmed. 614 CORE remain (warranty341, docs106, pipes65, refrigerant63, panels20, masses3, dimensions16); plus conditional fields and 12 specific prior conflicts need full second-pass OEM verification.

## Links and continuation

- [Stage46 checkpoint](STAGE46_CHECKPOINT.md) · [patch](STAGE46_KTZV60_PATCH.csv) · [356 model audit](STAGE46_MODEL_AUDIT_356.csv) · [77 column coverage](STAGE46_77_COVERAGE.csv) · [dealer internal mismatch](STAGE46_VENDOR_TEXT_MISMATCH.csv).
- [Stage45 evidence](STAGE45_CHECKPOINT.md) · [Stage44 evidence](STAGE44_CHECKPOINT.md) · [Stage43 actual history](../2026-10-17/SESSION_MANIFEST_41_TO_43.md).
- [Stage40 master + exact source protocol](../2026-10-15/HANDOFF_MASTER_PROMPT_STAGE40_RU.md).
- Next: original Russian OEM PDF page for KTZV60 and pending Midea R32/R410A; repeat exact-SKU FILE→WEB audit + full 77-column applicability, record each field; preserve and publish validated XLSX whenever ability to upload binary exists.
