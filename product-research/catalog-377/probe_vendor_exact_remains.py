#!/usr/bin/env python3
"""Check discovered genuine seller product URLs for unresolved models.

Do not accept guessed URLs as evidence unless exact SKU in product heading,
real description, specs and product gallery confirmed. Logs stdout only.
"""
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import re
todo=[
("Midea","MIH90GHN18(DP)","https://midea-pro.ru/catalog/vnutrennie-bloki-vrf-sistemy/midea-mih90ghn18-dp/"),
("Midea","MIH90GHN18(DP)","https://russia-midea.ru/midea-mih-gdp-v8-mih90ghn18dp/"),
("Midea","MIH90GHN18(DP)","https://www.klimat-master.ru/mih90ghn18-dp/"),
("Midea","MIH90GHN18","https://midea-pro.ru/catalog/vnutrennie-bloki-vrf-sistemy/midea-mih90ghn18/"),
("Midea","MIH90GHN18","https://russia-midea.ru/midea-mih-g-v8-mih90ghn18/"),
("Kentatsu","KTKB18HZBN1","https://russia-kentatsu.ru/kentatsu-ktkb18hzbn1/"),
("Kentatsu","KTKB18HZBN1","https://kentatsu-pro.ru/catalog/vrf_sistemy/vnutrennie_bloki/ktkb18hzbn1/"),
("Kentatsu","KTKB18HZBN1","https://kentatsu-air.ru/ktkb18hzbn1/"),
("Kentatsu","KTKB18HZBN1","https://kentatsu-russia.ru/ktkb18hzbn1/"),
("Kentatsu","KTKB18HZBN1","https://climatehnik.com/catalog/promyshlennye-konditsionery/vrf-sistemy/mini-vrf/vnutrennie-bloki/kentatsu-deiks-pro-beysik-dx-pro-basic-ktkb-ktkb18hzbn1/"),
("Kentatsu","KTTB60HZBN1","https://russia-kentatsu.ru/kentatsu-kttb60hzbn1/"),
("Kentatsu","KTHB40HZBN1","https://russia-kentatsu.ru/kentatsu-kthb40hzbn1/"),
("Kentatsu","KTHB40HZBN1","https://climatehnik.com/catalog/promyshlennye-konditsionery/vrf-sistemy/mini-vrf/vnutrennie-bloki/kentatsu-deiks-pro-beysik-dx-pro-basic-kthb-kthb40hzbn1/"),
("Kentatsu","KTTB60HZBN1","https://climatehnik.com/catalog/promyshlennye-konditsionery/vrf-sistemy/mini-vrf/vnutrennie-bloki/kentatsu-deiks-pro-beysik-dx-pro-basic-kttb-kttb60hzbn1/"),
("IGC","IMS-BS36NHQ(DC)","http://igc-aircon.com/product/kanalnye_bloki_vrf/vnutrenniy_kanalnyy_ploskiy_blok_igc_ims_bs36nhq_dc/"),
]
def chk(x):
    brand,sku,url=x
    try:
        r=requests.get(url,timeout=16,headers={"User-Agent":"Mozilla/5.0"},allow_redirects=True)
        s=BeautifulSoup(r.text,"html.parser")
        primary=" ".join(x.get_text(" ",strip=True) for x in s.find_all("h1"))
        title=s.title.get_text(" ",strip=True) if s.title else ""
        text=s.get_text(" ",strip=True).lower()
        model=re.sub(r"\s+","",sku).lower()
        normalized=re.sub(r"\s+","",primary).lower()
        return (sku,r.status_code,len(r.content),r.url,
                model in normalized,
                "описание" in text,"характеристики" in text,
                len(s.find_all("img")),primary[:180],title[:100])
    except Exception as e:
        return (sku,"ERROR",0,url,False,False,False,0,str(e)[:140],"")
with ThreadPoolExecutor(max_workers=8) as pool:
    for z in pool.map(chk,todo):
        print("PROBE",z,flush=True)
