# MIXED STAGE43 — source conflicts and regression, 17 Oct 2026
Status: **INTERMEDIATE; NOT FOR PRODUCTION IMPORT**.

## Baseline
- Source: Stage42 full workbook, `MIXED_356_77cols_STAGE42_KENTATSU_KTGV_DOC_QA_2026-10-17.xlsx`.
- New Stage43 full workbook: `MIXED_356_77cols_STAGE43_REFRIGERANT_REVISION_CONFLICT_QA_2026-10-17.xlsx`.
- Size **555300 bytes**, SHA256 **`eef2987a6e4bb6bd0fc8779029ef647a571bf82bad5081af06626da378d4409b`**.
- Full original 356 models ×77 output columns. **Zero value changes in Stage43**; only QA tab additions, source/log appends, highlighting of conflict cells. Original values and order preserved.
- Remaining **615 core applicable blanks** (including 341 manufacturer warranty and 106 exact technical documentation links). Count unchanged in Stage43; not an all-fields completeness percentage.
- Full binary XLSX generated in chat only; **not verified published to GitHub**.

## Critical 11 field-level conflicts
1. **Daikin FXKQ20A and FXKQ25A**, row 37/38, unit weight: 18 kg according to Daikin EEDEN241 technical PDF (PDF p4, printed p5), but **17 kg** in official Daikin Austria 2026 catalogue for the exact same model labels. We retain 18 provisionally while marking AMBER; resolution requires manufacturer market/revision confirmation. 
  - https://easyspec.daikin.fr/EasySpec/VRV/Documentations/UI/J4_FXKQ-A/Manuel%20technique/ManTech_J4_FXKQ-A.pdf
  - https://www.daikin.at/content/dam/DACE-AT/document-library/catalogues/ac/vrv/Daikin_Katalog_VRV_2026.pdf
2. **Midea MI2-28/36/45/56/71T3DHN18(At)**, rows 299–303, existing workbook R410A vs model-specific MirCli R32; do NOT replace until exact Russian OEM version evidence.
3. **Midea MI2-80T2DHN18(At)**, row 304, refrigerant kept BLANK; model-specific MirCli R32 vs indexed distributor catalog R410A.
4. **Midea MI2-45/90/140DLDHN18(At)**, rows 311, 315, 317, existing R32 vs exact matching Envok R410A; must resolve. Prior Stage38 conflict is preserved.
- RU 2026 EAC declaration identifies possible family model with **suffix X**, not necessarily exact same variant and does not prove R32/R410A; do not infer refrigerant: https://xn----7sbajahheyaepn1ca0aveqcb0fxl.xn--p1acf/document/eaes-n-ru-d-cnra08v0854326/
- See [11-row audit CSV](STAGE43_CONFLICT_QA_11_MODELS.csv). **11 conflicts are not 11 new discoveries**: nine already known Midea, two strengthened Daikin cross-catalogue findings; the value of this stage is explicit regression and import blocking.

## QA and next actions
- Workbook sheets: `QA43 конфликт 11 моделей`, `QA43 открытые 615`, `QA43 сводка`; source and audit trail appended to `Источники` and `Log`.
- Old 341 warranty blanks unchanged; seller promises do not establish manufacturer warranty.
- Kentatsu 8 Stage42 model-specific catalog links pending visual PDF table QA.
- 6+3 Midea refrigerant fields and 2 Daikin weight cells marked conflict; flagged cards must not ship until issue resolved.
- Continue exact-model manufacturer PDF verification, regional/suffix compatibility, model-specific documentation, other base blanks and 77-column applicability; revisit already filled values.
- Preserve all earlier Stage39–42 XLSXs and all checkpoint manifests.
