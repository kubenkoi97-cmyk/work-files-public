#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import requests, re
from bs4 import BeautifulSoup
data=[
("https://kentatsu.group/?s=KTKB18HZBN1&post_type=product","KTKB18HZBN1"),
("https://kentatsu.group/?s=KTTB160HZBN1&post_type=product","KTTB160HZBN1"),
("https://kentatsu.group/?s=KTHB40HZBN1&post_type=product","KTHB40HZBN1"),
("https://kentatsuair.ru/search/?q=KTKB18HZBN1","KTKB18HZBN1"),
("https://kentatsuair.ru/catalog/?q=KTKB18HZBN1","KTKB18HZBN1"),
("https://kentatsuair.ru/catalog/vnutrennie_bloki_vrf_sistemy/?q=KTKB18HZBN1","KTKB18HZBN1"),
("https://kentatsu-aircond.ru/search/?q=KTKB18HZBN1","KTKB18HZBN1"),
("https://kentatsu-kondicioner.ru/search/?q=KTKB18HZBN1","KTKB18HZBN1"),
("https://daichi.market/search/?q=KTKB18HZBN1","KTKB18HZBN1"),
("https://daichi.business/search/?q=KTKB18HZBN1","KTKB18HZBN1"),
("https://russia-midea.ru/?s=MIH90GHN18%28DP%29&post_type=product","MIH90GHN18(DP)"),
("https://midea-pro.ru/catalog/vnutrennie-bloki-vrf-sistemy/?q=MIH90GHN18","MIH90GHN18"),
("https://www.klimat-master.ru/?s=MIH90GHN18","MIH90GHN18"),
]
def one(entry):
  url,model=entry
  try:
    r=requests.get(url,timeout=15,headers={"User-Agent":"Mozilla/5.0"})
    soup=BeautifulSoup(r.text,"html.parser")
    items=[]
    for a in soup.find_all("a",href=True):
      h=a.get("href","");t=a.get_text(" ",strip=True)
      if model.lower().replace("(","").replace(")","") in (t+" "+h).lower().replace("(","").replace(")",""):
        link=urljoin(r.url,h)
        if link not in items:items.append(link)
    return url,r.status_code,len(r.content),soup.title.get_text(" ",strip=True)[:90] if soup.title else "",items[:12]
  except Exception as e:return url,"ERROR",0,str(e)[:110],[]
with ThreadPoolExecutor(max_workers=8) as pool:
 for x in pool.map(one,data):
  print("SEARCHPROBE",x,flush=True)
