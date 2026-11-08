#!/usr/bin/env python3
"""Two independent gates: exact HTML archived vs. original page content completeness.

Do not overwrite archived originals, and do not count a wrong suffix as an
original. Uses verified master_status.csv created from authenticated ZIP audit.
"""
import csv,json
from pathlib import Path
from collections import Counter
ROOT=Path("product-research/catalog-377")
SRC=ROOT/"status/master_status.csv"
OUT=ROOT/"status"
with SRC.open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))
assert len(rows)==377
result=[]
for x in rows:
    status=x["status"]
    archive=(x.get("archive_download_url") or "")
    zip_verified=x.get("zip_verified","")
    html_captured=(status in ("COMPLETE","PARTIAL") and bool(x.get("source_url")) and bool(archive) and zip_verified=="YES")
    descriptor=(status=="COMPLETE" and x.get("has_description")=="True")
    photos=(int(x.get("image_count") or 0)>0)
    wrong=status=="WRONG_MODEL"
    result.append({
        "excel_row":x["excel_row"],"brand":x["brand"],"model":x["model"],
        "exact_original_html_captured":"YES" if html_captured else "NO",
        "original_html_description":"YES" if descriptor else "NO",
        "exact_gallery_photo_files":"YES" if html_captured and photos else "NO",
        "zip_integrity_verified":"YES" if html_captured else "NO",
        "source_url":x["source_url"],"zip_archive_url":archive,
        "content_gate":status,
        "quarantined_wrong_model_url":x.get("rejected_source_url","") if wrong else "",
        "outstanding_action":(
           "NONE: complete source and archive verified" if status=="COMPLETE" else
           "Find additional exact-SKU original with its own narrative; preserve current original HTML" if status=="PARTIAL" else
           "Find historical EXACT-SKU individual product page; DC5/7 not accepted" if status=="WRONG_MODEL" else
           "Discover genuine exact-model page and its photo gallery" )
    })
with (OUT/"html_capture_matrix.csv").open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(result[0]))
    w.writeheader();w.writerows(result)
n=Counter(x["content_gate"] for x in result)
captured=sum(x["exact_original_html_captured"]=="YES" for x in result)
summary={
   "total_exact_skus":377,"verified_original_html_and_photos":captured,
   "original_page_also_has_product_description":sum(x["original_html_description"]=="YES" for x in result),
   "verified_original_html_but_no_independent_description":sum(x["content_gate"]=="PARTIAL" for x in result),
   "wrong_model_suffix_quarantined":n["WRONG_MODEL"],
   "exact_individual_page_unavailable":n["NOT_FOUND"],
   "statuses":dict(n),
   "important":"Original HTML capture and data-complete source are separate gates. PARTIAL does not mean HTML/photos missing."
}
(OUT/"html_capture_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
(OUT/"html_capture_readme.md").write_text(
   "# Подлинные HTML-страницы и полнота содержания — отдельные статусы\n\n"
   f"Всего **377** уникальных SKU. **{captured}** оригинальных HTML с фотографиями фактически получены и проверены. "
   f"Из них **{summary['original_page_also_has_product_description']}** имеют самостоятельное описание в карточке продавца, "
   f"а **{summary['verified_original_html_but_no_independent_description']}** — содержат характеристики и фото без отдельного описания.\n\n"
   f"**{n['WRONG_MODEL']}** HTML относятся к неподходящему суффиксу и изолированы; **{n['NOT_FOUND']}** пока не имеют точного HTML.\n\n"
   "См. [поартикульную матрицу](./html_capture_matrix.csv). Неполное описание продавца нельзя исправлять подменой оригинала текстом из PDF.\n",
   encoding="utf-8")
print("HTML_CAPTURE_MATRIX",json.dumps(summary,ensure_ascii=False),flush=True)
