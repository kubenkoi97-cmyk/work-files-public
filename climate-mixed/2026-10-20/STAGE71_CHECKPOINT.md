# Stage71 — first 50 exact source articles (2026-10-20)

**REAL TECHNICAL EXCEL EDIT. NOT FULL IMPORT READY.** The output's column 6, `Артикул [CML2_ARTICLE]`, was physically blank in ALL target rows 2–51 even though every corresponding original `Сбор данных!C` contains the literal exact model designation.

Applied **exactly 50 old-empty→original FILE literal article** fields, preserving punctuation, spaces and suffix. Examples: `IMS-BS22NH (DC)` has a space; `IMS-K22NH(DC)` does not; `FXKQ20A`, `KTGV72HZBN1` unchanged. The original master prompt explicitly classifies SKU article as **FILE-ONLY**, not a value to scrape from WEB. Each of 50 rows was identity-checked against its own exact product name.

Binary `MIXED_356_77cols_STAGE71_FIRST50_50_EXACT_FILE_ARTICLES_2026-10-20.xlsx`, **747878B, SHA256 `30bc279577983554a8167bbe82856a067cead115d4ae6995cb4614d46170c49e`**, parent Stage70 741178B. Built using artifact_tool, exported and separately re-read. All **356×77 output cells** except the 50 precise article entries stayed identical; all 306 out-of-scope SKU rows 52–357 unchanged, original source text unchanged, previous 35 QA sheets retained, new QA71 plus append-only Источники/Log. 

**Caveat:** Restoring exact FILE model values in article column is high-confidence identification, but **not** proof that a separate supplier order/part number equals this model-code string. The original FILE supplies the model designation, not an independently asserted manufacturer part number. If importing CML2_ARTICLE requires another ID convention, validate that external system mapping before go-live.

[50 exact old/new patch](STAGE71_FIRST50_50_ARTICLES_PATCH.csv). No other 306 edited. 0/50 import ready.
