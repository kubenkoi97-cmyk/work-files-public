#!/usr/bin/env python3
"""Deep IGC historical exact-(DC) HTML hunt. Preserve source bytes, never conflate DC/DC5/DC7.
This is a research/capture stage; master status remains unchanged until independent review.
"""
import argparse, csv, json, re, hashlib, time, io, zipfile, base64, html, os
from pathlib import Path
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse,urljoin, urlencode, quote
import requests
from bs4 import BeautifulSoup

ROOT=Path("product-research/catalog-377")
DEST=ROOT/"igc-deep-2026-11-09"
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","Accept-Language":"ru-RU,ru;q=0.9,en;q=0.5"}
def norm(s):return re.sub(r"[^A-Z0-9]","",str(s).upper())
def skus(s):return re.findall(r"IMS[-\s]?[A-Z0-9-]+(?:\s*\([A-Z0-9]+\))?",str(s).upper())
def sku_exact(model,title):
    # Full suffix must be physically present; do not treat unsuffixed base as exact.
    m=re.sub(r"\s+","",model.upper())
    text=str(title).upper()
    pat=re.escape(m).replace(r"\(",r"\s*\(")
    return bool(re.search(r"(?<![A-Z0-9])"+pat+r"(?![A-Z0-9(])",text))
def clean(s):return re.sub(r"[^A-Za-z0-9._-]","_",str(s)).strip("_")[:90]
def variant_class(model,title):
    t=str(title).upper();m=model.upper().replace(" ","")
    if sku_exact(model,t): return "EXACT_DC_H1"
    base=m.split("(")[0]
    if not re.search(r"(?<![A-Z0-9])"+re.escape(base)+r"(?![A-Z0-9])",t):
        return "DIFFERENT_MODEL_OR_INDEX"
    if re.search(re.escape(base)+r"\s*[\(-]?\s*DC[457]",t):return "WRONG_DC4_DC5_DC7"
    if re.search(re.escape(base)+r"\s*[\(-]?\s*[45]\s*\)?",t):return "WRONG_GENERATION"
    return "UNSUFFIXED_UNCONFIRMED"
def download(url):
    try:
        r=requests.get(url,headers=UA,timeout=12,allow_redirects=True)
        ct=r.headers.get("content-type","").lower()
        meta={"url":url,"final_url":r.url,"http":r.status_code,"bytes":len(r.content),"content_type":ct}
        if r.status_code!=200 or ("html" not in ct and "text" not in ct) or len(r.content)<1000:
            return meta,None
        if len(r.content)>5_000_000:meta["error"]="too large";return meta,None
        if r.encoding in (None,"ISO-8859-1"):r.encoding=r.apparent_encoding or "utf-8"
        return meta,r
    except Exception as e:
        return {"url":url,"error":str(e)[:170]},None

CATEGORIES=[
"http://igc-aircon.com/product/nastennye_bloki_vrf/",
"http://igc-aircon.com/product/kanalnye_bloki_vrf/",
"http://igc-aircon.com/product/napolno_potolochnye_bloki_vrf/",
"http://igc-aircon.com/product/pritochnye_bloki_vrf/",
"http://igc-aircon.com/product/ventilyatsionnye_ustanovki_vrf/",
"https://igc.com.ru/catalog/vnutrennie_bloki_vrf_sistemy/",
"https://igc.com.ru/catalog/arkhiv_modeley/",
]
def catalogue_links():
    links={}
    results=[]
    def task(u):
        meta,r=download(u)
        match=[]
        if r:
            soup=BeautifulSoup(r.text,"html.parser")
            for el in soup.select("a[href], [onclick]"):
                label=el.get_text(" ",strip=True)
                target=el.get("href","")
                event=el.get("onclick","")
                mo=re.search(r"""(?:location(?:\.href)?\s*=\s*)['"]([^'"]+)['"]""",event)
                if mo:target=mo.group(1)
                if not target:continue
                if "IMS-" not in (label+" "+target).upper(): continue
                full=urljoin(r.url,target)
                if full.startswith("http") and urlparse(full).hostname not in ("web.archive.org",):
                    match.append((label[:200],full))
        return meta,match
    with ThreadPoolExecutor(max_workers=6) as pool:
        for meta,found in pool.map(task,CATEGORIES):
            results.append(dict(meta,links_found=len(found)))
            for label,u in found:
                links.setdefault(u,label)
    return links,results

def find_indexed(model):
    # Normal organic results only; don't treat a snippet as original HTML.
    queries=[f'"{model}" IGC',f'"{model.split("(")[0]}" "DC" кондиционер IGC']
    urls=[]
    for q in queries:
        index="https://www.bing.com/search?format=rss&"+urlencode({"q":q})
        meta,r=download(index)
        if not r:continue
        soup=BeautifulSoup(r.text,"xml")
        for it in soup.find_all("item"):
            link=it.find("link").get_text(" ",strip=True) if it.find("link") else ""
            summary=" ".join(z.get_text(" ",strip=True) for z in [it.find("title"),it.find("description")] if z)
            if norm(model.split("(")[0]) in norm(summary+" "+link) and link.startswith(("http://","https://")):
                if urlparse(link).hostname not in ("bing.com","google.com","youtube.com"):
                    urls.append(link)
    return list(dict.fromkeys(urls))[:12]

def candidates(model,from_cat):
    m=model.replace(" ","")
    bare=m.split("(")[0]
    tail=bare.lower().replace("-","_")
    exact_slug=bare+"(DC)"
    guessed=[
        "https://mircli.ru/IGC-"+bare+"/",
        "https://mircli.ru/IGC-"+bare+"-DC-/",
        "https://mircli.ru/IGC-"+bare+"DC/",
        "https://mircli.ru/IGC-"+bare+"-DC/",
        "https://igc.com.ru/catalog/vnutrennie_bloki_vrf_sistemy/igc_"+tail+"/",
        "https://igc.com.ru/catalog/arkhiv_modeley/igc_"+tail+"/",
        "http://igc-aircon.com/product/"+tail+"_dc/",
        "https://www.effect-nn.ru/search/?q="+quote(bare),
        "https://climatehnik.com/search/?q="+quote(bare),
    ]
    c=[(u,"DIRECT_GUESS") for u in guessed]
    for u,label in from_cat.items():
        if norm(bare) in norm(label+" "+urlparse(u).path):
            c.insert(0,(u,"PUBLISHED_CATALOGUE_LINK"))
    for u in find_indexed(model): c.insert(0,(u,"INDEXED_SEARCH_RESULT"))
    return list(dict.fromkeys(c))[:25]

def inspect(meta,r,model):
    out=dict(meta,model=model)
    if not r:return out
    soup=BeautifulSoup(r.text,"html.parser")
    h1=[x.get_text(" ",strip=True) for x in soup.find_all("h1")]
    title=soup.title.get_text(" ",strip=True) if soup.title else ""
    primary=" ".join(h1+[title])
    out.update(title=title[:220],h1=h1[:4],classification=variant_class(model,primary),
               exact_h1=any(sku_exact(model,x) for x in h1),has_h1=bool(h1))
    if any(z in primary.lower() for z in ("поиск по","результаты поиска","страница не найдена","404 not found","access denied","captcha")):
        out["classification"]="SEARCH_OR_ERROR"
    # Require an actual product detail page with one main heading and brand.
    out["product_page"]=bool(len(h1)==1 and "IGC" in primary.upper() and
            out["classification"] in ("EXACT_DC_H1","UNSUFFIXED_UNCONFIRMED","WRONG_DC4_DC5_DC7"))
    if out["product_page"]:
        txt=soup.get_text(" ",strip=True)
        out["description_markers"]=[x for x in ("Особенности и преимущества","Описание","О товаре","Характеристики","Технические характеристики") if x.lower() in txt.lower()]
        out["image_tags"]=len(soup.find_all("img"))
        out["raw_html_sha256"]=hashlib.sha256(r.content).hexdigest()
        out["model_in_text"]=norm(model) in norm(txt)
        out["source_encoding"]=r.encoding
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--shard",type=int,required=True)
    p.add_argument("--shards",type=int,default=3)
    args=p.parse_args()
    assert 0<=args.shard<args.shards
    allrows=list(csv.DictReader((ROOT/"status"/"master_status.csv").open(encoding="utf-8-sig",newline="")))
    target=[x for x in allrows if x["brand"]=="IGC" and x["status"] in ("WRONG_MODEL","NOT_FOUND")]
    assert len(target)==22
    # Contiguous groups to report family-level outcomes.
    target=sorted(target,key=lambda x:(x["model"].split("-")[1].split("2")[0],int(x["excel_row"])))
    selected=[row for i,row in enumerate(target) if i%args.shards==args.shard]
    group=DEST/("shard-"+str(args.shard))
    group.mkdir(parents=True,exist_ok=True)
    pub,catdiag=catalogue_links()
    (group/"catalogue_http.json").write_text(json.dumps(catdiag,ensure_ascii=False,indent=2),encoding="utf-8")
    results=[]; summary=[]
    for row in selected:
        model=row["model"]
        cand=candidates(model,pub)
        print("START",model,"candidates",len(cand),flush=True)
        entries=[]
        def job(pair):
            u,method=pair
            meta,r=download(u)
            item=inspect(meta,r,model)
            item["discovered_by"]=method
            return item,r
        with ThreadPoolExecutor(max_workers=9) as pool:
            futures=[pool.submit(job,pair) for pair in cand]
            for f in as_completed(futures):
                entry,r=f.result()
                if r and entry.get("product_page"):
                    # Byte-for-byte research copies; EXACT originals archived separately from unconfirmed aliases.
                    grade=entry["classification"]
                    if grade in ("EXACT_DC_H1","UNSUFFIXED_UNCONFIRMED"):
                        d=group/("exact_html" if grade=="EXACT_DC_H1" else "alias_reference_html")
                        d.mkdir(exist_ok=True)
                        name=clean(model)+"__"+hashlib.sha256(entry["final_url"].encode()).hexdigest()[:12]+".html"
                        (d/name).write_bytes(r.content)
                        entry["local_original"]=str((d/name).relative_to(group))
                entries.append(entry)
        entries.sort(key=lambda x:(x.get("classification")!="EXACT_DC_H1",x.get("classification")!="UNSUFFIXED_UNCONFIRMED",x.get("url","")))
        results.extend(entries)
        summary.append({"model":model,"prior_status":row["status"],"checked_urls":len(entries),
            "full_exact_html":[x.get("final_url") for x in entries if x.get("product_page") and x.get("exact_h1") and x.get("classification")=="EXACT_DC_H1"],
            "unverified_unsuffixed":[x.get("final_url") for x in entries if x.get("classification")=="UNSUFFIXED_UNCONFIRMED" and x.get("product_page")],
            "wrong_variant":[x.get("final_url") for x in entries if x.get("classification")=="WRONG_DC4_DC5_DC7" and x.get("product_page")],
            "other_results":dict(Counter(x.get("classification") or "NOT_ACCESSIBLE" for x in entries))})
        print("RESULT",model,json.dumps({"exact":len(summary[-1]["full_exact_html"]),"alias":len(summary[-1]["unverified_unsuffixed"]),"wrong":len(summary[-1]["wrong_variant"])},ensure_ascii=False),flush=True)
        (group/"progress.json").write_text(json.dumps({"models":summary,"requests":results},ensure_ascii=False,indent=2),encoding="utf-8")
    payload={"date_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
         "shard":args.shard,"target_total":22,"models_tested":len(selected),
         "exact_model_html_candidates":sum(bool(y["full_exact_html"]) for y in summary),
         "models_with_unsuffixed_html_reference":sum(bool(y["unverified_unsuffixed"]) for y in summary),
         "models":summary,
         "quality_gate":"Exact (DC) in individual H1; unsuffixed, DC4, DC5, DC7 and series pages cannot replace requested SKU."}
    (group/"results.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
    with (group/"requests.csv").open("w",encoding="utf-8-sig",newline="") as f:
        fields=["model","url","final_url","http","bytes","classification","product_page","exact_h1","discovered_by","h1","title","local_original","error"]
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader()
        for x in results:
            y=dict(x);y["h1"]=" | ".join(x.get("h1",[]))
            w.writerow(y)
    print("SHARD_COMPLETE",json.dumps(payload,ensure_ascii=False)[:2000],flush=True)
if __name__=="__main__":main()
