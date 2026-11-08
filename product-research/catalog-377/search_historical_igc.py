#!/usr/bin/env python3
"""Targeted search of historical indexed *exact* IGC product URLs.

The search only identifies candidates. It NEVER claims a complete product HTML
or changes catalog status until original HTML and images are downloaded.
Uses Common Crawl public index and Wayback CDX. No proxy/anti-bot evasion.
"""
import csv, json, re, time
from pathlib import Path
from urllib.parse import urlparse
import requests
ROOT=Path("product-research/catalog-377")
OUT=ROOT/"history-diagnostics";OUT.mkdir(parents=True,exist_ok=True)
with (ROOT/"status/master_status.csv").open(encoding="utf-8-sig",newline="") as f:
    pending=[x for x in csv.DictReader(f) if x["brand"]=="IGC" and x["status"]!="COMPLETE"]
assert len(pending)==22,len(pending)
session=requests.Session()
session.headers.update({"User-Agent":"Catalog377-research/1.0 (public archival source verification)"})
evidence=[]
def probe(url):
    try:
        r=session.get(url,timeout=17)
        if r.status_code in (403,429):
            return {"status":r.status_code,"blocked":True,"body":r.text[:140]}
        if r.status_code!=200:
            return {"status":r.status_code,"body":r.text[:140]}
        ct=r.headers.get("content-type","")
        lines=r.text.splitlines()
        if "application/json" in ct:
            try:
                data=r.json()
                if isinstance(data,list):
                    return {"status":200,"content_type":ct,"json":data[:30],"len":len(r.content)}
                if isinstance(data,dict):
                    return {"status":200,"content_type":ct,"json":data,"len":len(r.content)}
            except ValueError:pass
        return {"status":200,"content_type":ct,"lines":lines[:25],"len":len(r.content)}
    except Exception as e:return {"error":str(e)[:200]}
# Find active index endpoints rather than inventing index names.
cc=probe("https://index.commoncrawl.org/collinfo.json")
indexes=[]
if cc.get("status")==200:
    try:
        data=cc.get("json") or json.loads("\n".join(cc["lines"]))
        indexes=[x["cdx-api"] for x in data if "cdx-api" in x][:3]
    except Exception:pass
print("INDEXES",indexes,"CC",str(cc)[:250],flush=True)
# Select models from three historical series with strict DC suffix.
samples=["IMS-K22NH(DC)","IMS-BS36NHQ(DC)","IMS-BH220NH(DC)","IMS-QV100NH(DC)"]
for model in samples:
    stem=re.sub("[^a-z0-9]","",model.lower().replace("(dc)",""))
    # Wayback service is currently returning 503/timeouts from this runner.
    # Avoid repeated blocked calls; Common Crawl is an independent index.
    for index in indexes[:2]:
        from urllib.parse import urlencode
        candidate=index+"?"+urlencode({"url":"*.igc-aircon.com/*"+stem+"*","output":"json","filter":"status:200"})
        r=probe(candidate)
        evidence.append({"model":model,"source":"CommonCrawl","index":index,"result":r})
        print("COMMONCRAWL",model,str(r)[:340],flush=True)
        time.sleep(.6)
(OUT/"historical_igc_index_probe.json").write_text(json.dumps({
    "sampled_models":samples,"total_unresolved_igc":len(pending),
    "public_indexes":indexes,"findings":evidence,
    "caveat":"Index record is NOT original HTML; requires exact-SKU verification and capture of underlying page."},
    ensure_ascii=False,indent=2),encoding="utf-8")
