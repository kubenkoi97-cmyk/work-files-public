# STAGE 41 — Midea ATOM refrigerant safety audit (2026-10-19)

**Status: PARTIAL / CONFLICTS OPEN / NOT SAFE TO IMPORT.** This is an evidence-only checkpoint analogous to Stage40, NOT a new technical-value edit. Never imply full 356-row 77-field web QA from this report.

## Immutable baseline and binary snapshot

- Canonical unchanged technical data: `MIXED_356_77cols_STAGE39_MIDEA_DEEP_QA_2026-10-15.xlsx` (Git blob `16b8779680bdb25273e18b1f499219a29a5de297`, 483530 B, SHA256 `ed5918460aa74738c225fd15cc8b8426261ae0fea08bbb6053a951bc78c187d1`).
- Stage41 checkpoint workbook: `MIXED_356_77cols_STAGE41_BASELINE_UNCHANGED_2026-10-19.xlsx`. **Bit-for-bit same blob as Stage39**, intentionally copied by referencing the existing Git blob. This is NOT an edited XLSX. Changes and new source judgments reside in companion CSV and Markdown. XLSX cell-level regression was NOT performed locally because binary file access was unavailable; unchanged Git blob is the stronger proof of zero XLSX changes.
- Stage39 audits independently re-read from GitHub: 356 model audit rows, 77 coverage rows, 625 open base applicable cells; sum of per-model open count = 625. The same open count applies because the workbook is unchanged.

## Stage41 research and decisions

- **9 exact Midea SKU conflict cases** from Stage32 and Stage38 reconciled against the Stage39 model audit row identities. The conflict statuses remain open (5 T3, 1 T2, 3 DL); Stage41 closes **0**.
- **7 exact model pages presently directly expose R32** on MirCli: MI2-36/45/56/71T3DHN18(At), MI2-80T2DHN18(At), MI2-45DLDHN18(At), MI2-90DLDHN18(At). This proves what the seller currently publishes, NOT a unique factory refrigerant for a particular system.
- MI2-28T3DHN18(At) MirCli link could not be fetched on this pass. MI2-140DLDHN18(At) exact MirCli page was fetched but currently omits a refrigerant field. **Do not count these two as fresh R32 confirmations.** Historical Stage32/Stage38 assertions remain preserved.
- Exact SKU MI2-90DLDHN18(At) at IFREEZ publishes **R410A/R32**; additionally lists **liquid 15.9 mm / gas 9.52 mm**, an apparent label inversion requiring OEM pipe-table check before transferring. Seller 3-year warranty is not a verified manufacturer policy.
- Formerly indexed factory portal `air-midea.com/support/marketing/download/12031/` now redirects to a temporary site-unavailable notice and sends visitors to Daichi product cards for documentation. Search snippets alone are not viewed OEM PDF evidence. Daichi indexed catalog has **older MI2-DLDHN1 model codes**, which are not the same as `MI2-DLDHN18(At)`.
- Manufacturer-hosted Midea Atom 2024-V7 PDF and 2025-V15 VRF PDF were found, but could not be opened due to size limits; the markets/editions may differ. **No OEM page screenshots were verified** and no region-safe single-refrigerant decision is possible.
- Historic Envok alternative R410A cards were retained from Stage38, but current direct fetch failed. Neither contradiction nor previous R32 entry is erased.

## Counts / regression

| Metric | Stage40 baseline | Stage41 |
|---|---:|---:|
| Total selected SKU | 356 | 356 (inherited unchanged) |
| Output columns | 77 | 77 (inherited unchanged) |
| New filled XLSX cells | 0 | 0 |
| Corrected XLSX cells | 0 | 0 |
| Core missing fields | 625 | 625 |
| Explicit targeted Midea refrigerant conflicts | 9 | 9 OPEN |
| OEM visual confirmations for these 9 | 0 | 0 |

The 625 fields remain: manufacturer warranty 341, tech documentation 114, pipe pairs 66, refrigerant blanks 63, cassette panels 20, net masses 5, dimension components 16, electrical nominal input 0. This counter excludes 77-column conditional applicability exceptions and the nonblank refrigerant conflicts.

## Blocking issues and next actions

1. Quarantine all 9 targeted SKU from import until exact **Russian OEM edition + suffix + paired outdoor unit compatibility** supports the refrigerant choice. Check whether refrigerant is property of entire installed VRF circuit rather than a unique attribute of unpaired indoor unit.
2. Inspect a directly accessible original OEM PDF **page image** for the exact ATOM B revisions, with model rows and Russian-market identity; index-only excerpts are not sufficient. Old portal is currently down; use Daichi directly or locally provided OEM document.
3. Check MI2-90DLDHN18(At) *liquid/gas tubing assignments* with OEM. IFREEZ has suspected field inversion; do not transfer it.
4. Resume the baseline 66 piping, 63 blank refrigerant, 20 panel, 5 mass, 16 dimensional, 114 technical-doc, 341 manufacturer-warranty investigations and the remaining 77-column applicability web passes, recording source and search outcome for every exact SKU.

## Files

- `STAGE41_9_REFRIGERANT_REVIEW.csv` — 9 exact-SKU historic/current evidence cases.
- `STAGE41_SOURCE_EVENTS.csv` — 7 source-review notes with direct-open status and limits.
- `STAGE41_FIELD_PATCH.csv` — header-only proof of **zero technical field changes**.
- `SESSION_MANIFEST_41_TO_41.md` — next chat resume status.
- Stage41 binary snapshot is exactly the **same bytes as Stage39**, not a newly edited workbook.

### Source quality rule

`CONFLICT_OPEN` and `RETAIL_VERIFIED_OEM_PENDING` are never equivalent to a factory-verified final value. No generic `R410A/R32` pair or seller warranty was imported as a single-valued technical attribute.
