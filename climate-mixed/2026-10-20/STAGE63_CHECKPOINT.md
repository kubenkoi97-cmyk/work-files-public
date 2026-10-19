# Stage63: manufacturer exact BSQ(DC) index QA and workbook checkpoint

Latest complete XLSX: MIXED_356_77cols_STAGE63_FIRST50_IGC_BS_BSQ_EXACT_OEM_QA_2026-10-20.xlsx; 729740 B, SHA256 a2c95f15b9fde459c9a9f3143bb71752bcce003f97ac37b297a0205bd912a0d9.
The binary is a downloadable ChatGPT sandbox file; it was NOT uploaded as a GitHub XLSX. Parent Stage61 (722275 B) is still intact.
IGC source (manufacturer domain): https://igc-aircon.com/upload/iblock/8e1/f2umkqwfiqx3p6b65iz03odbvjqw01vo.pdf
Mirror indexed copy: https://www.c-o-k.ru/library/instructions/igc/kondicionery-promyshlennye/38333/141247.pdf
Seven exact model identifiers IMS-BS15/22/28/36/45/56/71NHQ(DC) have two model-specific OEM tables. In manufacturer document, the R410A cell is merged over four exact model columns in first table and three in second, not copied from other suffixes.
Those seven R410A values were ALREADY present in Stage61. No redundant writes or fictitious new completions. 70 existing technical cells matched manufacturer indexed exact-model tables (10 per SKU); original PDF was inaccessible and no visual OEM-page verification is claimed for these 70.
Stage62 added 24 matches from visually opened BS(DC) OEM page and flagged dangerous BS45 cabinet/package discrepancy. Two QA worksheets plus source and Log entries added to Stage63.
artifact_tool exported workbook, reopened successfully; independently parsed full first output sheet XML and verified exactly ZERO changes in all 356×77 product cells, including zero changes in remaining 306 out-of-scope SKUs.
First50 core unresolved remains 41, and optional/conditional applicability unresolved. 0/50 READY FOR IMPORT. Do not automatically assign R410A to the 21 other first50 IGC blank refrigerant cells.
[70 QA matches](STAGE63_BSQ_DC_70_EXACT_OEM_INDEX_MATCHES.csv); [24 visual QA matches](STAGE62_BS_DC_24_EXACT_OEM_VISUAL_MATCHES.csv).
