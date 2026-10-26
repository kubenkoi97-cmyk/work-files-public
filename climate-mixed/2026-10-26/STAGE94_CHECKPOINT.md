# MIXED Stage94 technical batch — validated checkpoint

Workbook: `MIXED_356_77cols_STAGE94_FIRST50_IGC_4T_AREA_DAIKIN_OEM_SOUND_2026-10-26.xlsx` (809539 B; SHA256 `ab4ca1cb95d12e8544c1a1f0f6d6296a67b00bc5d19616a693ed431757271a36`). Original Stage93 = `c9f7a5a232202006ae7d6d0397f1def5b8e75fa9ae57e31dece052a28ccf8cb6`.

**2 actual first50 changes, only one new technical-market value:** N26 from blank to **71** for exact old IGC `IMS-4T71NHQ(DC)`, source [archival official dealer](https://igc.com.ru/catalog/arkhiv_modeley/igc_ims_4t71nhq_dc/), using own literal attribute `Площадь, кв.м. 71` not separate guidance `до 80`. AQ37 appended manufacturer [Daikin FXKQ20A sound chart](https://www.daikin.es/content/dam/MDM/TechnicalDrawings/VRV/fxka-a_fxkq-a/lv/FXKA20A_FXKQ20A_spres_4D151078_ES.pdf) with visual factory P1 confirmation 32/27.5/22.5 dB(A) (cooling high/medium/low). Excel U37 already 22.5, confirmed but no double-count.

## New risk finding
Exact short names in [official Daikin Spain 2025 catalog](https://www.daikin.es/content/dam/internet-spain/AVANCE-TARIFA-2025.pdf) show FXKQ20A/FXKQ25A **17 kg**; existing workbook 18 kg, while both remain edition-ambiguous. **Do not copy 17 over 18 until market/revision/serial reconciled; mark OPEN_CONFLICT.** Other four FXKQ net masses 18/23/23/23 match index. Original PDF index was read, but not visually accessible due full document size. Never claim 2025 mass visually verified.

## Independent 356×77 after-export test
Compared **27412** product cells. Exactly `N26` and `AQ37` differ; unchanged SKU identities, 77 headers, original 62 sheets' values, all 306 non-target items. Final 65 sheets. First50 occupancy **1633→1634**, historic 40 core unfilled and conditional gates remain. **0 release ready**.
