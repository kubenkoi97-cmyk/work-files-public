#!/usr/bin/env python3
"""Evidence-preserving product page capture. Exact model only; MirCli first.

Source: user-provided Excel, 377 unique (brand, article) keys.
Outputs: per-model authentic server HTML, readable offline HTML, locally
downloaded page resources, manifest; batch archive + per-row status CSV.
"COMPLETE" is reserved for a verified exact-model page with product gallery,
description AND characteristics. Similar-model or series-level data is never
substituted.
"""
import argparse
import base64
import csv
import gzip
import hashlib
import html as htmlmod
import io
import json
import logging
import mimetypes
import os
from pathlib import Path
import re
import sys
import time
import unicodedata
from urllib.parse import urljoin, urlparse, quote, urlencode, parse_qs
from urllib.robotparser import RobotFileParser
import zipfile
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

ROOT = Path("product-research/catalog-377")
INVENTORY = ROOT / "source-inventory.tsv.gz.b64"
OUT = ROOT / "output"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.6",
}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)
IGC_OFFICIAL_LINKS = None  # populated once per batch to avoid repeated catalogue crawls
EFFECT_CATALOG_LINKS = None

def key(s):
    return re.sub(r"[^A-Z0-9]", "", unicodedata.normalize("NFKC", str(s)).upper())

def safe(s):
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(s)).strip("_")[:85]

def get(url, timeout=15):
    try:
        r=SESSION.get(url,timeout=timeout,allow_redirects=True)
        if r.status_code != 200 or len(r.content)<500:
            return None
        # Older Russian vendor pages declare "ANSI", which is not a valid
        # Python encoding. Requests then incorrectly substitutes UTF-8 and
        # loses all Russian descriptions/specifications.
        declared=(r.encoding or "").strip().lower()
        if declared in ("ansi","iso-8859-1","latin-1","latin1",""):
            r.encoding=r.apparent_encoding or "windows-1251"
        return r
    except requests.RequestException:
        return None

def parse_source(url, brand, model, response):
    if not response:
        return None
    ctype=response.headers.get("content-type", "").lower()
    if "html" not in ctype and "text" not in ctype:
        return None
    text=response.text
    if len(text)<5000 or key(model) not in key(text):
        return None
    soup=BeautifulSoup(text, "html.parser")
    title=soup.title.get_text(" ",strip=True) if soup.title else ""
    heads=[h.get_text(" ",strip=True) for h in soup.find_all(["h1"])]
    # Exact model must be present in primary product heading or title.
    # Require brand too. A listing whose title only says 'search results'
    # does not count as a verified product page.
    primary=" ".join(heads+[title])
    if key(model) not in key(primary) or key(brand) not in key(primary):
        return None
    bad=["поиск по сайту", "результаты поиска", "не найдено", "страница не найдена",
         "404 not found", "access denied", "service unavailable"]
    if any(v in title.lower() for v in bad):
        return None
    # A single product card is different from category search results
    if not heads or len(heads)>6:
        return None
    page_text=soup.get_text(" ",strip=True)
    gallery=product_images(soup, model, brand, response.url)
    descr_score=sum(t in page_text.lower() for t in [
        "о товаре","описание","особенности","предназначен","характеристики"])
    spec_score=sum(t in page_text.lower() for t in [
        "характеристики","охлаждение", "обогрев", "мощность", "вес", "габарит"])
    return {
        "url": response.url, "title":title,"heads":heads,
        "text":text,"raw_bytes":response.content,"source_encoding":response.encoding,"soup":soup,"photos":gallery,
        "has_description": descr_score>=2 or ("описание" in page_text.lower()),
        "has_specs": spec_score>=2,
        "ctype":ctype,"brand":brand,"model":model
    }

def product_images(soup, model, brand, base_url):
    # Only product gallery, not generic page images or related products.
    out=[]
    tag_entries=[]
    for img in soup.find_all("img"):
        alt=img.get("alt","")
        raw=" ".join([alt,img.get("title","")])
        candidates=[]
        for attr in ("src","data-src","data-original","data-lazy-src"):
            if img.get(attr): candidates.append(img[attr])
        for attr in ("srcset","data-srcset"):
            for seg in img.get(attr,"").split(","):
                if seg.strip(): candidates.append(seg.strip().split()[0])
        for c in candidates:
            u=urljoin(base_url,htmlmod.unescape(c))
            path=urlparse(u).path
            if key(model) in key(raw) or key(model) in key(path):
                tag_entries.append((u,alt))
    # Verified exact product on climatehnik.com: its main gallery uses
    # <img alt=""> wrapped in class="thumb"; filenames are opaque hashes.
    # These must not be confused with similar-product and logo images.
    if (urlparse(base_url).hostname or "").endswith("climatehnik.com"):
        for img in soup.find_all("img"):
            parent=img.parent
            cls=(parent.get("class",[]) if parent else [])
            if "thumb" not in cls: continue
            for attr in ("src","data-src","data-original"):
                raw=img.get(attr)
                if not raw: continue
                u=urljoin(base_url,htmlmod.unescape(raw))
                if "/resize_cache/iblock/" not in urlparse(u).path: continue
                # Prefer large gallery frame; keep thumbnail if that is all
                # the source has, but do not count duplicates twice.
                if "/140_140_1/" in u: continue
                tag_entries.append((u,"Exact-model product gallery (climatehnik)"))
    # If the site uses JSON-LD, collect only exact product image URLs.
    for tag in soup.find_all("script",type="application/ld+json"):
        try: obj=json.loads(tag.get_text())
        except: continue
        collection=obj if isinstance(obj,list) else [obj]
        for p in collection:
            if not isinstance(p,dict): continue
            graph=p.get("@graph",[])
            collection2=(graph if isinstance(graph,list) else [])+[p]
            for node in collection2:
                if not isinstance(node,dict): continue
                if "Product" not in str(node.get("@type","")): continue
                if key(model) not in key(node.get("name","")): continue
                for im in node.get("image",[]) if isinstance(node.get("image"),list) else [node.get("image")]:
                    if isinstance(im,str):tag_entries.append((urljoin(base_url,im),"Product JSON-LD"))
    # Product-specific photos can have generic CDN filenames; if alt says exact
    # SKU include those. Sort high-res variants before thumbnails.
    seen=set()
    for u,alt in tag_entries:
        pr=urlparse(u)
        if pr.scheme not in ("http","https") or "/static/" in pr.path:
            continue
        if u in seen: continue
        seen.add(u)
        out.append({"url":u,"alt":alt})
    return out[:50]

def slug_candidates(brand, model):
    variants=[]
    # MirCli substitutes each parenthesis with hyphen, and spaces with hyphens.
    base=re.sub(r"[^A-Za-z0-9_-]", "-", model).replace(" ", "-")
    for s in [base,base.rstrip("-"),base.replace("--","-"),model.replace(" ","-")]:
        if s not in variants:variants.append(s)
    out=[]
    for s in variants:
        safeurl=quote(s,safe="-_")
        out += ["https://mircli.ru/"+brand+"-"+safeurl+"/"]
        if brand=="Kentatsu" and model.startswith(("KRA","KZA","KKA","KLA")):
            out += ["https://mircli.ru/"+brand+"-"+safeurl+"-KPU95-RA/"]
    return list(dict.fromkeys(out))[:10]

def search_mircli(model):
    query="https://mircli.ru/search/?keyword="+quote(model)
    r=get(query,timeout=15)
    if not r:return []
    soup=BeautifulSoup(r.text,"html.parser")
    links=[]
    for a in soup.find_all("a",href=True):
        h=a.get("href","")
        label=a.get_text(" ",strip=True)
        if key(model) in key(label) or key(model) in key(h):
            u=urljoin(r.url,h)
            if urlparse(u).netloc.endswith("mircli.ru") and "/search/" not in u:
                links.append(u)
    return list(dict.fromkeys(links))[:15]

def external_candidates(brand, model):
    global EFFECT_CATALOG_LINKS
    # Public listing of exact SKU product pages at effect-nn.ru. Pages hold
    # genuine model-specific detail links, not aliases guessed from a series.
    extra=[]
    if brand=="Kentatsu":
        if EFFECT_CATALOG_LINKS is None:
            EFFECT_CATALOG_LINKS=[]
            for page_num in range(9,28):
                page_url=f"https://www.effect-nn.ru/cond_category_244_page-{page_num}.htm"
                rr=get(page_url,timeout=10)
                if not rr:continue
                ss=BeautifulSoup(rr.text,"html.parser")
                for a in ss.find_all("a",href=True):
                    dest=urljoin(page_url,a["href"])
                    if re.search(r"/condition_[0-9]+\.htm$",dest):
                        EFFECT_CATALOG_LINKS.append((a.get_text(" ",strip=True),dest))
        for name,dest in EFFECT_CATALOG_LINKS:
            if key(model) in key(name):
                extra.append(dest)
    # Query actual vendor sites plus Bing's well-formed RSS results. HTML
    # search engines may hide organic links; do not mistake that for no SKU.
    q=f'"{model}" "{brand}" купить характеристики'
    candidates=list(dict.fromkeys(extra))
    vendor_searches=[
       "https://climatehnik.com/search/?"+urlencode({"q":model}),
       "https://envok.ru/search/?"+urlencode({"q":model}),
       "https://daichi.market/search/index.php?"+urlencode({"q":model}),
    ]
    for u in vendor_searches:
        r=get(u,timeout=12)
        if not r:continue
        soup=BeautifulSoup(r.text,"html.parser")
        for a in soup.find_all("a",href=True):
            link=a.get("href","")
            label=a.get_text(" ",strip=True)
            if key(model) in key(link+" "+label):
                dest=urljoin(r.url,link)
                path=urlparse(dest).path.lower()
                if "/search/" not in path and dest not in candidates:
                    candidates.append(dest)
    # The brand+model can often be indexed even if a shop's internal search
    # has no URL in the anchor text. Bing RSS item links are actual URLs.
    urls=[
      "https://www.bing.com/search?format=rss&"+urlencode({"q":q}),
      "https://www.bing.com/search?format=rss&"+urlencode({"q":f'"{model}"'}),
      "https://www.google.com/search?"+urlencode({"q":q,"num":"10"}),
    ]
    for search_url in urls:
        r=get(search_url,timeout=13)
        if not r:continue
        if "bing.com" in search_url:
            feed=BeautifulSoup(r.text,"xml")
            for item in feed.find_all("item"):
                u=item.find("link").get_text(" ",strip=True) if item.find("link") else ""
                title=item.find("title").get_text(" ",strip=True) if item.find("title") else ""
                description=item.find("description").get_text(" ",strip=True) if item.find("description") else ""
                if key(model) in key(title+" "+u+" "+description):
                    candidates.append(u)
            continue
        soup=BeautifulSoup(r.text,"html.parser")
        for a in soup.find_all("a",href=True):
            href=a.get("href","")
            if href.startswith("/url?"):
                href=parse_qs(urlparse(href).query).get("q",[""])[0]
            u=urljoin(r.url,href)
            pr=urlparse(u)
            if pr.scheme not in ("http","https"): continue
            host=pr.hostname or ""
            if host.endswith(("google.com","bing.com","yandex.ru","duckduckgo.com","youtube.com","wikipedia.org")): continue
            if key(model) in key(u+" "+a.get_text(" ",strip=True)):
                candidates.append(u)
    # Structural guesses are *candidates only*, never proof of a matching model.
    if brand=="Kentatsu":
        candidates.extend([
            f"https://climatehnik.com/search/?q={quote(model)}",
            f"https://msk.climate-group.ru/vnutrenniy-blok-vrf-sistemy-kentatsu-{model.lower()}/",
            f"https://nizhniy-novgorod.vsekondicioneri.ru/product/kentatsu-{model.lower()}/",
            f"https://brand-climat.ru/kentatsu-{model.lower()}",
        ])
    if brand=="IGC":
        global IGC_OFFICIAL_LINKS
        if IGC_OFFICIAL_LINKS is None:
            IGC_OFFICIAL_LINKS=[]
            listing="https://igc.com.ru/catalog/vnutrennie_bloki_vrf_sistemy/"
            for page in range(1,8):
                url=listing+("?PAGEN_1="+str(page) if page>1 else "")
                r=get(url,timeout=13)
                if not r:continue
                soup=BeautifulSoup(r.text,"html.parser")
                for a in soup.find_all("a",href=True):
                    href=a.get("href","")
                    link=urljoin(url,href)
                    if link.startswith("https://igc.com.ru/catalog/"):
                        IGC_OFFICIAL_LINKS.append((a.get_text(" ",strip=True),link))
            for base in ("https://igc-aircon.com/product/nastennye_bloki_vrf/",
                         "https://igc-aircon.com/product/kanalnye_bloki_vrf/",
                         "https://igc-aircon.com/product/kassetnye_vrf_4_kh_potochnye_komplekty/"):
                rr=get(base,timeout=13)
                if not rr:continue
                soup=BeautifulSoup(rr.text,"html.parser")
                for a in soup.find_all("a",href=True):
                    IGC_OFFICIAL_LINKS.append((a.get_text(" ",strip=True),urljoin(base,a["href"])))
        for title,link in IGC_OFFICIAL_LINKS:
            if key(model) in key(title+" "+link):
                candidates.append(link)
        slug=model.lower().replace("-","_").replace("(","_").replace(")","").replace(" ","_")
        candidates.append("https://igc.com.ru/catalog/vnutrennie_bloki_vrf_sistemy/igc_"+slug+"/")
    if brand=="Midea":
        candidates.extend([
            f"https://coolsochi.ru/product/midea-{model.lower().replace('(', '-').replace(')', '')}/",
            f"https://vsekondicioneri.ru/product/midea-{model.lower().replace('(', '-').replace(')', '')}/",
            f"https://nizhniy-novgorod.vsekondicioneri.ru/product/midea-{model.lower().replace('(', '-').replace(')', '')}/",
        ])
    cleaned=[]
    for u in candidates:
        pr=urlparse(u)
        if pr.scheme not in ("http","https") or not pr.netloc: continue
        if u not in cleaned:cleaned.append(u)
    return cleaned[:28]

def choose_source(brand, model):
    attempts=[]
    for u in slug_candidates(brand,model):
        p=parse_source(u,brand,model,get(u),)
        attempts.append(u)
        if p:return p,attempts,"MirCli"
    for u in search_mircli(model):
        if u in attempts:continue
        p=parse_source(u,brand,model,get(u))
        attempts.append(u)
        if p:return p,attempts,"MirCli"
    for u in external_candidates(brand,model):
        if u in attempts:continue
        p=parse_source(u,brand,model,get(u))
        attempts.append(u)
        if p:return p,attempts,"External"
    return None,attempts,""

def choose_download_urls(page):
    soup=page["soup"]
    base=page["url"]
    photo_urls=[p["url"] for p in page["photos"]]
    asset_urls={}
    for u in photo_urls:
        asset_urls[u]={"type":"product_photo"}
    for tag in soup.find_all(["img","source","link","script","video"]):
        attrs=[]
        if tag.name=="link":
            if ("stylesheet" in tag.get("rel",[]) or
                "preload" in tag.get("rel",[]) and tag.get("as") in ("image","style","font","script")):
                attrs=["href"]
        elif tag.name in ("img","source","video"):
            attrs=["src","poster","data-src","data-original"]
        elif tag.name=="script":
            attrs=["src"]
        for attr in attrs:
            if not tag.get(attr):continue
            u=urljoin(base,htmlmod.unescape(tag[attr]))
            pr=urlparse(u)
            if pr.scheme not in ("http","https"):continue
            # Public first-party assets only; don't archive analytics/tracking.
            if pr.hostname not in ("mircli.ru","cdn2.mircli.ru","s3.mircli.ru") and \
               pr.hostname != urlparse(base).hostname:
                continue
            if any(x in pr.path.lower() for x in ["/api/","/payment/","/pusher/","/tracking/"]):
                continue
            if u not in asset_urls:asset_urls[u]={"type":"page_asset"}
    return dict(list(asset_urls.items())[:120])

def download_assets(page,folder):
    folder.mkdir(parents=True,exist_ok=True)
    chosen=choose_download_urls(page)
    assets={}
    failed=[]
    downloaded_photos=[]
    def one(item):
        url,meta=item
        try:
            r=requests.get(url,headers=HEADERS,timeout=14)
            if r.status_code!=200 or not r.content or len(r.content)>12_000_000:
                raise ValueError("HTTP "+str(r.status_code)+" or asset size limit")
            content_type=r.headers.get("content-type","").split(";")[0].strip()
            if content_type.startswith("text/html"):raise ValueError("received HTML, not asset")
            ext=mimetypes.guess_extension(content_type) or ""
            basename=safe(Path(urlparse(url).path).name)[:75] or "resource"
            if "." not in basename and ext:basename+=ext
            file=hashlib.sha256(url.encode()).hexdigest()[:12]+"_"+basename
            (folder/file).write_bytes(r.content)
            return url,meta,{"file":file,"bytes":len(r.content),
                       "content_type":content_type,"role":meta["type"]},None
        except Exception as e:
            return url,meta,None,str(e)[:140]
    with ThreadPoolExecutor(max_workers=12) as pool:
        for url,meta,res,error in pool.map(one,chosen.items()):
            if res:
                assets[url]=res
                if meta["type"]=="product_photo" and res["content_type"].startswith("image/"):
                    downloaded_photos.append({
                        "file":res["file"],"url":url,"bytes":res["bytes"],
                        "content_type":res["content_type"]})
            else:
                failed.append({"url":url,"error":error})
    return assets,downloaded_photos,failed

def offline_html(page,asset_map,foldername):
    soup=BeautifulSoup(page["text"],"html.parser")
    base=page["url"]
    for tag in soup.find_all(["img","source","video","link","script"]):
        for attr in ("src","href","poster","data-src","data-original"):
            raw=tag.get(attr)
            if not raw:continue
            u=urljoin(base,htmlmod.unescape(raw))
            if u in asset_map:
                tag[attr]=foldername+"/"+asset_map[u]["file"]
    return "<!DOCTYPE html>\n"+str(soup)

def capture(row, dirpath):
    model,brand,excelrow=row["model"],row["brand"],row["row"]
    product_dir=dirpath/f"{brand}_{safe(model)}"
    product_dir.mkdir(parents=True,exist_ok=True)
    manifest={"excel_row":excelrow,"brand":brand,"model":model,
              "capture_date_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
              "source_priority":["mircli.ru","public exact-model other sites"],
              "model_match_required":True}
    try:
        page,attempts,site=choose_source(brand,model)
        manifest["attempted_urls"]=attempts
        if not page:
            manifest.update(status="NOT_FOUND",reason="No verified exact model product HTML")
        else:
            original=page["text"]
            # Keep the true raw bytes for any legacy non-UTF-8 product site.
            enc=(page.get("source_encoding") or "").lower()
            if enc not in ("utf-8","utf8","ascii","us-ascii"):
                (product_dir/"source-original-charset.html").write_bytes(page["raw_bytes"])
                original=re.sub(r'(?i)(<meta[^>]*charset\s*=\s*["\']?)(?:ansi|windows-1251|cp1251)',
                                lambda m:m.group(1)+"utf-8",original)
                if not re.search(r'(?i)<meta[^>]+charset',original):
                    original=re.sub(r'(?i)<head([^>]*)>',r'<head\1><meta charset="utf-8">',original,count=1)
            # The decoded document remains original page markup, not an
            # authored model card; only charset marker is normalized.
            page["text"]=original
            (product_dir/"original.html").write_text(original,encoding="utf-8")
            asset_map,downloaded_photos,failures=download_assets(page,product_dir/"page_files")
            (product_dir/"offline.html").write_text(
                offline_html(page,asset_map,"page_files"),encoding="utf-8")
            has_desc=page["has_description"]
            has_specs=page["has_specs"]
            complete=(has_desc and has_specs and len(downloaded_photos)>=1
                      and len(downloaded_photos)==len(page["photos"]))
            status="COMPLETE" if complete else "PARTIAL"
            manifest.update(
              status=status,site=site,source_url=page["url"],title=page["title"],
              h1=page["heads"][:3],has_description=has_desc,
              has_specs=has_specs,photo_links_found=len(page["photos"]),
              downloaded_product_photos=len(downloaded_photos),
              downloaded_page_assets=len(asset_map),image_files=downloaded_photos,
              asset_failures=failures,
              original_html_size=len(original.encode("utf-8")),
              note="Authentic source HTML; offline.html differs only in local resource links."
            )
            if not complete:
                manifest["reason"]="Exact page found, but description/specs/images not all confirmed"
    except Exception as e:
        manifest.update(status="ERROR",error=str(e)[:250])
    (product_dir/"manifest.json").write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    return manifest

def inventory():
    raw=gzip.decompress(base64.b64decode(INVENTORY.read_text().strip())).decode("utf-8")
    source=list(csv.DictReader(io.StringIO(raw),delimiter="\t"))
    assert len(source)==377, len(source)
    assert len({(r["brand"],r["model"]) for r in source})==377
    assert hashlib.sha256(raw.encode()).hexdigest()=="00ce0e59ca2e3a67074285a21d84c538172b12a6c990c2caef1ddaa6afa3808b"
    return source

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--start",type=int,default=0)
    ap.add_argument("--end",type=int,default=5)
    ap.add_argument("--quick",action="store_true")
    ap.add_argument("--only-unresolved",action="store_true",
                    help="Retry only models without prior COMPLETE status in initial batches")
    args=ap.parse_args()
    products=inventory()
    assert 0<=args.start<args.end<=len(products)
    tag=f"{args.start+1:03d}-{args.end:03d}"
    batch=OUT / (("recovery-" if args.only_unresolved else "batch-")+tag)
    batch.mkdir(parents=True,exist_ok=True)
    chosen=products[args.start:args.end]
    if args.only_unresolved:
        existing=ROOT / "status" / ("batch-"+tag+".csv")
        if existing.exists():
            previous=list(csv.DictReader(existing.open(encoding="utf-8-sig",newline="")))
            completed={(r["brand"],r["model"]) for r in previous
                       if r.get("status")=="COMPLETE"}
            chosen=[r for r in chosen if (r["brand"],r["model"]) not in completed]
            print("RECOVERY_MODE",tag,"previous_complete",len(completed),
                  "recapturing",len(chosen),flush=True)
    records=[]
    for record in chosen:
        index=int(record["row"])-1
        print(f"BEGIN {index}/377 [{record['brand']}] {record['model']}",flush=True)
        result=capture(record,batch/"products")
        print("RESULT",index,record["model"],result["status"],
              result.get("source_url",""),result.get("downloaded_product_photos",0),flush=True)
        records.append(result)
        (batch/"progress.json").write_text(
            json.dumps({"batch":tag,"processed":len(records),"total_in_batch":len(chosen),
                        "results":records},ensure_ascii=False,indent=2),encoding="utf-8")
    columns=["excel_row","brand","model","status","site","source_url","has_description",
             "has_specs","photo_links_found","downloaded_product_photos",
             "downloaded_page_assets","reason"]
    with (batch/"status.csv").open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=columns,extrasaction="ignore")
        writer.writeheader();writer.writerows(records)
    counters={state:sum(r["status"]==state for r in records)
              for state in ("COMPLETE","PARTIAL","NOT_FOUND","ERROR") }
    report={"source":"User uploaded Товары для наполнения Илья.xlsx",
            "inventory_total":len(products),
            "range_indices":[args.start+1,args.end],"recovery":args.only_unresolved,
            "batch":tag,"counts":counters,
            "products":[{"brand":x["brand"],"model":x["model"],
                         "status":x["status"],"url":x.get("source_url",""),
                         "photos":x.get("downloaded_product_photos",0)}
                        for x in records],
            "status_rule":"COMPLETE only with exact-model HTML, description, specs, and local product images",
            "limitations":"Server response may differ from post-JavaScript browser DOM. Product rights remain with site owners."}
    (batch/"summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    zpath=OUT/("catalog377-"+tag+".zip")
    with zipfile.ZipFile(zpath,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in batch.rglob("*"):
            if p.is_file():z.write(p,p.relative_to(batch))
    csv_target=OUT/("catalog377-"+tag+"-status.csv")
    csv_target.write_bytes((batch/"status.csv").read_bytes())
    print("BATCH_RESULT",json.dumps({"zip":str(zpath),"zip_size":zpath.stat().st_size,
          "status_csv":str(csv_target),"counts":counters},ensure_ascii=False),flush=True)
    return 0

if __name__=="__main__":
    sys.exit(main())
