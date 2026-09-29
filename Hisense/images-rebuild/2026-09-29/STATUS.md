# Hisense image rebuild — STATUS

Updated: 2026-09-29

## Repository policy
All non-confidential work artifacts for this task are stored in this public repository.
Large work is split into stages/packages and each stage is persisted before the next stage.

## Scope
- Source catalog: 276 products
- 22 series
- 15 staged packets
- Target image format: JPG, 850×850, white background
- Every model is checked separately
- Exact visual configuration matters: dimensions, generation, chassis, fan count, panel, remote/controller, colour and composition

## Stages

### 0. Public workspace migration
- [x] Public repository initialized
- [x] Rebuild engine copied to public repository
- [x] Compact 276-product manifest copied to public repository
- [x] Packet 01 source registry copied
- [x] Public packet workflows created

### 1. Packet 01 — AVC-HJDBA + AVY-HJDA
- [x] Curated rebuild logic prepared
- [x] Exact HPE-DNK1 panel source confirmed
- [x] Exact HYE-VD01 remote source confirmed
- [x] AVY exact-product dealer pages used
- [ ] Public packet branch/release finalization running

### 2. Packets 02–15
- [x] Exact packet composition defined
- [x] Parallel public rebuild workflow created
- [x] Cross-category Hisense Ukraine thumbnails explicitly filtered
- [ ] Public packet branches being rebuilt

### 3. Mandatory second pass
Priority:
1. models with 0 images
2. models with only 1 image
3. models with only 2 images
4. missing exact remote/panel
5. weak preview
6. visually suspicious sharing across distinct models

Current high-priority anomalies:
- HFRWE-65DGF/SYS — HiMod AE2
- HFRWE-130DGF/SYS — HiMod AE2
- MACS packets with only one confirmed image
- ZKPU models with only one confirmed image

### 4. HiMod AE2 recovery
Research found exact product pages and usable product imagery for both missing models:
- HFRWE-65DGF/SYS
- HFRWE-130DGF/SYS

Exact-model pages found on:
- official Hisense Russia dealer site
- iClim exact product pages
- 1Clim exact product pages
- additional dealer pages

Next action: ingest exact model imagery, normalize to 850×850 and rebuild packet 15.

### 5. Third anomaly pass
Will check:
- missing 01.jpg
- 1/2-file folders
- same image set reused across distinct body sizes
- 1-fan/2-fan/3-fan conflicts
- missing confirmed controller/panel
- exact duplicates only
- final ZIP integrity

### 6. Final delivery
- [ ] unified REPORT.csv
- [ ] unified README.txt
- [ ] unified anomalies log
- [ ] final ZIP(s)
- [ ] public direct-download links verified without authentication


## Progress update — second pass
- [x] Packet 08 MACS cassette: exact-model audit completed for all 30 models.
- [x] Packet 08: 28 exact-model renders added from exact iClim pages.
- [x] Packet 08: targeted C45/C51 audit completed.
- [x] Packet 08: C45 and C51 exact/validated renders added.
- [x] Packet 08 final curated result: 30/30 models have 2 images; ZIP verified.
- [x] ZKPU exact/series audit completed: dealer pages reuse generic series imagery across distinct sizes; no unsafe cross-size promotion of generic images.
- [x] UNIVERSO exact-model audit completed: official exact product pages reuse only two renders across eight models with materially different dimensions, so reused renders are treated as generic and not accepted as model-specific additions.
- [ ] MACS duct (69 models) exact-gallery audit running.
- [ ] MACS floor/ceiling (9 weak models) exact-gallery audit running.
- [ ] Packet 15 Triumph/AR/IR exact-gallery audit running.
