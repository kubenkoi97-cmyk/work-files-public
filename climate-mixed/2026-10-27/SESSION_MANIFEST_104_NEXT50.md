# MIXED — Stage104 NEXT50 canonical checkpoint (2026-10-27)

Latest full verified workbook: `MIXED_356_77cols_STAGE104_NEXT50_ALL50_AREA_SOURCES_AUDIT_2026-10-27.xlsx`. **834581 bytes**; **SHA256 6c1c02b52e8252bfc38ca2306db9d81e9f5921b76c3d515fe187bd47141cf687**; 74 worksheets, 356 products ×77 fields.
Latest complete handoff archive: `MIXED_NEXT50_STAGE104_COMPLETE_HANDOFF_2026-10-27.zip`; **SHA256 b429f9845561e6d00df2ceb96b81bf037c90616784b7174d30b56885a13239fc**; 13 verified members; full workbook plus 11 audit reports and originating detailed master prompt. **Both binary files are available as conversation attachments, not uploaded to GitHub.** Do not reconstruct the Excel from GitHub text sources.

Source Stage103 complete workbook SHA256 `b157bad80f241fc373fc62271f167097f20d7015b831923e37c8de5f1cb57ba2`, 73 worksheets, was the input.
New Stage104: **23 expected area values** `Наполнение MIXED!N79:N101`; exact model-specific *retail recommended areas*, NOT OEM heat-load calculations. 50/50 area occupied: 8 baseline not newly reconfirmed, 19 Stage103 exact single-retail, 23 Stage104 exact retail (3 have two retailer sources). Active second 50 fill **1561→1584 out of 3850**.

Independent full-writer-and-reader XLSX regression verified exactly **23 expected** changes, 0 unexpected out of 27,412 product cells; 306 protected rows untouched, all 73 previous worksheets preserved by cell value. One new worksheet `QA104 NEXT50`.

**TECH_READY 0/50, READY_FOR_IMPORT 0/50.** Original `0` prices and `100` stock values are placeholders, not live commercial figures. First50 frozen by user; later256 protected.

Engineering spotcheck KTLV15: exact existing `Сбор данных!F79` shows 10 (10–50) Pa; retailer 10 Pa nominal is compatible with target max 50 Pa, so no overwrite. KTKV80 40 (10–160) Pa nominal/max distinction likewise. OEM manuals KTVV-HZBN1 and KTZV-HZBN1 indexed but direct PDFs HTTP 404; no visual OEM PDF validation. Older HQAN1 documentation does not establish exact HZBN1 specs.

Outstanding SKU-specific factory evidence: piping, controls/panels/accessories, supply current, precise dimensions, installation drawings, media, supplier warranty, real owner pricing and stock. Exact audit CSV and regression report are included inside user's complete ZIP. This Github commit is only the **textual checkpoint**.
