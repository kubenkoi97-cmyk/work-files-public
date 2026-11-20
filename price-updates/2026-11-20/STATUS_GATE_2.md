# Price update gate 2 — 2026-11-20

Retail source confirmed: `прайс catalog(1).xlsx`, sheet `Worksheet`, SKU in B, recommended retail price in P, RUB. R1 with category sections. No formulas, no merged cells; zero confirmed two-row kits.

**Existing site cards (5,989):** 230 retail prices changed, 426 same price, 1,797 not reliably found, 3,536 discontinued and unchanged. Original rows preserved exactly once; prices verified against match log. Two ambiguous matches plus site duplicates held.

**New candidates:** 28,777 safely selected through SKU canonicalization, source-description identity and duplicate filter. 30,788 catalog lines not automatically added: 19,763 article/name mismatch, 9,485 invalid model identifier under gate, 921 already on site, 323 no recommended retail price, 164 unclear type, 126 conflicting duplicate, 6 duplicate article. A12.4 component-without-price filter removed zero independently confirmed rows.

**Artifact layout:** Main XLSX contains all 5,989 existing + 6,487 new, LOG, CONTROL, price match audit and exceptions. Supplementary 22,290 selected new rows for ventilation valves, fans and automation are provided in a separate CSV and Excel chunks because the XLSX exporter could not handle all 34,766 rows in one workbook. An A12.2 loose-code audit flagged 16 unresolved site cards for human review.

Source and output files are available in the ChatGPT conversation; binary workbook upload to this GitHub repository is not supported through the connected text-only contents action, so no file-download URL is asserted here. No changes have been published to the online shop.