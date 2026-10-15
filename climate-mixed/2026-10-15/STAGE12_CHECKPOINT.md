# Stage 12 — Kentatsu KTDB / Midea V8 — 2026-10-15

**CHECKPOINT — PARTIAL / NOT FOR IMPORT**

- Continued cumulative **356 products / 77 output columns** workbook.
- **20** new previously empty fields: six KTDB panels `1430×53×680`, six indoor masses (KTDB24/30/40 = 29.7 kg; KTDB50/60/72 = 31.6 kg), eight technical PDF references (six KTDB and two Midea MIH).
- Technical source KTDB: https://daichi.business/support/documents/download.php?ID=27751. Contains exact **KTDB24/30/40/50/60/72HZBN1** with **KPU2-D3**, separate dimensions for panel and unit and separate weights. 11 kg is **panel weight** and must not replace 29.7/31.6 kg unit weights.
- Exact Midea source for **MIH160Q4HN18 / MIH180Q4HN18**: https://air-midea.com/support/marketing/download/6515/. A different model-specific engineering publication quotes 1050×55×1050 mm panel while another Midea source quotes 1050×65×1050 mm. **Do not fill ambiguous panel size** until the catalogue edition and exact Russian SKU are confirmed.
- The international Midea `MI2-28Q4DHN18(At)` means 8.0 kW in a different market, while Russian seller cards designate 2.8 kW. Market code collision now explicitly extends beyond Q4C; technical numeric fields NOT cross-copied.
- Daikin FXMQ regional catalog dimensional/consumption conflicts remain OPEN, as do KTGB18 gas pipe and IGC BS45 body dimensions.
- Regression checks passed: KTGV50 720 m3/h, FXKQ20A R410A, Midea Q4C 1.5 kW unchanged, Bosch 900×1327×400, template 356x77 unchanged.
- After stage 12 the **stage10-defined core applicability list** had **972** blank unresolved fields, down from 1061, with 69 additions in stage11 and 20 in stage12. Independent applicability corrections may further revise the denominator without filling values.
- Workbook snapshot: `MIXED_356_77cols_STAGE12_2026-10-15.xlsx`, attached in ChatGPT, binary GitHub push not yet confirmed.
- [Field patch CSV](STAGE12_20_FIELD_PATCH.csv). Remaining files available in ChatGPT: `MIXED_STAGE12_AUDIT_356_MODELS.csv`, `MIXED_STAGE12_OPEN_972_FIELDS.csv`.

**Next:** inspect improperly classified "required" fields and fill only truly applicable model fields. Log corrections separately; never claim WEB PASS complete solely from counts.
