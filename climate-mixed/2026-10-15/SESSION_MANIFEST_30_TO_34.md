# LONG MIXED SESSION 30–34 — RESUME CONTEXT

**As of 2026-10-15: PARTIAL, DO NOT IMPORT.**

## Single current working version
- [Stage33 complete binary XLSX](https://raw.githubusercontent.com/kubenkoi97-cmyk/work-files-public/main/climate-mixed/2026-10-15/MIXED_356_77cols_STAGE33_QA_2026-10-15.xlsx), 440019 bytes SHA256 `801e4050f3f60c1a8514d181743abe5690fe2d32c0de02570cb08bb81c7e42ba`.
- 356 selected SKUs from original 744, 77 final columns, 388 excluded, previous stages preserved. Archive [Stage25 full history](MIXED_356_77cols_STAGE25_QA_LONG_SESSION_2026-10-15.xlsx) stays immutable.
- Parent is [Stage28 compact workbook](MIXED_356_77cols_STAGE28_COMPACT_QA_2026-10-15.xlsx).

## Stages and sources
- [Stages 30–31](STAGE30_31_CHECKPOINT.md): 6 exact MirCli SKU refrigerants, [CSV patch](STAGE30_31_SIX_REFRIGERANTS.csv), originally empty only; 3 Q4/Q4C R410A + 3 DLD R32.
- [Stage32](STAGE32_CHECKPOINT.md): 6 IMPORTANT R410A/R32 contradictions, [exact cards vs OEM index](STAGE32_MIDEA_6_CONFLICTS.csv). Five T3 pre-existing `R410A` values directly contradicted by `R32` exact seller cards; one MI2-80T2 blank conflicting OEM/retailer. **Unresolved**. Do NOT send these SKUs to production import.
- [Stage33](STAGE33_CHECKPOINT.md): QA 356×77; [631 core open](STAGE33_OPEN_631.csv), [356 model audit](STAGE33_356_AUDIT.csv). No formula errors, no unintended previous nonempty overwrite.
- [Stage34](STAGE34_CHECKPOINT.md): [all 77 columns applicability/coverage](STAGE34_ALL_77_COLUMNS_REAUDIT.csv), conditional fields still OPEN.

## Live gap counts
637→**631** base applicable: OEM guarantee341, tech links114, pipes66, refrigerant63, cassette panels20, net mass10, dimensions16, power1. **This does not certify complete 77-column accuracy.**

## Next exact actions
1. Obtain exact *Russian factory* passport/revision for 5 T3 R410A/R32 conflicts and MI2-80T2 discrepancy. Compare original XLSX data, seller SKU, factory version; preserve opposing records and reason for resolution.
2. Work 66 missing pipe pairs and 63 refrigerants by exact model (incl. DP/A/At suffix); factory first, user priority domains second, other reputable sources if needed; record each view and why unresolved.
3. Complete individual PDF inspection for 114 documentation links and OEM guarantee terms for 341 (do not copy retailer duration).
4. Recheck every column conditionally applicable across every product; not just baseline open list. Update per-field Log/Источники/Exceptions and report full WEB pass by model/domain.
5. After each sizeable batch release patch CSV + Markdown GitHub immediately and full XLSX as verified binary blob with exact SHA; old versions immutable. No premature FINAL.

Prior history and conflict ledger: [Stages26–29](SESSION_MANIFEST_26_TO_29.md), [Stages22–25](SESSION_MANIFEST_22_TO_25.md).
