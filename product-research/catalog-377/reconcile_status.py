#!/usr/bin/env python3
"""Audited 377-model index from exact-model archive statuses."""
import base64,csv,gzip,hashlib,io,json
from collections import Counter
from pathlib import Path

ROOT=Path("product-research/catalog-377")
STAT=ROOT/"status"
def inventory():
    s=gzip.decompress(base64.b64decode((ROOT/"source-inventory.tsv.gz.b64").read_text().strip())).decode("utf-8")
    assert hashlib.sha256(s.encode()).hexdigest()=="00ce0e59ca2e3a67074285a21d84c538172b12a6c990c2caef1ddaa6afa3808b"
    rows=list(csv.DictReader(io.StringIO(s),delimiter="\t"))
    assert len(rows)==377 and len({(r["brand"],r["model"]) for r in rows})==377
    (ROOT/"inventory.tsv").write_text(s,encoding="utf-8")
    return rows

def all_states():
    states={}
    for prefix in ("batch-","recovery-batch-","deep-batch-","supplemental-batch-","supplemental-v2-batch-","igc-http-batch-","midea-batch-","final-sweep-batch-"):
        for p in sorted(STAT.glob(prefix+"*.csv")):
            tag=p.stem[len(prefix):]
            with p.open(encoding="utf-8-sig",newline="") as f:
                for row in csv.DictReader(f):
                    if not row.get("model"):continue
                    r=dict(row)
                    # The original Gorodskie-Sistemy archives were mistakenly
                    # tagged COMPLETE by a generic navigation-text heuristic.
                    # This seller publishes exact photos and specs but NO
                    # independent product description. Keep the genuine HTML
                    # and image assets, but correct that status to PARTIAL.
                    if (r.get("brand")=="Kentatsu" and
                        r.get("model","").startswith(("KTKB","KTTB","KTHB")) and
                        "gorodskie-sistemy.ru" in r.get("source_url","")):
                        r["status"]="PARTIAL"
                        r["has_description"]="False"
                        r["reason"]="Original seller HTML has exact SKU, photos, and specs but no product-only description"
                    root="https://github.com/kubenkoi97-cmyk/work-files-public/releases/"
                    release=("catalog377-"+prefix)+tag
                    r["archive_release_url"]=root+"tag/"+release
                    r["archive_download_url"]=root+"download/"+release+"/catalog377-"+tag+".zip"
                    r["result_stage"]=prefix.rstrip("-")
                    k=(r["brand"],r["model"])
                    old=states.get(k)
                    # Prefer confirmed complete sources, then partial pages
                    # with local product photos. Never downgrade PARTIAL to
                    # NOT_FOUND or COMPLETE to PARTIAL after a failed retry.
                    rank={"COMPLETE":3,"PARTIAL":2,"NOT_FOUND":1,"ERROR":0}
                    def quality(row):
                        return (rank.get(row.get("status"),-1),
                                int(row.get("downloaded_product_photos") or 0),
                                (row.get("has_description")=="True"),
                                (row.get("has_specs")=="True"),
                                {"supplemental-batch":1,"supplemental-v2-batch":3,"final-sweep-batch":4}.get(row.get("result_stage",""),2))
                    if old and quality(old)>=quality(r):
                        continue
                    states[k]=r
    return states

def main():
    inventory_rows=inventory()
    states=all_states()
    final=[]
    for x in inventory_rows:
        st=states.get((x["brand"],x["model"]),{})
        final.append(dict(
          excel_row=x["row"],brand=x["brand"],model=x["model"],
          status=st.get("status","UNPROCESSED"),source_site=st.get("site",""),
          source_url=st.get("source_url",""),image_count=st.get("downloaded_product_photos",""),
          has_description=st.get("has_description",""),has_specs=st.get("has_specs",""),
          archive_release_url=st.get("archive_release_url",""),
          archive_download_url=st.get("archive_download_url",""),
          stage=st.get("result_stage",""),reason=st.get("reason","")
        ))
    # Independent authenticated ZIP audit: store both good captures and
    # quarantined wrong-SKU pages. Never treat (DC5) as the requested (DC).
    qa={}
    for shard_file in sorted((ROOT/"audit-v2").glob("integrity-shard-*.csv")):
        with shard_file.open(encoding="utf-8-sig",newline="") as fd:
            for rec in csv.DictReader(fd):
                k=(rec["brand"],rec["model"])
                if k in qa: raise RuntimeError("Duplicate QA source record: "+str(k))
                qa[k]=rec
    for row in final:
        row["zip_verified"]="NOT_CHECKED"
        row["rejected_source_url"]=""
        row["rejected_archive_url"]=""
        rec=qa.get((row["brand"],row["model"]))
        # QA applies only to the specific chosen archive release.
        if not rec or not row.get("archive_release_url","").endswith("/releases/tag/"+rec["release_tag"]):
            continue
        if (rec.get("zip_integrity")=="OK" and rec.get("reason")=="OK"
                and rec.get("file_presence")=="YES"
                and rec.get("exact_heading")=="YES"):
            row["zip_verified"]="YES"
        elif rec.get("reason")=="SKU not in product heading":
            row["zip_verified"]="WRONG_SKU"
            row["rejected_source_url"]=row["source_url"]
            row["rejected_archive_url"]=row["archive_download_url"]
            row["source_url"]=""
            row["archive_download_url"]=""
            row["archive_release_url"]=""
            row["status"]="WRONG_MODEL"
            row["reason"]="QUARANTINED: original page contains different SKU suffix, e.g. DC5 instead of requested DC. See rejected_source_url."
        else:
            row["zip_verified"]="FAIL"
            row["reason"]="ZIP audit finding: "+rec.get("reason","")[:200]
    STAT.mkdir(parents=True,exist_ok=True)
    with (STAT/"master_status.csv").open("w",newline="",encoding="utf-8-sig") as f:
        writer=csv.DictWriter(f,fieldnames=list(final[0]))
        writer.writeheader();writer.writerows(final)
    counts=Counter(x["status"] for x in final)
    bybrand={}
    for brand in sorted({r["brand"] for r in final}):
        products=[r for r in final if r["brand"]==brand]
        bybrand[brand]={"total":len(products),
                        "complete":sum(r["status"]=="COMPLETE" for r in products),
                        "unresolved":[r["model"] for r in products if r["status"]!="COMPLETE"]}
    summary=dict(inventory_total=377,counts=dict(counts),brands=bybrand,
       fully_verified=counts["COMPLETE"]==377,
       process_terminated=sum(x["status"]!="UNPROCESSED" for x in final)==377,
       definition="COMPLETE only when exact model has source HTML, verified description/specs, and downloaded product photos",
       methodology="Original archives matched to independently validated zip files; wrong SKU captures quarantined with link preserved only as rejected source")
    (STAT/"master_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    md=["# Catalog 377 — текущий проверенный статус",
        "",f"Исходно 377 моделей. Обработано: {377-counts['UNPROCESSED']}.",
        f"С подтверждённой карточкой и изображениями (COMPLETE): {counts['COMPLETE']}.",
        f"PARTIAL: {counts['PARTIAL']}; NOT_FOUND: {counts['NOT_FOUND']}; WRONG_MODEL: {counts['WRONG_MODEL']}; ERROR: {counts['ERROR']}; необработано: {counts['UNPROCESSED']}.",
        "",
        "Каждый результат в [master_status.csv](./master_status.csv) содержит источник и ссылку на конкретный архив в GitHub Releases. Ни PARTIAL, ни NOT_FOUND, ни WRONG_MODEL, ни ERROR не являются выполненной задачей.",
        "",
        "| Бренд | Всего | COMPLETE | Неполные |",
        "|---|---:|---:|---:|"]
    for brand,d in bybrand.items():
        md.append(f"| {brand} | {d['total']} | {d['complete']} | {d['total']-d['complete']} |")
    md += ["", "## Незакрытые товары",
           "", "Полный перечень приведён в CSV. Ниже первые 100:", ""]
    notdone=[r for r in final if r["status"]!="COMPLETE"]
    for x in notdone[:100]:
        row="- "+x["brand"]+" "+x["model"]+" — "+x["status"]
        if x["source_url"]:row+=" ([источник]("+x["source_url"]+"))"
        md.append(row)
    if len(notdone)>100:md.append(f"- ...ещё {len(notdone)-100} моделей в CSV.")
    (STAT/"summary.md").write_text("\n".join(md)+"\n",encoding="utf-8")
    print("MASTER_SUMMARY",json.dumps({k:summary[k] for k in ["inventory_total","counts","fully_verified","process_terminated"]},ensure_ascii=False))

if __name__=="__main__":
    main()
