# Stage 20 — Second FILE→WEB extraction + OEM edition conflicts

**2026-10-15. INTERMEDIATE / NOT FOR SITE IMPORT.**

- 25 formerly blank core cells newly filled without overwriting preexisting values. Same 356 products ×77 columns.
- **Kentatsu KLA24/30/40/50/60/72HZAN1**: 6 exact liquid/gas diameters recovered from original user's free-text specifications and rechecked against the 2025 Kentatsu model family catalog; 6 HTML technical catalog references. (12)
- **Kentatsu KZA18/24/30/40/50/60HZAN1**: 6 exact model OEM catalogue HTML links. (6)
- Four body **net** weights added ONLY when different model-year Kentatsu catalogs agree: KZA18/KZA24 **13.5 kg** and KZA50/KZA60 **15.5 kg**. (4)
- For KZA30 and KZA40 two factory catalog revisions disagree on body weight: 2025 June catalogue says 15.5/15.5 kg, the other exact SKU catalog says 13.5/14.5 kg. **Kept blank** and logged, no unwarranted choice.
- KZA30 **gas pipe conflict**: 2025 June catalogue says 12.7 mm vs other OEM edition 9.52 mm; existing 12.7 mm retained only as current recorded value, **FLAGGED OPEN** pending revision/supply confirmation.
- KZA24/KZA30: two exact Russian seller cards report **R410A**; filled under **SELLER_VERIFIED_OEM_PENDING** status, no generic extrapolation to other KZA models. (2)
- Midea MI2-56Q4DHN18(At): exact variant's original user's characteristic block explicitly states liquid/gas **6,35/12,7 mm**. Filled after whole-text second pass, regional web corroboration remains OPEN. (1)
- Stage19 open core 825 → **800**. Full 77-field relevance/source passes and remaining **800** missing core fields still OPEN.
- Technical source 1: https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf.
- Technical source 2: https://daichi.business/upload/iblock/b4d/5rjf3831ekyb4cqv2gz363d324reihkb/K2_DX-PRO-A_2025_180625.pdf.
- Other OEM source conflicting KZA: https://www.c-o-k.ru/library/instructions/kentatsu/kondicionery-promyshlennye/37986/140011.pdf
- [25 field changes](STAGE20_25_FIELDS.csv). XLSX chat attachment `MIXED_356_77cols_STAGE20_KENTATSU_MIDEA_2026-10-15.xlsx`, includes `QA20 каталоги конфликт`. GitHub XLSX binary not yet published.
