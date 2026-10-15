# STAGE 10 — Kentatsu KLA and Daikin FXKQ, 15 October 2026

**INTERMEDIATE. DO NOT IMPORT INTO PRODUCTION.**

- 12 exact models in this pass; **23** previously empty applicable cells filled.
- Kentatsu KLA24/30/40/50/60/72HFAN1: 6 supply voltages (220–240 V) and 6 links to factory PDF https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf.
- Daikin FXKQ20/25/32/40/50/63A: 6 factory tech document references; FXKQ32/40/50/63A also 4 voltages (220–240 V); FXKQ63A minimum fan sound pressure 38.5 dBA according to exact manufacturer's noise chart in https://easyspec.daikin.fr/EasySpec/VRV/Documentations/UI/J4_FXKQ-A/Manuel%20technique/ManTech_J4_FXKQ-A.pdf. 
- The manufacturer FXKQ-A PDF was inspected including its sound chart (web PDF screenshot). Verified product suffixes and independent distinction between electrical input (kW) and power supply (V).
- All 356 selected products / 77 final product columns preserved, previous stages preserved.
- Full applicable-core-cell exception audit rerun across **356 products**. Remaining unconfirmed applicable core cells **1061**, down from stage 9: 1084 (delta -23). Stages 8/9/10 audit trajectory: **1132 → 1084 → 1061**.
- Regression checks: KTGV50HZBN1 airflow 720 m³/h and Daikin FXKQ20A refrigerant R410A kept.
- Still open: manufacturer warranty 341; exact technical docs 287; refrigerant 135; piping 105; series 94; panel dimensions 43; indoor net mass 26; duct pressures 8; Midea MI2-100Q4DHN18(At) heating; Midea MI2-22Q1DHN18(At) input power; several block dimensions incl. Bosch outdoor.
- Market-code collision of seven Midea MI2-Q4C variants and KTGB18HZBN1 9.52-vs-12.7-mm gas-line conflict remain UNRESOLVED, with no guesses.
- Full model-by-model deep web-pass across all 356×77 model-applicable fields remains uncompleted. Empty here = **not confirmed**, NOT verified unavailable.

Artifacts:
- [23 changed fields](STAGE10_FIELD_CHANGES.csv) — GitHub CSV.
- Chat XLSX `MIXED_356_77cols_STAGE10_KLA_DAIKIN_2026-10-15.xlsx` with stages 1–10, including QA10 current exceptions (binary has **not** been uploaded to GitHub).
- Chat CSV `STAGE10_GLOBAL_AUDIT_356.csv` offers current model-level exceptions.

Next priorities: refrigerant and piping 135/105, cassette panels 43, technical documentation 287, warranty 341, and conflict resolution backed by regional exact-model manufacturer datasheets.
