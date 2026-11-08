#!/usr/bin/env python3
"""Save verifiable original manufacturer supporting documents for unresolved exact SKUs.

These files are supplementary evidence and MUST NEVER be called original product HTML.
Per SKU links preserve existing archived original product HTML where available.
"""
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import time
import zipfile
import requests
import fitz
from collections import Counter

ROOT=Path("product-research/catalog-377")
STATUS=ROOT/"status/master_status.csv"
OUT=ROOT/"supporting-evidence"
OUT.mkdir(exist_ok=True,parents=True)

SOURCES=[
    {
       "name":"Kentatsu_DX_PRO_VII_catalog_2025.pdf",
       "url":"https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf",
       "brand":"Kentatsu",
       "note":"Kentatsu DX PRO VII catalogue: KTKB/KTTB/KTHB series model tables and series descriptions; downloaded PDF only, not HTML"
    },
    {
       "name":"IGC_VRF_technical_characteristics.pdf",
       "url":"http://igc-aircon.com/upload/iblock/8e1/f2umkqwfiqx3p6b65iz03odbvjqw01vo.pdf",
       "brand":"IGC",
       "note":"IGC manufacturer VRF technical characteristics, old DC versions; no model-by-model product HTML"
    },
    {
       "name":"Midea_MIH_GHN18_original_manual.pdf",
       "url":"https://air-midea.com/upload/iblock/5fa/w3uwwedt34zlvayeyypdf82w8bqe3b4d.pdf",
       "brand":"Midea",
       "model":"MIH90GHN18",
       "note":"Midea manufacturer manual for MIH90GHN18 WITHOUT DP"
    },
    {
       "name":"Midea_MIH_GHN18_DP_original_manual.pdf",
       "url":"https://daichi.ru/upload/iblock/e3f/1r0uk23yt3xq50hbmhmd4ctbrsbow353/IOM_Wall-mounted_MIH_GHN18%28DP%29_11_07_25.pdf",
       "brand":"Midea",
       "model":"MIH90GHN18(DP)",
       "note":"Midea manufacturer manual for MIH90GHN18(DP), different variant from the model without suffix"
    },
]
def norm(s):
    return re.sub("[^A-Z0-9]","",str(s).upper())

def download(url):
    for attempt in range(3):
        try:
            r=requests.get(url,headers={"User-Agent":"Mozilla/5.0"},timeout=40)
            r.raise_for_status()
            if not r.content.startswith(b"%PDF-"):
                raise ValueError("Source was not a PDF")
            if not 10000 <= len(r.content) <= 45000000:
                raise ValueError("PDF unexpected size")
            return r.content,r.url
        except (requests.RequestException,ValueError) as e:
            if attempt==2:raise
            time.sleep(attempt+1)

def pdf_text(raw):
    try:
        doc=fitz.open(stream=raw,filetype="pdf")
        return "\n".join(page.get_text() for page in doc),len(doc)
    except Exception:
        return "",None

with STATUS.open(encoding="utf-8-sig",newline="") as f:
    models=[r for r in csv.DictReader(f) if r["status"]!="COMPLETE"]
assert len(models)==52, len(models)
source_entries=[]
for source in SOURCES:
    name=source["name"]
    try:
        raw,final_url=download(source["url"])
        (OUT/name).write_bytes(raw)
        content,pages=pdf_text(raw)
        source_entries.append({
            **source,"downloaded":True,"actual_url":final_url,"bytes":len(raw),
            "pages":pages,"sha256":hashlib.sha256(raw).hexdigest(),
            "normalized_pdf_text":norm(content)
        })
        print("SAVED",name,len(raw),"PAGES",pages,flush=True)
    except Exception as e:
        source_entries.append({**source,"downloaded":False,"error":str(e)[:300]})
        print("SOURCE_ERROR",name,str(e)[:200],flush=True)

mapped=[]
for sku in models:
    matches=[]
    for evidence in source_entries:
        if not evidence["downloaded"] or evidence["brand"]!=sku["brand"]:continue
        target=evidence.get("model")
        if target and target!=sku["model"]:continue
        found=norm(sku["model"]) in evidence["normalized_pdf_text"]
        matches.append({
            "pdf":evidence["name"],
            "exact_sku_in_pdf_text":found,
            "source":evidence.get("actual_url",evidence["url"]),
            "note":evidence["note"]
        })
    mapped.append({
        "brand":sku["brand"],"model":sku["model"],
        "original_html_status":sku["status"],
        "existing_archived_html":sku["archive_download_url"] if sku["status"]=="PARTIAL" else "",
        "existing_html_source":sku["source_url"],
        "supporting_sources":matches,
        "important":"Manufacturer original PDF is an independent extra source. It is NOT original store HTML. Never call this COMPLETE based on PDF."
    })
(OUT/"source_map.json").write_text(json.dumps(mapped,ensure_ascii=False,indent=2),encoding="utf-8")
with (OUT/"sku_source_map.csv").open("w",newline="",encoding="utf-8-sig") as f:
    fields=["brand","model","html_status","existing_html_archive","existing_html_source","pdf_sources","exact_sku_confirmed_in_pdf"]
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for r in mapped:
        w.writerow({
          "brand":r["brand"],"model":r["model"],
          "html_status":r["original_html_status"],
          "existing_html_archive":r["existing_archived_html"],
          "existing_html_source":r["existing_html_source"],
          "pdf_sources":"; ".join(x["pdf"] for x in r["supporting_sources"] if x["exact_sku_in_pdf_text"]),
          "exact_sku_confirmed_in_pdf":any(x["exact_sku_in_pdf_text"] for x in r["supporting_sources"])
        })

summary={
 "unresolved_exact_skus":len(models),
 "original_html_complete_from_this_support_pack":0,
 "source_pdfs": [{k:v for k,v in x.items() if k!="normalized_pdf_text"} for x in source_entries],
 "models_with_exact_sku_in_original_pdf":sum(any(s["exact_sku_in_pdf_text"] for s in r["supporting_sources"]) for r in mapped),
 "photos":"Original product photographs remain in linked earlier per-SKU HTML ZIPs for PARTIAL; PDFs are supporting evidence only."
}
(OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
zpath=ROOT/"output/catalog377-unresolved-original-manufacturer-sources.zip"
zpath.parent.mkdir(exist_ok=True,parents=True)
with zipfile.ZipFile(zpath,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
    for p in OUT.iterdir():
        if p.is_file():z.write(p,p.name)
print("EVIDENCE_ARCHIVE",zpath,zpath.stat().st_size,json.dumps({"pdfs":sum(x["downloaded"] for x in source_entries),"with_exact_sku":summary["models_with_exact_sku_in_original_pdf"]}),flush=True)
