#!/usr/bin/env python3
"""Probe exact original product HTML of two Midea MIH90 variants, preserving provenance.
No artificial descriptions; no status promotions in this diagnostic stage.
"""
from pathlib import Path
import requests, re, json, csv, time
from bs4 import BeautifulSoup
from urllib.parse import urlparse

ROOT=Path("product-research/catalog-377/midea-final-2026-11-09")
ROOT.mkdir(parents=True,exist_ok=True)
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/132.0.0.0 Safari/537.36","Accept-Language":"ru-RU,ru;q=0.9,en;q=0.6"}
TARGETS={
"MIH90GHN18":[
"https://midea-pro.ru/catalog/vnutrennie-bloki-vrf-sistemy/midea-mih90ghn18/",
"https://iclim.ru/catalog/promyshlennye_konditsionery/multizonalnye_sistemy/vnutrennie_bloki/midea_mih90ghn18/",
"https://vsekondicioneri.ru/product/midea-mih90ghn18/",
"https://gorodskie-sistemy.ru/polupromyshlennoe-oborudovanie/vrf-sistemy-kondicionirovaniya/vnutrennij-blok-vrv/vnutrennij-blok-vrf-sistemy-midea-mih90ghn18",
"https://midea.kg/product-categories/vrf-sistemy/vnutrennie-bloki/nastennyy-blok-v8"],
"MIH90GHN18(DP)":[
"https://midea-pro.ru/catalog/vnutrennie-bloki-vrf-sistemy/midea-mih90ghn18-dp/",
"https://iclim.ru/catalog/promyshlennye_konditsionery/multizonalnye_sistemy/vnutrennie_bloki/midea_mih90ghn18_dp/",
"https://vsekondicioneri.ru/product/midea-mih90ghn18-dp/",
"https://ryazan.vsekondicioneri.ru/product/midea-mih90ghn18-dp/",
"https://coolsochi.ru/product/midea-mih90ghn18-dp/",
"https://www.klimat-master.ru/serie/mih-gdp-v8/"]
}
def token(s):return re.sub(r"[^A-Z0-9]","",str(s).upper())
def title_match(model,h1):
    s=str(h1).upper()
    t=re.sub(r"\\s+","",str(model).upper())
    # Reject the DP sibling for the unmodified version.
    regex=r"(?<![A-Z0-9])"+re.escape(t)+r"(?![A-Z0-9(])"
    return bool(re.search(regex,s))
session=requests.Session();session.headers.update(UA)
rows=[]
for model,urls in TARGETS.items():
 for url in urls:
    rec={"model":model,"requested_url":url,"date_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())}
    print("TRY",model,url,flush=True)
    try:
        r=session.get(url,timeout=18,allow_redirects=True)
        rec.update(http=r.status_code,final_url=r.url,bytes=len(r.content),content_type=r.headers.get("content-type",""))
        if r.status_code!=200 or "html" not in r.headers.get("content-type","").lower() or len(r.content)<2000:
            rec["finding"]="HTTP_UNAVAILABLE_OR_NOT_HTML"
        else:
            r.encoding=r.apparent_encoding or "utf-8"
            soup=BeautifulSoup(r.text,"html.parser")
            h1=" | ".join(x.get_text(" ",strip=True) for x in soup.select("h1"))
            title=soup.title.get_text(" ",strip=True) if soup.title else ""
            rec.update(h1=h1[:250],title=title[:250],exact_sku_h1=title_match(model,h1),canonical_model_in_body=token(model) in token(soup.get_text(" ",strip=True)))
            # Restrict seller copy to actual product description sections, exclude generic shipping, warranty and montage sections.
            sections=[]
            for tag in soup.select('[id*="descr" i], [class*="descr" i], [itemprop="description"], [id*="detail" i], [class*="detail" i]'):
                text=tag.get_text(" ",strip=True)
                if 110<=len(text)<=4500 and text not in sections:
                    sections.append(text[:2000])
                if len(sections)>=6:break
            h2=[x.get_text(" ",strip=True) for x in soup.select("h2,h3")][:30]
            rec["section_candidates"]=sections[:5]
            rec["product_headings"]=h2
            rec["section_candidate_count"]=len(sections)
            rec["img_nodes"]=len(soup.select("img"))
            imgs=[]
            for im in soup.select("img"):
                alt=im.get("alt","")
                if token(model) in token(alt):
                    imgs.append({"src":(im.get("src") or im.get("data-src") or "")[:250],"alt":alt[:120]})
            rec["exact_model_image_elements"]=imgs[:8]
            rec["finding"]="EXACT_H1" if rec["exact_sku_h1"] else "NO_EXACT_H1"
            # Do not upload site source bytes as HTML unless we can establish it is an exact individual SKU.
            if rec["exact_sku_h1"]:
                name="MIH90GHN18_DP" if model.endswith("(DP)") else "MIH90GHN18"
                host=(urlparse(r.url).hostname or "site").replace(".","_")
                dst=ROOT/(name+"_"+host+".html")
                dst.write_bytes(r.content)
                rec["original_saved_path"]=str(dst)
    except requests.RequestException as exc:
        rec.update(finding="NETWORK_OR_ACCESS_ERROR",error=str(exc)[:220])
    rows.append(rec)
    print("EVIDENCE",json.dumps({k:rec.get(k) for k in ("model","http","bytes","h1","finding","section_candidate_count","img_nodes")},ensure_ascii=False),flush=True)
jsonpath=ROOT/"candidate_probe.json"
jsonpath.write_text(json.dumps({"date_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"targets":TARGETS,"results":rows},ensure_ascii=False,indent=2),encoding="utf-8")
with (ROOT/"candidate_probe.csv").open("w",encoding="utf-8-sig",newline="") as f:
    cols=["model","requested_url","http","final_url","bytes","h1","exact_sku_h1","section_candidate_count","img_nodes","finding","original_saved_path","error"]
    w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(rows)
print("PROBE_FINISHED",json.dumps({"attempted":len(rows),"exact_h1":sum(bool(x.get("exact_sku_h1")) for x in rows),"paths":[x.get("original_saved_path") for x in rows if x.get("original_saved_path")]},ensure_ascii=False),flush=True)
