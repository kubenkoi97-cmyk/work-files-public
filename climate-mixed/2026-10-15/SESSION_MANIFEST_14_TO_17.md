# MIXED 356-product HVAC catalog — Long session stages 14–17

**Date:** 2026-10-15. **MOST RECENT:** STAGE 17. **UNFINISHED: NOT READY FOR WEBSITE IMPORT.**

## Source of truth / scope
- Input workbook original tab `MIXED — обработка` 744 products. Only **356** with simultaneously populated original description + characteristics; remaining **388 untouched**.
- Final output tab `Наполнение MIXED`: **356 products × 77 columns**, no changed product order or lost previous approved values.
- User mode MIXED: FILE→WEB for missing technical fields; exact-SKU checks including `(At)`, `(DP)`, `(A)` suffixes, region and revision. Never substitute near model or gas pressure group, do not guess values or add inapplicable items.

## Checkpoints executed this session
| Checkpoint | Model families | Newly filled blank cells | GitHub logs |
|---|---|---:|---|
| [Stage14](STAGE14_CHECKPOINT.md) | Kentatsu KTYV/KTZV/KTVV and Midea MI2-Q4D decorative panels | **17** | [17 panel fields](STAGE14_17_PANELS.csv) |
| [Stage15](STAGE15_CHECKPOINT.md) | Five exact Kentatsu KTYV/KTZV/KTVV refrigerant pipe values | **5** | [5 piping fields](STAGE15_5_PIPE_FIELDS.csv) |
| [Stage16](STAGE16_CHECKPOINT.md) | Midea MIH-G(DP) and MIH-Q1(A), 10 exact model refrigerant and series checks | **20** | [20 fields](STAGE16_20_MIDEA_FIELDS.csv) |
| [Stage17](STAGE17_CHECKPOINT.md) | Midea MIH-B / MIH-G(DP) / MIH-Q2 model-specific tech tables | **23** | [23 fields](STAGE17_23_FIELDS.csv) |

**65 formerly blank applicable core fields filled in total**; there are **12 indexed factory-Q2 entries requiring original PDF page visual QA** and 53 other model/source checks. No nonblank numbers overwritten.

## All-model QA after every batch
Core applicable missing field count: **925 → 908 → 903 → 883 → 860**. Audited source files after each stage; stage17 workbook reimport with `artifact_tool` and checks passed:
- Output exactly **357 rows including one header**, exactly **77 columns**, **356 product lines**.
- Verified stage17 23 field values against the CSV patch and verified every item in 860 blank audit still corresponds to a genuinely empty cell.
- Older model modifications were not touched in these stages.
- **Full 77-field web-pass across all 356 models is not done.** Missing core count is not global import completeness %.

## Current open CORE exceptions 860
| Applicable field | Missing |
|---|---:|
| Manufacturer warranty (not vendor claim) | 341 |
| Technical documentation (actual link/HTML per exact SKU) | 241 |
| Refrigerant | 119 |
| Pipe sizes | 88 |
| Series | 20 |
| Cassette panel dimensions | 20 |
| Indoor net weight | 14 |
| Width + height + depth + aggregate dimensions | 4 of each = 16 |
| Nominal electrical input | 1 |

**Important omissions deliberately kept open:**
- Midea V8 factory model-engineering tables show **R410A/R32**, which is NOT a proven single refrigerant for an unspecified model/market. Do not force R410A for Midea MIH-Q2, MIH-Q4, etc. Confirm actual Russian edition.
- Exact suffix `MIH90GHN18(DP)`, `MIH18Q1HN18(A)`, and `MIH71Q1HN18(A)` lacked reliable exact-suffix source for some fields and were not silently filled.
- `MIH22/28/36/45/56/71Q2HN18` 12 entries of pipe sizes and indoor BODY weight are model-specific values present in a catalog table indexed by the search engine at `https://air-midea.com/upload/iblock/43b/0lq6fla7pf4pijetalxk0gyjb10xk3v2.pdf`; actual PDF image fetch timed out and **visual page QA pending**; this is recorded as `OEM_MODEL_INDEXED_PDF_VISUAL_QA_OPEN`. Do not consider factory visual audit done.
- A KTVV KPU95-D3 decorative panel may appear as **50 or 53 mm** deep in different editions; exact edition QA remains open.
- Prior-stage unresolved: Daikin FXMQ200/250 catalog versions, Kentatsu KTGB18 liquid/gas pipe conflict, IGC IMS-BS45 body/packaging dimensions, and Midea Q4C market code collisions.
- OEM warranty is not the same as site retailer warranty. Do not fill 341 generic seller warranty values without evidence of manufacturer policy.

## Website priority / source guidance
User-selected general sites `mircli.ru`, `iclim.ru`; Midea `midearussia.ru`, `air-midea.com`, `midea-air.ru`; Kentatsu `kentatsu.group`, `kentatsu-kondicioner.ru`, `kentatsurussia.ru`; also check all other brand-specific domains set earlier. Expand exact product specs, hidden accordion sections, and download original technical manuals. Search additional trustworthy sites if missing. The scope of a full domain-by-model deep pass **has not been met** yet.

## Latest working artifacts
- Chat Excel: `MIXED_356_77cols_STAGE17_MIDEA_FACTORY_WEB_2026-10-15.xlsx`, ~810 KB; includes all prior stages, exact 356 products × 77 output columns, and 3 new worksheets each stage (changes, core open list, summary).
- Chat CSV `STAGE17_OPEN_860.csv` is the complete row+field list of 860 unresolved core fields; `STAGE17_23_FIELDS.csv` details the latest 23 patches.
- GitHub commits contain Markdown checkpoints + source-specific patches; **the 810KB binary XLSX has not been published to GitHub**. ChatGPT attachment is current complete working copy. The GitHub ledger is complementary, not an exact byte-for-byte XLSX backup.

## Resume method
1. Start from stage17 chat XLSX and re-audit full 356×77 output; check 860 core open list and the 12 PDF visual QA flags.
2. Verify all exact suffix/market/series/version conflicts; inspect manufacturer original page images where web PDF retrieval becomes available; either confirm or rollback tentative entries and adjust audit.
3. In batches per family prioritize 88 piping, 119 refrigerant, 20 panels, 14 mass, 241 documentation, 341 warranty (OEM only). Check all 77 applicable fields, including hidden optional/conditional fields not included in core count.
4. Keep model-by-model field patch with source URL, QA status, unresolved conflict; run full 356-model regression after each batch; create new XLSX and immediately checkpoint Markdown+CSV to public GitHub.
5. Mark task final only after full FILE extraction, mandatory WEB recheck, second pass, 77-column QA, detailed field-by-field exceptions, and exact-source/audit proof across 356 SKUs.
