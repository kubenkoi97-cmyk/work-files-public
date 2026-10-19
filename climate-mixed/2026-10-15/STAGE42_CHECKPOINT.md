# Stage42 — IGC IMS-K-NH(DC) exact-suffix and refrigerant evidence (2026-10-19)

**INTERMEDIATE / NO TECHNICAL CELL CHANGES / DO NOT IMPORT UNVERIFIED FIELDS.**

## Scope and baseline

- Six exact IGC SKUs: `IMS-K22NH(DC)`, `IMS-K28NH(DC)`, `IMS-K36NH(DC)`, `IMS-K45NH(DC)`, `IMS-K56NH(DC)`, `IMS-K71NH(DC)`.
- Actual catalog positions: rows **2–7**, refrigerant column **27**, each blank in Stage39/41.
- Combined existing manufacturer-warranty gaps also remain open. Do not fill with generic IGC dealer 3-year term.
- Original 356 × 77 output structure unchanged, baseline applicable core empty count **625**, including these six already-counted blanks.
- Stage42 workbook `MIXED_356_77cols_STAGE42_BASELINE_UNCHANGED_2026-10-19.xlsx` points to the **exact same verified binary Git blob** as Stage39/Stage41: `16b8779680bdb25273e18b1f499219a29a5de297`, 483530 bytes, SHA256 `ed5918460aa74738c225fd15cc8b8426261ae0fea08bbb6053a951bc78c187d1`. The workbook is deliberately byte-identical because zero fields passed verification. No claim of a new local spreadsheet-cell audit.

## Evidence discovered

1. An **IGC-hosted factory technical-table PDF** for wall units, series J, search-indexes **all six exact `(DC)` identifiers** and model-by-model dimensions, net/gross weights, pipe sizes and cooling/heating capacities: https://igc-aircon.com/upload/iblock/8e1/f2umkqwfiqx3p6b65iz03odbvjqw01vo.pdf. However the web PDF fetch returned **502 Bad Gateway**; no original PDF page image was viewed. The indexed excerpts are not OEM_PAGE_VERIFIED. Crucially, this retrieved table segment **did not verify a refrigerant** for these exact six SKUs.
2. An independent **C-O-K mirror** indexes the same six exact-model technical tables: https://www.c-o-k.ru/library/instructions/igc/kondicionery-promyshlennye/38333/141247.pdf. The full PDF is **16.5 MB** and blocked by the web file-size limit, so again no page was visually examined. Model references are indexed, not original-page-validated.
3. The currently published IGC seller product page https://igc.com.ru/catalog/vnutrennie_bloki_vrf_sistemy/igc_ims_k22nhdc_5/ explicitly lists **R410A** but for **`IMS-K22NHDC(5)`**, not `IMS-K22NH(DC)`. Same numeric capacity is not evidence of identity; suffix, series and revision differ.
4. The IGC wall-unit catalog lists current model families as `IMS-K-NHDC(5)`; a separate 2025 EAEU declaration distinguishes `(DC4)`, `(DC5)`, `(DC6)`, `(DC7)` and `(DC8)`. These are distinct names, none of which may silently replace exact `(DC)`. The declaration is not a refrigerant specification.
5. An automation compatibility matrix lists the six **exact original `(DC)` model codes**, corroborating their identity but says nothing about the correct refrigerant.

## QA decision

- **Six exact SKU refrigerant entries stay blank.** No R410A copied from newer `DC(5)` or `DC5` code.
- Status for each: `OEM_INDEXED_PDF_VISUAL_PENDING; SKU_REVISION_MISMATCH_RISK`. Index evidence was inspected, not original PDF pages. No false `NOT_FOUND_AFTER_FULL_PASS` claim.
- Stage41 **nine separate Midea refrigerant conflicts remain OPEN**. They are distinct from this batch of six IGC unconfirmed blanks.
- Neither stage closes the 77-column conditional applicability audits or manufacturer warranty/source verification obligations.

## Batch statistics

| Metric | Value |
|---|---:|
| Exact IGC models investigated | 6 |
| Fields added to Excel | 0 |
| Previous filled values corrected | 0 |
| Baseline applicable empty fields | 625 (unchanged) |
| IGC refrigerant blanks reviewed but still open | 6 |
| Total already-known targeted Midea R32/R410A conflicts | 9 OPEN |
| Original PDFs visually opened | 0 |

## Reproducibility and queue

- `STAGE42_IGC_6_EXACT_SUFFIX_REVIEW.csv`: one evidence row per exact SKU.
- `STAGE42_SOURCE_EVENTS.csv`: URLs, exact/not-exact, original-PDF access status.
- `STAGE42_FIELD_PATCH.csv`: header-only no-change log.
- Obtain PDF originals and screenshots directly; find exact-series refrigerant from manufacturer, historical edition, pairing of outdoor systems; verify all six, including applicable conditional fields, instead of inferring from 2025 `DC5`.
- Resume the wider **66 piping, 63 refrigerant, 20 panel, 5 net-mass, 16 dimension, 114 tech-documentation and 341 manufacturer warranty core blank** queue, plus each of 77 conditional fields for all 356 models. After **actual verified technical value** edits, make a new workbook using real binary XLSX edit and full regression before publication.

**QA integrity note:** Number of reviewed source records does not equal comprehensive exact-SKU factory verification. Stage42 is evidence research, not a numeric improvement in the workbook.
