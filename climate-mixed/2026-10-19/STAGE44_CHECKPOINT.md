# Stage44 — Kentatsu KTZV15HZBN1 / 2026-10-19
**INTERMEDIATE. NOT IMPORT-READY.**

## Technical baseline reconciliation
The user's Library has the newer technical book `MIXED_356_77cols_STAGE43_REFRIGERANT_REVISION_CONFLICT_QA_2026-10-17.xlsx` (555300 B; SHA256 `eef2987a6e4bb6bd0fc8779029ef647a571bf82bad5081af06626da378d4409b`). It was compared with Stage39: **10 original empty cells were filled, none of the previously nonempty product fields changed**: two Daikin FXKQ20/25A net weights (18 kg with *17kg* alternative still disputed), plus eight KTGV exact-family PDF links. Stage43 retains all 356 product positions and 77 original column names, 615 core blank cells. Its checkpoint and source audit are [in the 2026-10-17 folder](../2026-10-17/STAGE43_CHECKPOINT.md). The source-only Stage41/42 reports dated October19 had copied older Stage39 data and **must not supersede this newer technical book**. Retain their Midea/IGC evidence but use Stage43 for technical values.

## Stage44 model pass and patch
- Excel row 60, exact Kentatsu `KTZV15HZBN1`, field 23: `(blank)→6,35/12,7` (liquid/gas pipe diameters in mm), supported independently by exact product cards https://multisystems.ru/catalog/vrf-kassetnye/kentatsu-ktzv15hzbn1 and https://sochi.climate-group.ru/vnutrenniy-blok-vrf-sistemy-kentatsu-ktzv15hzbn1/ . `RETAIL_VERIFIED_DUAL_SOURCES_OEM_PENDING`.
- Same row, conditional column 73: `(blank)→0.46` maximum current in A, exact MultiSystems full specification, `RETAIL_VERIFIED_OEM_PENDING`. OEM visual document pending. No protection circuit breaker/current substitution.
- No manufacturer warranty copied from dealer cards. Do not infer same sizes for neighboring KTZV models.

## Actual Excel preservation/integrity
`MIXED_356_77cols_STAGE44_KTZV15_PIPE_CURRENT_QA_2026-10-19.xlsx` 581672 B SHA256 `3a1f08d2bccbeeeb6db4260355a81e402b9bd03542965b8b40ed4fcc442b7122`. Created by direct `artifact_tool` editing of the full 32-tab Stage43 book, appended rows to `Источники` and `Log`, added 4 audit tabs, total 36 tabs. Cell-by-cell prior/new audit of all **356×77** output cells: **exactly two originally empty field changes** W60 and BU60, 0 previous nonempty overwrites; model order/77 headers preserved. Export reimport confirmed 356×77 and 614 applicable base open rows. Formula-token scan found no direct formula error strings. This latest binary is an **actual ChatGPT sandbox file**, but the available GitHub write connector cannot read container-local binary bytes. **This GitHub checkpoint does not imply a new binary XLSX was published to GitHub.** Stage39 historical binary remains in GitHub; Stage43 parent is in the ChatGPT Library; Stage44 download is to be supplied directly in current chat.

## Reopened exception register
Baseline core applicable blanks **615 → 614**: OEM warranty 341; TECH docs 106; pipes 65; refrigerant 63; decorative panels 20; net masses 3; body dimension parts 16; nominal electric input 0. Additional conditionally applicable fields from 77-column template still need per-model QA; in `QA44 77 колонок` populated/blank counts are rederived per physical cell, not claims of universal applicability.
Old Midea R32/R410A conflicts **9 OPEN**, Daikin mass 17/18 kg **2 OPEN**; all remain quarantine items until original regional OEM edition validation.

## Repro files
[2-field patch](STAGE44_KTZV15_PATCH.csv) · [614 exact blank cells](STAGE44_OPEN_614.csv) · [77-column audit](STAGE44_77_COVERAGE.csv). Next: verify original OEM KTZV15 PDF, proceed with all missing field passes, do not confuse KTYV, KTZV, KTVV and KTLV.
