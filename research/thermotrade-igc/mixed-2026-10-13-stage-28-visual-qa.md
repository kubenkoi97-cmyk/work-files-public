# MIXED stage 28 — KZA visual PDF QA addendum (2026-10-13)

**Scope:** Kentatsu KZA18HZAN1, KZA24HZAN1, KZA30HZAN1, KZA40HZAN1, KZA50HZAN1, KZA60HZAN1; stage28 Excel rows 287–292. Other stage28 data and history remain intact.

## New evidence — actual visual page inspection
A one-page **manufacturer 2025 DX PRO A catalogue, page 43** was opened and the PDF page **visually screenshot-inspected**. The six model headers and every numeric column align. Primary chosen model-specific A/B values (cooling, heating, 30 W electrical draw, 3-speed airflow, sound pressure, supply voltage, gas/liquid/drain diameters, body and panel dimensions/masses) were verified against the rendered page:
https://onokom.ru/dok/kentatsu/2025/catalog/2025-catalog-dx-pro-a-kza-vrf.pdf

This supersedes the earlier note saying primary KZA PDF page had **not** been visually checked; **only this one-page primary source is visually verified**. The alternate manufacturer catalogue **c-o-k 140011.pdf, p.86**, has **not** been visually verified, and the model-version conflicts remain open.

## Accessory and drainage QA
- The chosen 2025 page explicitly says indoor units ship **without remote controllers**. The depicted optional controllers are **KWC-05A (wired)** and **KIC-101A (infrared)**; both added to each model's specifications as options, not included parts.
- Drain pump and condensate lift **700 mm** are indicated by the **alternative catalogue/dealer**, *not* by the visually inspected 2025 one-page catalogue. The updated Excel A/B and QA distinguish this and request the actual installation passport.
- Compatible **KPU65-RA** is identified separately from the indoor body; panel parameters are not treated as body dimensions and inclusion in standalone SKU is not assumed.
- Dealer 300 W vs model-specific manufacturer 30 W discrepancy unresolved; 30 W remains provisional main value.

## Workbook and validation
**Updated XLSX**: `MIXED_Термотрейд_IGC_этап28_KZA_реаудит.xlsx`, **258208 bytes**, SHA-256 **ccdf55f49d1c4faa2f608c45180137e28e2e578574ceb2c9d471fbc48c99735a**.
Delivered in the user conversation (binary has **not** been uploaded into this GitHub repository).

- **265/744** A+B populated (6 newly added KZA), **479** empty.
- For KZA, 26 specification lines per model (an additional model-source-backed controller-options line).
- **14 sheets**; original 744-row 15-column source sheet is identical to previous workbook.
- Previously populated A/B entries and all 744 working identities C/D/E/I identical.
- No partially populated A/B pairs, no formula errors detected in the working sheet.
- The distinct sheet `MIXED — аудит этап 28` and QA/fullness sheets now explicitly reflect actual **primary visual PDF QA passed / alternative visual PDF QA remains open**.
- Full completeness remains **UNPROVEN** for these models due to divergent catalog editions and incomplete per-domain/JS verification.

Stage28 main report: [stage28](mixed-2026-10-13-stage-28.md); [six exact new models](mixed-2026-10-13-stage-28-delta.csv); [older model re-audit](mixed-2026-10-13-stage-28-reaudit.csv).

## Next priority
KRA72/80/90/100/115/125/140HFAN1 after stage28. Continue separate earlier-populated model audit, with focused conflict reconciliation for KTTB60HZBN1 and KGA115HZAN1 plus regional Midea/Daikin problems.
