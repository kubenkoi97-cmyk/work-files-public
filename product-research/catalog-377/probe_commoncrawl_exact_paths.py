#!/usr/bin/env python3
"""Search 3 independent Common Crawl index snapshots for original product URL paths.

Candidate URL alone is NEVER accepted as source HTML. For a hit we must later
fetch original WARC and verify H1, exact suffix, genuine description and photos.
"""
import csv,json,os,re,time,urllib.parse
from pathlib import Path
from collections import Counter
import requests
ROOT=Path("product-research/catalog-377")
DEST=ROOT/"history-diagnostics";DEST.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((ROOT/"status/master_status.csv").open(encoding="utf-8-sig",newline="")))
models=[x["model"] for x in rows if x["brand"]=="IGC" and x["status"]!="COMPLETE"]
assert len(models)==22
sess=requests.Session()
sess.headers.update({"User-Agent":"Mozilla/5.0 Catalog377 original-SKU-page provenance check"})
records=[]
indexes=[
 "https://index.commoncrawl.org/CC-MAIN-2026-43-index",
 "https://index.commoncrawl.org/CC-MAIN-2026-39-index",
 "https://index.commoncrawl.org/CC-MAIN-2025-47-index",
 "https://index.commoncrawl.org/CC-MAIN-2024-51-index",
]
# Wildcard query only within URL path. Filter for /product/ server-side to reduce bandwidth.
patterns=[
 "igc-aircon.com/product/*",
 "www.igc-aircon.com/product/*",
 "igc.com.ru/catalog/vnutrennie_bloki_vrf_sistemy/*",
 "iclim.ru/catalog/promyshlennye_konditsionery/multizonalnye_sistemy/vnutrennie_bloki/*",
]
def key(s):
    return re.sub("[^A-Z0-9]","",str(s).upper())
def rootkey(model):
    return key(model).replace("DC","")
for index in indexes:
    for pattern in patterns:
        query=index+"?"+urllib.parse.urlencode({"url":pattern,"output":"json","filter":"status:200","collapse":"urlkey","pageSize":300})
        try:
            r=sess.get(query,timeout=45)
            print("INDEX_QUERY",index.rsplit("/",1)[-1],pattern,r.status_code,len(r.content),repr(r.text[:130]),flush=True)
            if r.status_code!=200:
                records.append(dict(index=index,pattern=pattern,scan_status="HTTP_"+str(r.status_code)))
                continue
            matches=[]
            raw=r.text.splitlines()
            parsed=[]
            for line in raw[:12000]:
                try:
                    x=json.loads(line)
                    if isinstance(x,dict) and "url" in x: parsed.append(x)
                except (TypeError,ValueError):
                    continue
            for x in parsed:
                url=x.get("url","")
                compact=key(urllib.parse.unquote(url))
                for model in models:
                    if rootkey(model) in compact:
                        matches.append({"model":model,"url":url,"timestamp":x.get("timestamp"),"index":index,
                           "filename":x.get("filename"),"offset":x.get("offset"),"length":x.get("length"),
                           "status":"URL_CANDIDATE_NOT_HTML_VERIFIED"})
            records.extend(matches)
            print("RESULT",pattern,"parsed",len(parsed),"candidate_hits",len(matches),flush=True)
        except Exception as e:
            records.append({"index":index,"pattern":pattern,"scan_status":"ERROR","reason":str(e)[:210]})
            print("INDEX_ERROR",pattern,str(e)[:190],flush=True)
        time.sleep(.4)
# Disambiguate same model URL, but retain timestamp+index for provenance.
candidates=[r for r in records if r.get("model")]
seen=set()
deduped=[]
for r in candidates:
    k=(r["model"],r["url"],r.get("index"))
    if k not in seen:
        seen.add(k);deduped.append(r)
report={
 "unresolved_models":models,
 "candidate_count":len(deduped),
 "model_counts":dict(Counter(r["model"] for r in deduped)),
 "candidates":deduped,
 "index_failures":[r for r in records if r.get("scan_status")],
 "not_a_capture":"Common Crawl index URLs do not prove exact product page. No status upgrade without fetching original HTML and photo files.",
}
(DEST/"commoncrawl_candidates_22.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print("RESULT_SUMMARY",json.dumps({"candidate_count":len(deduped),"model_counts":report["model_counts"],"failed_queries":len(report["index_failures"])},ensure_ascii=False),flush=True)
