# MIXED Stage95 — 2026-10-26

Latest validated complete 356x77 XLSX: `MIXED_356_77cols_STAGE95_FIRST50_IGC_QV90_AREA_1T60_INDEXED_QA_2026-10-26.xlsx`, **812818 bytes**, SHA256 `24b5ff469fc2202cac8fbba74f955b128ed2a7972899dec0baf42280d999bdfc`, 66 sheets. Full workbook available as ChatGPT file only, NOT as GitHub XLSX binary.

Stage94 parent SHA256 `ab4ca1cb95d12e8544c1a1f0f6d6296a67b00bc5d19616a693ed431757271a36`.

Actual product change: row 32 exact `IMS-QV90NH(DC)`, N32 recommended seller area blank -> **90 m2**. Literal exact-model dealer source: https://igc.com.ru/catalog/vnutrennie_bloki_vrf_sistemy/igc_ims_qv90nh_dc/ . Did not copy 3y warranty or R410A because historic factory generation and contract linkage remain pending.

Additional model-specific technical QA: 6 exact old `IMS-1T...NH(DC)` factory model columns x 10 existing values each, **60 matches 0 discrepancies**. Source https://igc-aircon.com/upload/iblock/8e1/f2umkqwfiqx3p6b65iz03odbvjqw01vo.pdf was searchable/indexed, but original PDF did not open (HTTP 502). Mark as `OEM_EXACT_INDEXED_VISUAL_PENDING`, NOT visually verified.

Independent full XML reimport and 356x77 comparison: exactly N32 changed, **0 changes** in remaining 306 products rows 52-357, all 65 legacy sheets unchanged. First50 physically occupied **1635/3850**, not a completeness percentage. Historical 40 CORE missing remain (21 IGC DC refrigerants, 15 contractual warranties, 4 BS45 dimensions); additional Daikin revision and applicability QA open. **0/50 READY_FOR_IMPORT**.

Canonical next starting point = Stage95 full binary, not older GitHub text. Next: old IGC factory exact refrigerant and system pairing, BS45 cabinet independent original, Daikin region/year, per-model source/field verification.