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
    for prefix in ("batch-","recovery-batch-","deep-batch-","supplemental-batch-","supplemental-v2-batch-"):
        for p in sorted(STAT.glob(prefix+"*.csv")):
            tag=p.stem[len(prefix):]
            with p.open(encoding="utf-8-sig",newline="") as f:
                for row in csv.DictReader(f):
                    if not row.get("model"):continue
                    r=dict(row)
                    root="https://github.com/kubenkoi97-cmyk/work-files-public/releases/"
                    release=("catalog377-"+prefix)+tag
                    r["archive_release_url"]=root+"tag/"+release
                    r["archive_download_url"]=root+"download/"+release+"/catalog377-"+tag+".zip"
                    r["result_stage"]=prefix.rstrip("-")
                    k=(r["brand"],r["model"])
                    old=states.get(k)
                    # Never replace a verified complete source with a failed
                    # later attempt; preserve MirCli/source priority.
                    if old and old.get("status")=="COMPLETE" and prefix!="supplemental-v2-batch-":
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
       methodology="First pass statuses overridden by documented fallback recovery; source artifacts linked per model")
    (STAT/"master_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    md=["# Catalog 377 — текущий проверенный статус",
        "",f"Исходно 377 моделей. Обработано: {377-counts['UNPROCESSED']}.",
        f"С подтверждённой карточкой и изображениями (COMPLETE): {counts['COMPLETE']}.",
        f"PARTIAL: {counts['PARTIAL']}; NOT_FOUND: {counts['NOT_FOUND']}; ERROR: {counts['ERROR']}; необработано: {counts['UNPROCESSED']}.",
        "",
        "Каждый результат в [master_status.csv](./master_status.csv) содержит источник и ссылку на конкретный архив в GitHub Releases. Ни PARTIAL, ни NOT_FOUND, ни ERROR не являются выполненной задачей.",
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
