# MIXED Stage 56 — FIRST 50 ONLY — Seller-warranty correction (2026-10-19)

**SCOPE:** Only Excel output rows 2–51 of Stage55. Remaining 306 products unchanged.

## Data-quality repair
Eight existing values (12 months, column 41 «Гарантия, мес.») were supported **only by the seller's one-year warranty** explicitly written in each exact product's original source `Сбор данных!F[row]`. They were **not evidence for the manufacturer warranty demanded by the original master standard**. These fields were cleared to blank; all eight old values, exact SKU, reason and source rows were retained in `QA56 гарантия первых50`, `Источники`, `Log` and [exact patch CSV](STAGE56_FIRST50_WARRANTY_8_PATCH.csv).

Affected: FXKQ20A, FXKQ25A, KTGV18HZBN1, KTGV24HZBN1, KTGV30HZBN1, KTGV40HZBN1, KTGV50HZBN1, KTGV72HZBN1.

**Do not copy vendor three-year claims from other regional configurations** (e.g. IGC DC5 vs DC) without a documented, applicable manufacturer policy. All 8 now status `OEM_WARRANTY_OPEN`. Clearing unsubstantiated entries is a *quality improvement*, not a loss of verified data.

## Immutable parent and stage artifact
- Parent `MIXED_356_77cols_STAGE55_REAUDIT_356x77_2026-10-19.xlsx` — 423302 bytes; SHA256 `83c1e0414c75af3b38d766e9434bc80a9433fa8f64c96a0c3b1fc7b434ab6bcf`.
- Stage56 true binary `MIXED_356_77cols_STAGE56_FIRST50_SELLER_WARRANTY_CORRECTION_2026-10-19.xlsx`: **425283 bytes**, SHA256 **`498f055b55806eb9c0b7994fb3bf1c4c535e0685055b6e7dae8a1ab5b22e190b`**.
- Workbook full 356 ×77 schema retained, source/archive sheets retained. Only targeted first50 warranties corrected. Value restoration requires manufacturer proof.

**Binary transfer limit:** the XLSX exists in the current ChatGPT sandbox, not uploaded to GitHub via connector; do not invent remote binary link. This remote checkpoint and patch are real GitHub publications.

Next Stage57: fill source-verified `Тип установки` blanks for first50 only, without touching any already filled value.
