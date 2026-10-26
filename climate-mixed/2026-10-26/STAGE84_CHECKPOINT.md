# MIXED Stage84 — exact KTGV24 / KTGV60 maximum-current fills (2026-10-26)

**Parent:** Stage83 52-sheet FULL XLSX, 788556 bytes, SHA256 `45c096e1fae41833e8f5bdeac66b5380999ece248b1a4a462d23cff0673dbff0`.

**Actual Stage84 exported full XLSX** `MIXED_356_77cols_STAGE84_FIRST50_KTGV24_KTGV60_CURRENTS_2026-10-26.xlsx` 789821 bytes SHA256 `68db42147ce5ccf5e529eef89bfb4d1625a4147b05fd07def88d73724235a07d`, 53 sheets (52 originals preserved, new `QA84 2 точных тока`). **This XLSX is a verified ChatGPT artifact, NOT uploaded as binary to GitHub**.

## Real product values changed
- Excel row46, `KTGV24HZBN1` col73 max operating current blank → **0.29 A**; both Envok and TD Komfort independently show **exact model** and **max current**. Factory visual original remains open.
- Excel row50, `KTGV60HZBN1` col73 max operating current blank → **0.51 A**; both Envok and TD Komfort exact model; additional Coldcontrol exact match. Factory visual original remains open.

## Regression: all original 356 × 77 product cells (27 412 positions)
- Independent OOXML re-import/diff: **exactly 2 changes**, both the cells above; **0 changes** in all other 306 product rows52–357, headers unchanged, SKU order unchanged, all original non-product/history sheets retained. 2 log entries appended, one new audit sheet added.
- First50 physically occupied fields **1621 → 1623 / 3850**, blank **2229 → 2227**, including N/A and commercial fields. This is NOT a readiness percentage.
- Historical core unfilled **40 unchanged** (21 exact IGC refrigerants + 15 conditional Daichi warranties + 4 disputed IMS-BS45 body sizes). **0/50 READY_FOR_IMPORT**, **0/50 certified TECH_READY_COMMERCIAL_BLOCKED**; edition and coverage gates remain.
- No OEM PDF image/page was claimed inspected for these new current values. Retail dual-source values are an intermediate evidence tier.

## Delivery caveat
GitHub connector in this session accepts text/blobs but cannot ingest binary bytes directly from the container; archived text and source evidence here. The verified full XLSX is downloadable in ChatGPT. Do not label a nonexistent repository path as the workbook.
