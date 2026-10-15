# MIXED climate catalog — STAGE 22, source recovery
2026-10-15. **PARTIAL / WEB-QA OPEN / NOT FOR IMPORT**

## Verified stage
- Source of truth: `MIXED_356_77cols_STAGE21_FULL_QA_2026-10-15.xlsx` (previous full binary on GitHub).
- Revisited the exact-SKU `Сбор данных` row's `Исходный источник` against `QA21 пробелы 800`.
- Recovered **107 distinct empty TECH_DOCUMENTATION cells** by linking directly to the original row's existing technical PDF: **Kentatsu 76**, **Midea 31**, spread over **13 different document URLs**.
- Wrote complete HTML anchor `<a href="...pdf" target="_blank" rel="noopener noreferrer">Техническая документация / каталог (PDF)</a>` to 77-column target field **43**, never changing any other prior field.
- Created sheet `QA22 ссылки FILE` with 107 exact row/model/URL/status entries. Appended 107 change rows to `Log` explaining original-file provenance.
- Mechanical before/after diff: **zero unintended changes** to the 356×77 target table; **no previously nonblank fields overwritten**.
- Recalculated applicable-core missing count: **800 → 693**. Remaining: warranty 341; refrigerant 117; technical documentation 114; liquid/gas piping 74; panel 20; net weight 10; W/H/D/body total 16; power 1.
- Important distinction: all links were already in original product's SOURCE row (FILE). Where the source PDF was not page-reviewed, link is marked **PDF_VISUAL_QA_OPEN**, not fully verified technical documentation. A general manufacturer catalogue may contain many products and should not be misrepresented as the exact SKU's personal manual.
- Internal ChatGPT files: `MIXED_356_77cols_STAGE22_FILE_DOC_LINKS_2026-10-15.xlsx`, `STAGE22_107_PDF_LINKS.csv`, `STAGE22_OPEN_693.csv`. GitHub real binary checkpoint will be uploaded with the next cumulative stage once verified.
- Mandatory full exact-model web-pass, including all user-priority websites and external conflict resolution, remains **OPEN**.

## Quality next pass
1. Inspect model-specific refrigerant and piping sources, starting with exact regional SKUs and factory model tables.
2. Visually check a sample of the source PDFs if retrieval permits, downgrade stale links.
3. Re-audit 356 rows ×77 and report all exclusions and unresolved manufacturer warranty.
4. Publish cumulative next-stage binary XLSX to public repo with a matchable Git blob SHA. Keep this record historical.
