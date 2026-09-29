# Hisense image archive — FINAL STATUS

Finalized: 2026-09-30

## Result
- Products from workbook: 276
- Product folders in final archive: 276
- Final JPG files: 1082
- Models with 1 confirmed image: 113
- Models with 2 confirmed images: 32
- Models with 3+ confirmed images: 131
- Missing 01.jpg: 0
- Invalid JPEG/850×850 files: 0
- Known forbidden images remaining: 0
- Forbidden certificate/banner/corporate images removed globally: 264
- Unified ZIP size: 77,053,141 bytes
- Unified ZIP SHA-256: 56cd22de267d23de63631707a6087ea81bc77cf0e0963982abf262b1dfd4b072

## Completed quality gates
- Staged processing in 15 packets
- Exact-model and series-level source search
- Dedicated second pass for low-image-count models
- Dedicated audits for MACS cassette / floor-ceiling / duct, ZKPU, UNIVERSO, Triumph / AR / IR, HiMod AE2
- Exact VRF accessory audit
- Cross-model exact/perceptual duplicate audit
- Global removal of two certificate families, one promotional HVAC banner family and one corporate Hisense/Hitachi image family
- Exact accessory additions where the workbook identifies the accessory model
- Third-pass ZIP/image/folder verification
- Public unauthenticated HTTP download verification

## Exact accessories added
- AVBC-HJDBA: HPE-GNK1 + HYE-VD01
- AVBC-HJFKA: HP-G-NK; exact wireless remote model is not identified in the workbook
- AVS-HJDTD / AVF-H2FDA: HYE-VD01
- AVD-HJDH: HYXE-VA01A and HYXE-VC01
- AVE-HJDDH: HYXE-VC01
- AVD-HJFH: wired controller is specified, but its exact model is not identified in the workbook

## Documented limitations
The archive does not invent model-specific angles where dealers/manufacturers reuse generic renders across models with different physical dimensions. These cases remain explicitly recorded in FINAL_ANOMALIES.csv and FINAL_REPORT.csv.

## Public release
Tag: hisense-images-final-2026-09-30

The public verification job confirmed:
- release page HTTP 200 without authentication
- all 16 ZIP download endpoints returned HTTP 206 to unauthenticated ranged requests
- ZIP signature verified
- all selected report assets were publicly downloadable
- release metadata contains 25 uploaded, non-empty assets
