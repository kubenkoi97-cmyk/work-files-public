#!/usr/bin/env python3
"""Inspect all initial/recovery catalog 377 Releases: genuine source HTML and images.

Produces independent per-model evidence, without trusting status.csv alone.
The script reads ZIP files and images, never executes downloaded HTML or JS.
"""
import csv
import io
import json
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import tempfile
import unicodedata
import zipfile

import requests
from bs4 import BeautifulSoup
from PIL import Image

REPO="kubenkoi97-cmyk/work-files-public"
REPORT=Path("product-research/catalog-377/audit")
REPORT.mkdir(parents=True,exist_ok=True)
API="https://api.github.com/repos/"+REPO+"/releases?per_page=100"
h={"Accept":"application/vnd.github+json"}
if os.environ.get("GITHUB_TOKEN"):
    h["Authorization"]="Bearer "+os.environ["GITHUB_TOKEN"]

def normalize(x):
    return re.sub("[^A-Z0-9]","",unicodedata.normalize("NFKC",str(x)).upper())

def safe(x):
    return re.sub(r"[^A-Za-z0-9._-]","_",str(x)).strip("_")[:85]

def audit_one(z, model,brand):
    folder="products/"+brand+"_"+safe(model)+"/"
    orig=folder+"original.html"
    offline=folder+"offline.html"
    man=folder+"manifest.json"
    paths=set(z.namelist())
    row={"brand":brand,"model":model,"archive_present":"yes",
         "verified":False,"reason":"","photos":0,
         "largest_photo":0,"source":""}
    if any(n not in paths for n in [orig,offline,man]):
        row["reason"]="Missing original/offline HTML or manifest"
        return row
    try:
        m=json.loads(z.read(man))
        html=z.read(orig).decode("utf-8",errors="replace")
        offline_html=z.read(offline).decode("utf-8",errors="replace")
        soup=BeautifulSoup(html,"html.parser")
        primary=" ".join(hh.get_text(" ",strip=True) for hh in soup.find_all("h1"))
        title=soup.title.get_text(" ",strip=True) if soup.title else ""
        row["source"]=m.get("source_url","")
        if normalize(model) not in normalize(primary+" "+title):
            row["reason"]="Exact model not in product heading or title"
            return row
        if not row["source"] or "http" not in row["source"]:
            row["reason"]="No source URL"
            return row
        if not m.get("has_description") or not m.get("has_specs"):
            row["reason"]="Description/specifications incomplete"
            return row
        photos=m.get("image_files",[])
        row["photos"]=len(photos)
        if not photos:
            row["reason"]="No downloaded product photos"
            return row
        valid=0
        largest=0
        errors=[]
        for photo in photos:
            p=folder+"page_files/"+photo.get("file","")
            if p not in paths:
                errors.append("missing "+p[-80:])
                continue
            try:
                data=z.read(p)
                with Image.open(io.BytesIO(data)) as img:
                    img.load()
                    w,h=img.size
                valid+=1
                largest=max(largest,w*h)
            except Exception as ex:
                errors.append("corrupt "+p[-80:])
        row["largest_photo"]=largest
        if errors:
            row["reason"]="; ".join(errors[:3])
            return row
        if not valid or largest<200*200:
            row["reason"]="All images are tiny thumbnails"
            return row
        if normalize(model) not in normalize(offline_html):
            row["reason"]="Model absent from offline HTML"
            return row
        row["verified"]=True
        row["reason"]="OK"
    except Exception as e:
        row["reason"]="Audit exception: "+str(e)[:130]
    return row

def fetch_release(release):
    tag=release["tag_name"]
    asset=next((a for a in release.get("assets",[]) if a["name"].endswith(".zip")),None)
    if not asset:return tag,[],["No archive ZIP"]
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/asset["name"]
        try:
            with requests.get(asset["browser_download_url"],timeout=125,stream=True) as r:
                r.raise_for_status()
                with path.open("wb") as fd:
                    for chunk in r.iter_content(1024*1024):
                        if chunk:fd.write(chunk)
            if path.stat().st_size<100:
                raise ValueError("Suspiciously small archive")
            rows=[]
            with zipfile.ZipFile(path) as z:
                status_file="status.csv"
                if status_file not in z.namelist():raise ValueError("Missing status.csv")
                cr=list(csv.DictReader(io.StringIO(z.read(status_file).decode("utf-8-sig"))))
                for p in cr:
                    val= {"brand":p["brand"],"model":p["model"],
                          "declared":p.get("status",""),"release":tag,
                          "zip_url":asset["browser_download_url"]}
                    if p.get("status")=="COMPLETE":
                        val.update(audit_one(z,p["model"],p["brand"]))
                    else:
                        val.update({"verified":False,"reason":"Declared "+p.get("status",""),
                                    "photos":0,"largest_photo":0,
                                    "source":p.get("source_url","")})
                    rows.append(val)
            return tag,rows,[]
        except Exception as e:
            return tag,[],[str(e)[:180]]

def main():
    r=requests.get(API,headers=h,timeout=35)
    r.raise_for_status()
    releases=r.json()
    relevant=[x for x in releases
          if re.fullmatch(r"catalog377-(?:recovery-|deep-)?batch-\d{3}-\d{3}",x["tag_name"])]
    print("RELEASES_TO_AUDIT",len(relevant),flush=True)
    results={}
    failures={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for tag,rows,errors in pool.map(fetch_release,relevant):
            if errors:failures[tag]=errors
            else:results[tag]=rows
            print("CHECKED",tag,len(rows),"FAILED",len(errors),flush=True)
    states={}
    # Initial + recovered passes: recovery takes precedence for the same SKU
    for stage in ("catalog377-batch-", "catalog377-recovery-batch-", "catalog377-deep-batch-"):
        for tag in sorted(results):
            if not tag.startswith(stage):continue
            for row in results[tag]:
                states[(row["brand"],row["model"])]=row
    lines=sorted(states.values(),key=lambda a:(a["brand"],a["model"]))
    with (REPORT/"audit_status.csv").open("w",newline="",encoding="utf-8-sig") as f:
        columns=["brand","model","declared","verified","reason",
                 "photos","largest_photo","source","release","zip_url"]
        writer=csv.DictWriter(f,fieldnames=columns,extrasaction="ignore")
        writer.writeheader();writer.writerows(lines)
    totals=Counter("VERIFIED" if x["verified"] else ("FAIL" if x["declared"]=="COMPLETE" else x["declared"]) for x in lines)
    summary={"releases_scanned":len(relevant),"releases_downloaded":len(results),
             "release_failures":failures,"unique_models_found":len(states),
             "counts":dict(totals),
             "verified_ready":sum(x["verified"] for x in lines),
             "definition":"Original HTML, offline HTML, exact model heading, product description/specs, all local product images decodable, one image >=200x200.",
             "status":"audit_completed"}
    (REPORT/"audit_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    (REPORT/"README.md").write_text(
        "# Аудит HTML и изображений 377 товаров\n\n"
        +"Проверены фактические ZIP-архивы из GitHub Releases. "
        +"Точный результат по каждой модели: [audit_status.csv](./audit_status.csv).\n\n"
        +"Подтверждено (VERIFIED): **"+str(summary["verified_ready"])+"** / 377.\n\n"
        +"Обнаруженные ошибки: "+str(len(failures))+" пакетов. "
        +"Технический отчёт: [audit_summary.json](./audit_summary.json).\n",
        encoding="utf-8"
    )
    print("FINAL_AUDIT",json.dumps(summary,ensure_ascii=False),flush=True)
if __name__=="__main__":
    main()
