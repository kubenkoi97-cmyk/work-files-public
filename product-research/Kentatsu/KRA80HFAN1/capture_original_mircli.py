#!/usr/bin/env python3
"""Capture a genuine browser DOM snapshot of a PUBLIC MirCli product page.

Not a reconstructed product sheet. Outputs the Chromium DOM HTML, downloaded
page requisites, and a self-contained Chromium MHTML archive where available.
"""
import concurrent.futures
import hashlib
import json
import mimetypes
import re
import shutil
import sys
import time
import urllib.parse
import zipfile
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = "https://mircli.ru/Kentatsu-KRA80HFAN1-KPU95-RA/"
MODEL = "KRA80HFAN1"
ROOT = Path("product-research/Kentatsu/KRA80HFAN1/original")
BASENAME = "KRA80HFAN1_MirCli_original"
HTML = ROOT / (BASENAME + ".html")
MHTML = ROOT / (BASENAME + ".mhtml")
ASSETS = ROOT / (BASENAME + "_files")
ARCHIVE = ROOT / (BASENAME + "_complete.zip")
MANIFEST = ROOT / "capture_manifest.json"

def normalized_url(url):
    if not url or url.startswith(("data:", "blob:", "javascript:", "#", "mailto:", "tel:")):
        return None
    candidate = urllib.parse.urljoin(URL, url)
    parts = urllib.parse.urlparse(candidate)
    if parts.scheme not in ("http", "https"):
        return None
    if parts.netloc.endswith(("mircli.ru", "cdn2.mircli.ru", "s3.mircli.ru")):
        return candidate
    return None

def asset_name(url, response):
    path = urllib.parse.urlsplit(url).path
    base = Path(path).name or "resource"
    base = re.sub(r"[^A-Za-z0-9._-]", "_", base)[:65]
    media = response.headers.get("content-type", "").split(";")[0].strip()
    if "." not in base:
        base += mimetypes.guess_extension(media) or ".bin"
    return hashlib.sha256(url.encode()).hexdigest()[:12] + "_" + base

def fetch_asset(pair):
    url, _ = pair
    try:
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=18)
        r.raise_for_status()
        if len(r.content) > 15_000_000:
            return url, None, "oversize"
        name = asset_name(url, r)
        path = ASSETS / name
        path.write_bytes(r.content)
        return url, name, None
    except Exception as e:
        return url, None, str(e)[:120]

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width":1440,"height":1000}, locale="ru-RU",
                                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
        response = page.goto(URL, wait_until="domcontentloaded", timeout=75000)
        print("NAVIGATION", response.status if response else None, page.url)
        page.wait_for_timeout(5000)
        # Lazy-load product images by scrolling through the main page
        for y in range(0, 4500, 700):
            page.evaluate("(y) => window.scrollTo(0,y)", y)
            page.wait_for_timeout(120)
        page.evaluate("window.scrollTo(0,0)")
        # The product details may initially be collapsed; leave the actual DOM
        # untouched rather than injecting a synthetic description.
        html = page.content()
        browser_ok = MODEL in html and "Kentatsu" in html and (not response or response.status < 400)
        if not browser_ok:
            print("BROWSER_BLOCKED; testing plain HTTPS original source.")
            with requests.Session() as session:
                session.headers.update({
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.7",
                    "Referer": "https://mircli.ru/"})
                rr = session.get(URL, timeout=35)
            print("RAW_HTTPS_STATUS", rr.status_code, "BYTES", len(rr.content), "CTYPE", rr.headers.get("Content-Type"))
            if rr.status_code != 200 or MODEL not in rr.text or "Kentatsu" not in rr.text:
                raise RuntimeError("No original HTML available: browser and direct HTTPS access blocked")
            html = rr.text
            print("SOURCE_TYPE", "original server response, not browser hydrated DOM")
        HTML.write_text(html if html.lstrip().lower().startswith("<!doctype") else "<!DOCTYPE html>\n" + html, encoding="utf-8")
        print("HTML BYTES", HTML.stat().st_size)
        if browser_ok:
            try:
                devtools = page.context.new_cdp_session(page)
                snap = devtools.send("Page.captureSnapshot", {"format": "mhtml"})
                MHTML.write_text(snap["data"], encoding="utf-8")
                print("MHTML BYTES", MHTML.stat().st_size)
            except Exception as e:
                print("MHTML failed", str(e)[:300])
        browser.close()

    soup = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")
    assets = {}
    for tag in soup.find_all(["img","source","video","audio","script","link"]):
        for attr in ["src", "poster"]:
            if tag.has_attr(attr):
                u = normalized_url(tag[attr])
                if u: assets[u] = True
        if tag.name == "link" and tag.has_attr("href"):
            rel = tag.get("rel", [])
            as_type = tag.get("as", "")
            if "stylesheet" in rel or "preload" in rel or as_type in ("image","font","style"):
                u = normalized_url(tag["href"])
                if u: assets[u] = True
        for attr in ["srcset", "imagesrcset"]:
            if tag.has_attr(attr):
                for part in tag[attr].split(","):
                    u = normalized_url(part.strip().split()[0])
                    if u: assets[u] = True
    for tag in soup.find_all(style=True):
        for partial in re.findall(r"url\((['\"]?)(.*?)\1\)", tag["style"]):
            u = normalized_url(partial[1])
            if u: assets[u] = True

    # Exclude first-party dynamic endpoints and ad analytics; include static resources only.
    static = {}
    for url in assets:
        path = urllib.parse.urlsplit(url).path.lower()
        if "/api/" in path or "/catalog/" in path or "/payment/" in path or "/pusher" in path:
            continue
        static[url] = True
    print("FOUND ASSET URLS", len(static))
    downloaded = {}
    failures = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as pool:
        for url, name, error in pool.map(fetch_asset, [(u,None) for u in static]):
            if name: downloaded[url] = name
            else: failures[url] = error
    print("DOWNLOADED ASSETS", len(downloaded), "FAILED", len(failures))
    # Keep all literal HTML content. Only convert downloaded asset URLs to
    # local browser-save-style references. This is not a product rewrite.
    for tag in soup.find_all(["img","source","video","audio","script","link"]):
        for attr in ["src","href","poster"]:
            if not tag.has_attr(attr):
                continue
            url = normalized_url(tag[attr])
            if url in downloaded:
                tag[attr] = ASSETS.name + "/" + downloaded[url]
        for attr in ["srcset", "imagesrcset"]:
            if tag.has_attr(attr):
                parts=[]
                for seg in tag[attr].split(","):
                    bits=seg.strip().split()
                    if bits:
                        url=normalized_url(bits[0])
                        if url in downloaded: bits[0] = ASSETS.name + "/" + downloaded[url]
                    parts.append(" ".join(bits))
                tag[attr] = ", ".join(parts)
    HTML.write_text("<!DOCTYPE html>\n" + str(soup), encoding="utf-8")
    manifest = {
        "origin_url": URL, "model": MODEL,
        "source_type": ("Original live Chromium DOM saved after page load" if MHTML.exists() else "Original server HTML response, not browser-hydrated DOM"),
        "html_bytes": HTML.stat().st_size, "mhtml_bytes": MHTML.stat().st_size if MHTML.exists() else None,
        "asset_count": len(downloaded), "asset_failures": failures,
        "note": "HTML references local _files folder for downloaded assets; missing assets stay live URLs. MHTML is standalone."
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        z.write(HTML, HTML.name)
        if MHTML.exists(): z.write(MHTML, MHTML.name)
        z.write(MANIFEST, MANIFEST.name)
        for child in ASSETS.iterdir():
            if child.is_file(): z.write(child, ASSETS.name + "/" + child.name)
    print("RESULT", json.dumps({"html":str(HTML),"zip":str(ARCHIVE),"mhtml":str(MHTML),
                                "html_bytes":HTML.stat().st_size,"zip_bytes":ARCHIVE.stat().st_size,
                                "images":len(downloaded), "failures":len(failures)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
