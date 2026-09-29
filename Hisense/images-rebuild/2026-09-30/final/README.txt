HISENSE — FINAL IMAGE ARCHIVE
Finalized: 2026-09-30

Coverage:
- 276/276 workbook products represented by a model folder.
- 1082 final JPG files.
- Every model folder has 01.jpg: yes.
- Every JPG verified as JPEG 850x850: yes.
- Known forbidden certificate/banner/corporate images removed: 264.

Quality process:
- Exact-model/series searches were performed in staged packets.
- Mandatory second pass performed for 0/1/2-image models and missing panel/controller cases.
- Dedicated audits performed for MACS cassette, floor/ceiling and duct models, ZKPU, UNIVERSO, Triumph/AR/IR, HiMod AE2 and VRF accessories.
- Third-pass cross-model hash audit used to identify hidden certificates, banners, corporate imagery and suspicious shared renders.
- Two MirCli/Hisense certificates, a Hisense HVAC marketing banner and a Hisense/Hitachi corporate image family were removed globally.
- Generic dealer renders were not treated as distinct model images when different physical dimensions could not be visually verified.

Exact accessories added where the workbook identified the model:
- AVBC-HJDBA: HPE-GNK1 panel + HYE-VD01 remote.
- AVBC-HJFKA: HP-G-NK panel; wireless remote left unresolved because exact model is not specified.
- AVS-HJDTD / AVF-H2FDA: HYE-VD01 remote.
- AVD-HJDH: both HYXE-VA01A and HYXE-VC01 retained because both are explicitly listed.
- AVE-HJDDH: HYXE-VC01.

Documented limitations (not hidden or guessed):
- AVBC-HJFKA: source workbook specifies a wireless remote but does not identify its exact model; no guessed remote image was added.
- AVD-HJFH: source workbook specifies a wired controller but does not identify its exact model; no guessed controller image was added.
- MACS floor/ceiling and duct fan coils: targeted exact-model dealer audits showed reused generic renders across dimensionally different models; generic repeats were not used to inflate galleries.
- ZKPU: exact-model pages mainly expose shared series component/marketing images; only safe product imagery was retained.
- UNIVERSO and Triumph: exact dealer pages reuse renders across models with different dimensions; only safe confirmed imagery was retained.
- HFRWE-65DGF/SYS: only one independently confirmed exact-model clean render was found after the dedicated second pass.

Files:
- REPORT.csv — one row per product/model.
- ANOMALIES.csv — source limitations that remain after the second/third pass.
- SOURCES.csv — collected source registry plus exact accessory additions.
- REMOVED_FORBIDDEN_IMAGES.csv — every globally removed forbidden image.
- ACCESSORY_ADDITIONS.csv — exact panels/controllers/remotes added in finalization.
- CROSS_MODEL_DUPLICATES_FINAL.csv — remaining cross-series exact duplicates, including legitimate shared accessories.
- VERIFY.txt — mechanical validation results.
