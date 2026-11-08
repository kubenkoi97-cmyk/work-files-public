#!/usr/bin/env python3
"""Independent archive integrity audit of all authoritative product source ZIPs.

Reads actual ZIP contents via authenticated gh release download. Distinguishes
archive integrity (can files be read?) from completeness of vendor's product
narrative. Never upgrades the user's original HTML status based on PDFs.
"""
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import tempfile
import time
from collections import defaultdict,Counter
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image
from zipfile import ZipFile, BadZipFile

ROOT=Path("product-research/catalog-377")
OUT=ROOT/"audit-v2"
OUT.mkdir(parents=True,exist_ok=True)

def norm(s):
    return re.sub(r"\s+","",str(s).upper())

def safe(s):
    return re.sub(r"[^A-Za-z0-9._-]","_",str(s)).strip("_")[:85]

def fetch(tag,filename,destination):
    last=""
    for attempt in range(5):
        try:
            p=subprocess.run(["gh","release","download",tag,"--repo",
                "kubenkoi97-cmyk/work-files-public","--pattern",filename,
                "--dir",str(destination),"--clobber"],
                capture_output=True,text=True,timeout=150)
            target=destination/filename
            if p.returncode==0 and target.exists() and target.stat().st_size>1000:
                return target,""
            last=(p.stderr or p.stdout)[:300]
        except Exception as e:
            last=str(e)[:300]
        time.sleep((attempt+1)*2)
    return None,last or "Download unsuccessful"

def check_one(z,entry,tag):
    brand,model=entry["brand"],entry["model"]
    result={"brand":brand,"model":model,"master_status":entry["status"],
       "release_tag":tag,"zip_integrity":"OK","file_presence":"NO",
       "exact_heading":"NO","photo_images_verified":0,
       "has_description_in_manifest":"NO","has_specs_in_manifest":"NO",
       "source_url":"","reason":""}
    prefix=f"products/{brand}_{safe(model)}/"
    names=set(z.namelist())
    manifest=prefix+"manifest.json"
    original=prefix+"original.html"
    offline=prefix+"offline.html"
    if not all(x in names for x in (manifest,original,offline)):
        result["reason"]="Missing original/offline HTML or manifest for exact SKU"
        return result
    try:
        m=json.loads(z.read(manifest))
        text=z.read(original).decode("utf-8","replace")
        off=z.read(offline).decode("utf-8","replace")
        if len(text)<3000 or len(off)<3000:
            result["reason"]="Truncated HTML"
            return result
        soup=BeautifulSoup(text,"html.parser")
        primary=" ".join(h.get_text(" ",strip=True) for h in soup.find_all("h1"))
        title=soup.title.get_text(" ",strip=True) if soup.title else ""
        result["exact_heading"]="YES" if norm(model) in norm(primary+" "+title) else "NO"
        result["file_presence"]="YES"
        result["has_description_in_manifest"]="YES" if m.get("has_description") else "NO"
        result["has_specs_in_manifest"]="YES" if m.get("has_specs") else "NO"
        result["source_url"]=m.get("source_url","")
        if m.get("model")!=model or m.get("brand")!=brand:
            result["reason"]="Incorrect model or brand in manifest"
            return result
        if result["exact_heading"]!="YES":
            result["reason"]="SKU not in product heading"
            return result
        images=m.get("image_files",[])
        if not images:
            result["reason"]="No product photo file references"
            return result
        valid=0
        for img in images:
            if "loading.svg" in (img.get("url","").lower()):
                continue
            path=prefix+"page_files/"+img.get("file","")
            if path not in names:
                result["reason"]="Missing product image referenced in manifest"
                return result
            data=z.read(path)
            try:
                with Image.open(io.BytesIO(data)) as im:
                    im.verify()
                    if im.width>=150 and im.height>=150:
                        valid+=1
            except Exception:
                result["reason"]="Unreadable image file"
                return result
        result["photo_images_verified"]=valid
        result["reason"]="OK" if valid else "No decodable product image at useful resolution"
    except Exception as e:
        result["reason"]="Validation exception: "+str(e)[:160]
    return result

def main():
    shard=int(os.environ.get("AUDIT_SHARD","0"))
    nshards=int(os.environ.get("AUDIT_SHARDS","6"))
    assert 0<=shard<nshards
    with (ROOT/"status/master_status.csv").open(encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==377
    groups=defaultdict(list)
    missing=[]
    for row in rows:
        if row["status"]=="NOT_FOUND":
            continue
        url=row.get("archive_download_url","")
        m=re.search(r"/releases/download/([^/]+)/([^/]+\.zip)(?:\?|$)",url)
        if not m:
            missing.append((row["brand"],row["model"],"No release ZIP URL"))
            continue
        tag,name=m.groups()
        h=int(hashlib.sha256(tag.encode()).hexdigest()[:8],16)
        if h%nshards==shard:
            groups[(tag,name)].append(row)
    records=[]
    for n,((tag,name),models) in enumerate(sorted(groups.items()),start=1):
        print("RELEASE",shard,n,"of",len(groups),tag,"MODELS",len(models),flush=True)
        with tempfile.TemporaryDirectory() as temp:
            path,error=fetch(tag,name,Path(temp))
            if error:
                for model in models:
                    records.append({"brand":model["brand"],"model":model["model"],
                      "master_status":model["status"],"release_tag":tag,
                      "zip_integrity":"DOWNLOAD_ERROR","file_presence":"UNKNOWN",
                      "exact_heading":"UNKNOWN","photo_images_verified":0,
                      "has_description_in_manifest":"UNKNOWN","has_specs_in_manifest":"UNKNOWN",
                      "source_url":"","reason":error})
                continue
            try:
                with ZipFile(path) as z:
                    corrupt=z.testzip()
                    if corrupt:
                        for model in models:
                            records.append({"brand":model["brand"],"model":model["model"],
                                "master_status":model["status"],"release_tag":tag,
                                "zip_integrity":"CORRUPT","file_presence":"UNKNOWN",
                                "exact_heading":"UNKNOWN","photo_images_verified":0,
                                "has_description_in_manifest":"UNKNOWN","has_specs_in_manifest":"UNKNOWN",
                                "source_url":"","reason":"Corrupt ZIP member "+corrupt[:140]})
                    else:
                        records.extend(check_one(z,row,tag) for row in models)
            except (OSError,BadZipFile) as e:
                for row in models:
                    records.append({"brand":row["brand"],"model":row["model"],
                        "master_status":row["status"],"release_tag":tag,
                        "zip_integrity":"CORRUPT","file_presence":"UNKNOWN",
                        "exact_heading":"UNKNOWN","photo_images_verified":0,
                        "has_description_in_manifest":"UNKNOWN","has_specs_in_manifest":"UNKNOWN",
                        "source_url":"","reason":str(e)[:220]})
        print("CHECKED_MODELS",len(records),flush=True)
    p=OUT/f"integrity-shard-{shard}.csv"
    fields=["brand","model","master_status","release_tag","zip_integrity",
       "file_presence","exact_heading","photo_images_verified",
       "has_description_in_manifest","has_specs_in_manifest","source_url","reason"]
    with p.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fields);writer.writeheader();writer.writerows(records)
    counters=Counter("VERIFIED" if r["reason"]=="OK" else r["zip_integrity"] if r["zip_integrity"]!="OK" else "INVALID_CONTENT" for r in records)
    report=dict(shard=shard,nshards=nshards,models_checked=len(records),
        release_groups=len(groups),counts=dict(counters),
        no_source_records=missing,
        integrity_rule="ZIP opens and CRC passes, exact model heading and manifest, original+offline HTML, at least one decodable local product image",
        disclaimer="ZIP integrity and photos do not prove vendor published a product description; consult manifest and text-specific checks.")
    (OUT/f"summary-shard-{shard}.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print("SHARD_RESULT",json.dumps({k:report[k] for k in ("shard","models_checked","release_groups","counts")}),flush=True)
if __name__=="__main__":
    main()
