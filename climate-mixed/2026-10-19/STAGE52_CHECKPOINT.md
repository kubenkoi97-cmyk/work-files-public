# STAGE 52 — 14 exact-model Midea heat-exchanger source extractions (2026-10-19)

**INTERMEDIATE / NOT IMPORT-READY.** Exact original FILE→column extraction; OEM original PDF **NOT visually opened**. No R32/R410A or other high-risk model conflicts have been closed.

## Workbook and regression

- Full valid XLSX: `MIXED_356_77cols_STAGE52_MIDEA_EXACT_HEAT_EXCHANGERS_2026-10-19.xlsx`, **399419 bytes**, SHA-256 `96622c89146f551fccb4a2215b7ba3914254a824abe17e0d6ba727ebb6f007bd`.
- Parent is Stage51 unchanged 356×77, 12 sheets, 613 applicable CORE blanks. Stage52 appends exact-source rows to `Источники` and `Log`, new `QA52 Мidea теплообменники` sheet. **13 sheets**.
- Reopened exported XLSX and independently compared **all 356×77 cells** against the parent: **exactly 14 previously blank column 62 cells** changed; no prior nonempty output values altered; exact product order, model codes and 77 field headers preserved.
- Column 62 `Теплообменник` populated **18 → 32**; original core gap count **613 unchanged** (this conditional column was missing from historical base denominator).

## Exact SKU groups and quality
- `MIH36/45/56/71/80/90GHN18(DP)`: six exact rows 324–329, extracted from each own `Сбор данных!F` row. Engineering detail includes “2 и 3” rows, six or eight coil circuits by SKU, inner-grooved Ø5mm tubes, hydrophilic Al fins at 1.33mm pitch. Original source links lead to Daichi MIH-GHN18(DP) installation manual and other indexed manufacturer catalog material.
- `MIH15/22/28/36/45/56/71/80BHN18`: eight exact rows 330–337, exact row-specific values. MIH15/22: **one** row, two circuits, grooved Ø7mm and 1.3mm fin spacing. Larger codes: source literal “2 и 3” rows, six or eight circuits, Ø5mm grooved pipes and 1.33mm fin pitch.
- “2 и 3 ряда” is kept as the **source's literal wording**, not arbitrarily normalized into a single number.
- **Evidence status:** `FILE_EXACT_MODEL_ENGINEERING_TABLE__OEM_PDF_VISUAL_PENDING`: user-original source text is exact and model-specific, but current session failed to open two Daichi PDF originals; do not promote to `OEM_PAGE_VERIFIED`.

## Risk handling
- Never transfer Midea V8 specs to ATOM B suffix `(At)` items; never infer exact refrigerant from generalized `R410A/R32`; never transfer mass/dimensions/panel claims to unrelated SKU.
- Historic Midea T3/DL refrigerant conflicts, KZA edition disputes and Daikin weight conflicts continue OPEN.
- The new true XLSX binary currently exists as local ChatGPT artifact; **this GitHub entry is the source patch and checkpoint, not publication of the XLSX binary**. Binary upload via available GitHub connector remains unsupported in this environment.

[Patch 14 fields](STAGE52_MIDEA_EXACT_HEATEXCHANGER_PATCH.csv) · prior [Stage51 conflicting OEM revisions](STAGE51_CHECKPOINT.md).
