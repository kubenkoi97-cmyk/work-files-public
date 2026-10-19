# Stage65 — exact IGC BS45 suffix revision check

Scope: only first50; this is a SOURCE-ONLY checkpoint, no product edit.
Latest verified actual workbook remains Stage63, MIXED_356_77cols_STAGE63_FIRST50_IGC_BS_BSQ_EXACT_OEM_QA_2026-10-20.xlsx, size 729740 B, SHA256 a2c95f15b9fde459c9a9f3143bb71752bcce003f97ac37b297a0205bd912a0d9; available in ChatGPT sandbox, not GitHub binary.
Exact first50 Excel row10 IMS-BS45NH(DC), manufacturer-branded 2024 PDF [opened and visually inspected PDF page4 / printed p53]: https://onokom.ru/dok/igc/2024/catalog/2024-catalog-ims-duct.pdf
That exact (DC) table gives body W-D-H 700×470×200 mm, package 1305×580×275 mm, 90 W nominal fan, 34 dB(A), 23.5 kg net, max fan static pressure nominal13 adjustable0–50 Pa.
Body width 700 repeated even for larger blocks despite greatly larger cartons is suspected internal catalog error. Leave body size cells 29/30/31/35 blank, seek independent model-specific dimensional drawing. Neither shipping carton dimensions nor DC4 alternative is valid substitute.
DIFFERENT printed model IMS-BS45NH(DC4) on another manufacturer-branded PDF search INDEX https://split-nastroi.ru/uploads/612e04ce22a69doc573316842/612dfce441ed0.pdf lists body 1160×460×185, package 1350×545×250, fan 80 W, acoustic38dB(A), mass20kg, ESP10/30. This second PDF could not be opened as image because download exceeded browser file cap; OEM_INDEXED_ONLY for the different DC4 SKU. Model revision/year not fully verified.
The two printed model SKUs are NOT identical. Many technical values differ despite same nominal cooling/heating. The old exact (DC) manufacturer source is more relevant to row10, but the anomalous body size remains unconfirmed by an independent drawing.
12-field comparison: STAGE65_IGC_BS45_DC_VS_DC4_REVISION_RISKS.csv. Status: 0 new cells filled; 306 excluded products untouched; 0/50 ready, 41 first50 core blanks remain plus additional field-applicability checks.
Previous Stage63 full workbook and Stage64 checkpoints retained. Do NOT revert to Stage61/55, do NOT overwrite exact (DC) fields with (DC4) data.
