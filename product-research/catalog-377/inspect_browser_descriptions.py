#!/usr/bin/env python3
"""Inspect browser-rendered original product pages for descriptions hidden from HTTP HTML.

This is a diagnostic. No synthetic marketing text is inserted into originals.
Records H1, meta description, JSON-LD Product.description, exact-model text in
the rendered main section, image count, and screenshot. Never fabricates status.
"""
import asyncio,json,re
from pathlib import Path
from urllib.parse import urlsplit
from playwright.async_api import async_playwright

ROOT=Path("product-research/catalog-377/browser-diagnostics")
ROOT.mkdir(parents=True,exist_ok=True)
SAMPLES=[
("Kentatsu","KTKB18HZBN1","https://gorodskie-sistemy.ru/polupromyshlennoe-oborudovanie/vrf-sistemy-kondicionirovaniya/vnutrennij-blok-vrv/vnutrennij-blok-vrf-sistemy-kentatsu-ktkb18hzbn1"),
("Kentatsu","KTTB250HZBN1","https://gorodskie-sistemy.ru/polupromyshlennoe-oborudovanie/vrf-sistemy-kondicionirovaniya/vnutrennij-blok-vrv/vnutrennij-blok-vrf-sistemy-kentatsu-kttb250hzbn1"),
("Midea","MIH90GHN18","https://gorodskie-sistemy.ru/polupromyshlennoe-oborudovanie/vrf-sistemy-kondicionirovaniya/vnutrennij-blok-vrv/vnutrennij-blok-vrf-sistemy-midea-mih90ghn18"),
("Midea","MIH90GHN18(DP)","https://coolsochi.ru/product/midea-mih90ghn18-dp/"),
]
def check_sku(model,text):
    sku=re.sub(r"\s+","",model).upper()
    source=re.sub(r"\s+","",text).upper()
    return bool(re.search(r"(?<![A-Z0-9])"+re.escape(sku)+r"(?![A-Z0-9(])",source))
def jsonld_descriptions(raw,model):
    found=[]
    try:
        a=json.loads(raw)
        nodes=a if isinstance(a,list) else [a]
        while nodes:
            n=nodes.pop()
            if isinstance(n,list):nodes.extend(n);continue
            if not isinstance(n,dict):continue
            t=n.get("@type","")
            types=t if isinstance(t,list) else [t]
            if any("Product" in str(x) for x in types):
                title=str(n.get("name",""))
                if check_sku(model,title):
                    d=n.get("description","")
                    if isinstance(d,str) and len(d)>40:found.append(d[:2500])
            if "@graph" in n:nodes.append(n["@graph"])
    except Exception:pass
    return found
async def one(browser,brand,model,url):
    result={"brand":brand,"model":model,"source_url":url}
    page=await browser.new_page(locale="ru-RU",viewport={"width":1360,"height":900},user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    try:
        response=await page.goto(url,wait_until="domcontentloaded",timeout=35000)
        result["status"]=response.status if response else None
        await page.wait_for_timeout(1800)
        result["final_url"]=page.url
        result["h1"]=await page.locator("h1").all_text_contents()
        result["title"]=await page.title()
        result["meta_description"]=await page.locator('meta[name="description"]').get_attribute("content") if await page.locator('meta[name="description"]').count() else ""
        result["exact_sku_in_heading"]=check_sku(model," ".join(result["h1"]+[result["title"]]))
        result["browser_product_images"]=await page.locator("img").count()
        result["description_sections"]=[]
        for x in await page.locator('section,[id*="descr"],[class*="descr"],[data-tab*="descr"]').all():
            t=(await x.inner_text())[:1800]
            if len(t)>75 and t not in result["description_sections"] and (check_sku(model,t) or "описан" in t.lower()):
                result["description_sections"].append(t)
            if len(result["description_sections"])>=4:break
        result["jsonld_product_descriptions"]=[]
        for r in await page.locator('script[type="application/ld+json"]').all_text_contents():
            result["jsonld_product_descriptions"].extend(jsonld_descriptions(r,model))
        result["dom_length"]=len(await page.content())
        # Keep browser-rendered HTML as a distinct artifact with provenance.
        if result["exact_sku_in_heading"]:
            (ROOT/(brand+"_"+model.replace("(","_").replace(")","")+"_rendered.html")).write_text(await page.content(),encoding="utf-8")
        print("BROWSER_PROBE",json.dumps({k:result.get(k) for k in ("brand","model","status","exact_sku_in_heading","dom_length","browser_product_images","meta_description","description_sections","jsonld_product_descriptions")},ensure_ascii=False)[:3200],flush=True)
    except Exception as e:
        result["error"]=str(e)[:300]
        print("BROWSER_ERROR",model,result["error"],flush=True)
    finally:
        (ROOT/(brand+"_"+model.replace("(","_").replace(")","")+".json")).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
        await page.close()
async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True)
        for x in SAMPLES:
            await one(browser,*x)
        await browser.close()
asyncio.run(main())
