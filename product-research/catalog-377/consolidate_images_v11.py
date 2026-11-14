#!/usr/bin/env python3
"""Consolidate v11 photo packets for exact 377 unfilled Catalog 744 SKUs.

Original HTML archives stay untouched. Only prior GitHub Releases published by
the current audited workflow are input. A global model/photo manifest is emitted.
"""
import csv, hashlib, json, os, re, subprocess, zipfile
from collections import Counter, defaultdict
from pathlib import Path

REPO="kubenkoi97-cmyk/work-files-public"
SRC=Path("product-research/catalog-377/status/master_status.csv")
OUT=Path("product-research/catalog-377/images-v11-final")
OUT.mkdir(parents=True,exist_ok=True)
DOWNLOADS=Path("/tmp/catalog744-images-v11-releases")
DOWNLOADS.mkdir(exist_ok=True,parents=True)

def batches(a,b,n=15):
    while a<=b:
        end=min(b,a+n-1)
        yield (a,end)
        a=end+1

PACKETS=[
    ("catalog377-images-v11-ktgv-pilot-2026-11-14","Kentatsu_KTGV_images_v11_pilot.zip",63,67),
    ("catalog377-images-v11-kentatsu-067-081-2026-11-14","Kentatsu_KTGV_KTYV_KTZV_images_v11.zip",68,82),
    ("catalog377-images-v11-083-097-2026-11-14","Catalog744_images_v11_083-097.zip",83,97),
]
for a,b in [*batches(2,62),*batches(98,275),*batches(276,378)]:
    PACKETS.append((f"catalog377-images-v11-{a:03d}-{b:03d}-2026-11-14",
                    f"Catalog744_images_v11_{a:03d}-{b:03d}.zip",a,b))
assert len(PACKETS)==27
covered=set()
for _,_,a,b in PACKETS:
    overlap=covered.intersection(range(a,b+1))
    assert not overlap, overlap
    covered.update(range(a,b+1))
assert covered==set(range(2,379)),(len(covered),min(covered),max(covered))

def dl(tag,filename):
    dest=DOWNLOADS/tag
    dest.mkdir(exist_ok=True,parents=True)
    path=dest/filename
    if not path.is_file():
        subprocess.run(["gh","release","download",tag,"-p",filename,
                        "-D",str(dest)],check=True)
    if path.stat().st_size<80: raise ValueError("Empty Release asset "+tag)
    return path

def verified_current_white_skus(rows):
    assert len(rows)==377
    names="".join(x["brand"]+"\t"+x["model"]+"\n" for x in rows)
    h=0x811c9dc5
    for b in names.encode("utf-8"):
        h=((h^b)*0x01000193)&0xffffffff
    assert f"{h:08x}"=="b1d25baf","Unexpected catalog model inventory"

def main():
    master=list(csv.DictReader(SRC.open(encoding="utf-8-sig",newline="")))
    verified_current_white_skus(master)
    photo_counts=Counter()
    series_by_model={}
    seen_paths=set()
    errors=[]
    per_packet=[]
    archive=OUT/"Каталог_744_фотографии_v11_сборка.zip"
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as dst:
        for index,(tag,name,lo,hi) in enumerate(PACKETS,1):
            path=dl(tag,name)
            with zipfile.ZipFile(path) as src:
                assert src.testzip() is None,tag
                sl=[]
                for member in src.namelist():
                    if member.endswith("/"): continue
                    if member in ("SUMMARY.json","PHOTO_SOURCES.csv",
                                  "CONTACT_SHEET.png","README.txt","REVIEW_NOTES.csv"):
                        doc=src.read(member)
                        dst.writestr(f"_REPORTS/{tag}/{member}",doc)
                        if member=="SUMMARY.json":
                            summary=json.loads(doc)
                            per_packet.append({
                                "tag":tag,"url":f"https://github.com/{REPO}/releases/tag/{tag}",
                                "archive":name,"range":f"{lo}-{hi}",
                                "models_target":summary["models_target"],
                                "models_with_jpg":summary["models_with_jpg"],
                                "total_jpg":summary["total_jpg"],
                                "errors":summary["errors"],
                                "missing_html":summary.get("models_without_exact_html",[])
                            })
                        continue
                    parts=Path(member).parts
                    if len(parts)==3 and parts[-1].lower().endswith(".jpg") and re.fullmatch(r"\d+\.jpg",parts[-1]):
                        if member in seen_paths:
                            raise ValueError("Duplicate output product path "+member)
                        seen_paths.add(member)
                        series,model,_=parts
                        series_by_model[model]=series
                        data=src.read(member)
                        # JPEG marker check (complete decoding is done in stage jobs)
                        assert data.startswith(b"\xff\xd8\xff"),(tag,member)
                        photo_counts[model]+=1
                        dst.writestr(member,data)
                    elif len(parts)==3 and parts[-1]=="SOURCES.json":
                        dst.writestr(member,src.read(member))
                    else:
                        errors.append({"tag":tag,"excluded_unrecognized_member":member})
            print(f"PACKET {index}/{len(PACKETS)} {tag}: JPG cumulative {sum(photo_counts.values())}",flush=True)
        assert len(per_packet)==len(PACKETS),(len(per_packet),len(PACKETS))
        assert sum(x["models_target"] for x in per_packet)==377
        models=[]
        for r in master:
            m=r["model"];brand=r["brand"];n=photo_counts.get(m,0)
            original_row=int(r["excel_row"])
            actual_row=original_row+(69 if original_row>=54 else 0)
            status=("CURATED_AWAITING_VISUAL_QA" if n else
                    "NO_EXACT_ARCHIVED_HTML" if r["status"] in ("WRONG_MODEL","NOT_FOUND") else
                    "NO_USABLE_IMAGE")
            models.append({
                "excel_row":actual_row,"brand":brand,"model":m,
                "series_folder":series_by_model.get(m,""),
                "image_count":n,"image_status":status,
                "archive_content_status":r["status"],
                "exact_model_page_url":r["source_url"],
                "original_archived_source_zip":r["archive_download_url"]
            })
        assert len(models)==377
        fields=list(models[0])
        import io
        f=io.StringIO()
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader();writer.writerows(models)
        dst.writestr("_REPORTS/ALL_377_MODELS.csv",f.getvalue().encode("utf-8-sig"))
        stats={
            "scope":"377 unfilled models, verified by exact brand/SKU fingerprint",
            "model_total":377,
            "model_images_curated":sum(x["image_count"]>0 for x in models),
            "image_files":sum(photo_counts.values()),
            "models_without_exact_archived_html":sum(x["image_status"]=="NO_EXACT_ARCHIVED_HTML" for x in models),
            "models_with_no_usable_image_other":sum(x["image_status"]=="NO_USABLE_IMAGE" for x in models),
            "grouped_by_brand":dict(Counter(x["brand"] for x in models)),
            "packets":per_packet,
            "quality_status":"CURATED_AWAITING_VISUAL_QA: gallery and dimensions checked; visual confirmation incomplete",
            "original_HTML_archives_modified":False,
            "source_manifest":"_REPORTS/ALL_377_MODELS.csv",
            "warnings":errors[:100]
        }
        dst.writestr("_REPORTS/SUMMARY_ALL.json",json.dumps(stats,ensure_ascii=False,indent=2))
        dst.writestr("_REPORTS/README.txt",
                     "Фотографии только для 377 товаров БЕЗ ЗАЛИВКИ на листе Каталог 744.\n"
                     "Структура: серия / точная модель / NN.jpg; JPEG 850x850.\n"
                     "Каждая модель проверена по коду; неразрешённые модели не подменены.\n"
                     "Статус всех изображений — предварительно обработаны, ожидают ручной визуальной проверки.\n"
                     "Смотри _REPORTS/ALL_377_MODELS.csv и исходные архивные Release.\n")
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len([x for x in z.namelist() if x.lower().endswith(".jpg")])==sum(photo_counts.values())
    (OUT/"SUMMARY_ALL.json").write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding="utf-8")
    with (OUT/"ALL_377_MODELS.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(models)
    (OUT/"COMPLETION.txt").write_text(
        f"total_models=377\nmodels_with_images={stats['model_images_curated']}\n"
        f"jpgs={stats['image_files']}\nnot_exact_source={stats['models_without_exact_archived_html']}\n"
        f"manual_visual_qa_required=YES\n",
        encoding="utf-8")
    print("OVERALL",json.dumps({k:v for k,v in stats.items() if k!="packets"},
                                ensure_ascii=False),flush=True)
    print("ZIP",archive,archive.stat().st_size,flush=True)
if __name__=="__main__":
    main()
