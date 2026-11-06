#!/usr/bin/env python3
"""Package original public MirCli server HTML with locally downloaded assets.

The raw server HTML stays byte-for-byte unchanged. A second copy with only
asset URL rewrites is created for 'Webpage, Complete'-style offline viewing.
This is not an authored/reconstructed product page.
"""
import concurrent.futures
import hashlib
import json
import mimetypes
import re
import urllib.parse
import zipfile
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://mircli.ru/Kentatsu-KRA80HFAN1-KPU95-RA/"
BASE = Path("product-research/Kentatsu/KRA80HFAN1/original")
RAW = BASE / "KRA80HFAN1_MirCli_server_original.html"
NAME = "KRA80HFAN1_MirCli_complete"
HTML = BASE / (NAME + ".html")
ASSETS = BASE / (NAME + "_files")
ZIP = BASE / (NAME + ".zip")
MANIFEST = BASE / "KRA80HFAN1_MirCli_complete_manifest.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
           "Accept-Language":"ru-RU,ru;q=0.9"}

def norm(url, base=URL):
    if not url or url.startswith(("data:", "blob:", "javascript:", "#", "mailto:", "tel:")):
        return None
    url = urllib.parse.urljoin(base, url)
    p=urllib.parse.urlparse(url)
    if p.scheme not in ("http","https") or p.hostname not in ("mircli.ru", "cdn2.mircli.ru", "s3.mircli.ru"):
        return None
    if "/api/" in p.path or "/payment/" in p.path:
        return None
    return url

def fname(url, content_type):
    p=urllib.parse.urlsplit(url).path
    name=re.sub(r"[^A-Za-z0-9._-]","_",Path(p).name)[:70] or "resource"
    if "." not in name:
        name += mimetypes.guess_extension(content_type) or ".bin"
    return hashlib.sha256(url.encode()).hexdigest()[:12]+"_"+name

def fetch(url):
    try:
        r=requests.get(url,headers=HEADERS,timeout=26)
        r.raise_for_status()
        ctype=r.headers.get("content-type","").split(";")[0].strip()
        if ctype.startswith("text/html") or len(r.content)>15_000_000:
            return url,None,"html/oversize"
        name=fname(url,ctype)
        (ASSETS/name).write_bytes(r.content)
        return url,name,None
    except Exception as e:
        return url,None,str(e)[:110]

def get_srcset(s):
    return [v.strip().split()[0] for v in s.split(",") if v.strip()]

def iter_css_urls(s):
    return [x[1] for x in re.findall(r"url\(\s*(['\"]?)(.*?)\1\s*\)",s,flags=re.I)]

def main():
    if not RAW.exists(): raise RuntimeError("Raw original HTML file missing")
    raw=RAW.read_text(encoding="utf-8")
    if "KRA80HFAN1" not in raw or not raw.lstrip().lower().startswith("<!doctype html"):
        raise RuntimeError("Not the authentic KRA80 original source file")
    ASSETS.mkdir(parents=True,exist_ok=True)
    soup=BeautifulSoup(raw,"html.parser")
    source_urls=set()
    for tag in soup.find_all(["img","source","video","audio","link","script"]):
        attrs=["src","poster","data-src","data-original"]
        if tag.name=="link":
            rel=tag.get("rel",[])
            kind=tag.get("as","")
            if "stylesheet" in rel or "preload" in rel or kind in ("image","font","style","script"):
                attrs.append("href")
        for a in attrs:
            if tag.has_attr(a):
                u=norm(tag.get(a))
                if u: source_urls.add(u)
        for a in ("srcset","imagesrcset","data-srcset"):
            if tag.has_attr(a):
                for src in get_srcset(tag.get(a,"")):
                    u=norm(src)
                    if u: source_urls.add(u)
        if tag.has_attr("style"):
            for src in iter_css_urls(tag.get("style","")):
                u=norm(src)
                if u: source_urls.add(u)
    for st in soup.find_all("style"):
        for src in iter_css_urls(st.get_text()):
            u=norm(src)
            if u: source_urls.add(u)
    source_urls=sorted(source_urls)[:450]
    downloaded={}
    failures={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as ex:
        for url,name,error in ex.map(fetch,source_urls):
            if name: downloaded[url]=name
            else: failures[url]=error
    print("DOM RESOURCES",len(source_urls),"DOWNLOADED",len(downloaded),"FAILED",len(failures),flush=True)

    # Download CSS dependencies (fonts, background images). CSS is already inside
    # the _files folder, so its dependencies refer to basenames only.
    css_additions=[]
    for url,name in list(downloaded.items()):
        if not name.lower().endswith(".css"):
            continue
        path=ASSETS/name
        content=path.read_text(encoding="utf-8",errors="replace")
        for src in iter_css_urls(content):
            full=norm(src,base=url)
            if full and full not in downloaded and full not in failures:
                css_additions.append(full)
    css_additions=sorted(set(css_additions))[:300]
    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as ex:
        for url,name,error in ex.map(fetch,css_additions):
            if name: downloaded[url]=name
            else: failures[url]=error
    for url,name in list(downloaded.items()):
        if not name.lower().endswith(".css"): continue
        path=ASSETS/name
        content=path.read_text(encoding="utf-8",errors="replace")
        def repl_css(match):
            quoted, val=match.group(1),match.group(2)
            full=norm(val,base=url)
            return "url("+quoted+downloaded[full]+quoted+")" if full in downloaded else match.group(0)
        content=re.sub(r"url\(\s*(['\"]?)(.*?)\1\s*\)",repl_css,content)
        path.write_text(content,encoding="utf-8")

    # HTML only has asset URLs changed. Keep every title, model datum and text.
    for tag in soup.find_all(["img","source","video","audio","link","script"]):
        for attr in ("src","poster","data-src","data-original","href"):
            if not tag.has_attr(attr): continue
            u=norm(tag.get(attr))
            if u in downloaded:
                tag[attr]=ASSETS.name+"/"+downloaded[u]
        for attr in ("srcset","imagesrcset","data-srcset"):
            if not tag.has_attr(attr): continue
            chunks=[]
            for chunk in tag[attr].split(","):
                bits=chunk.strip().split()
                if bits:
                    u=norm(bits[0])
                    if u in downloaded: bits[0]=ASSETS.name+"/"+downloaded[u]
                chunks.append(" ".join(bits))
            tag[attr]=", ".join(chunks)
    HTML.write_text("<!DOCTYPE html>\n"+str(soup),encoding="utf-8")
    info={"source_url":URL,"model":"KRA80HFAN1",
          "raw_html_bytes":RAW.stat().st_size,
          "complete_html_bytes":HTML.stat().st_size,
          "downloaded_asset_count":len(downloaded),
          "asset_failures_count":len(failures),
          "asset_failures":failures,
          "provenance":"Authentic MirCli server HTML; complete copy only changes local asset paths. Not a reconstruction.",
          "limitations":"Original server response is not hydrated browser DOM. Some dynamic functions may need internet; failed assets retain original links."}
    MANIFEST.write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding="utf-8")
    with zipfile.ZipFile(ZIP,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        z.write(RAW,RAW.name);z.write(HTML,HTML.name);z.write(MANIFEST,MANIFEST.name)
        for f in ASSETS.iterdir():
            if f.is_file(): z.write(f,ASSETS.name+"/"+f.name)
    print("FINISH",json.dumps({"archive":str(ZIP),"archive_bytes":ZIP.stat().st_size,
                               "original_html_bytes":RAW.stat().st_size,
                               "complete_html_bytes":HTML.stat().st_size,
                               "downloaded_assets":len(downloaded),
                               "failures":len(failures)},ensure_ascii=False),flush=True)

if __name__=="__main__":
    main()
