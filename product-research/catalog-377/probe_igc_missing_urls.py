"""Find archived exact HTML products omitted from the current IGC site listing."""
import csv
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

sys.path.insert(0,"product-research/catalog-377")
import capture_batch as c

models=["IMS-BS22NH (DC)","IMS-BS36NH(DC)","IMS-BS45NH(DC)",
        "IMS-BS36NHQ(DC)","IMS-BS45NHQ(DC)","IMS-BS56NHQ(DC)","IMS-BS71NHQ(DC)",
        "IMS-BH220NH(DC)","IMS-BH280NH(DC)",
        "IMS-4T140NHQ(DC)","IMS-QV100NH(DC)","IMS-AHU220NH(DC)","IMS-AHU280NH(DC)"]

def guesses(model):
    slug=re.sub(r"[^a-z0-9]+","_",model.lower().replace(" ","")).strip("_")
    root="http://igc-aircon.com/product/"
    options=[]
    if model.startswith("IMS-BS"):
        for prefix in ["vnutrenniy_kanalnyy_ploskiy_blok_igc_","vnutrenniy_kanalnyy_ploskiy_blok_igc_200mm_","vnutrenniy_kanalnyy_ploskiy_blok_igc_200_"]:
            options.append(root+"kanalnye_bloki_vrf/"+prefix+slug+"/")
    elif model.startswith("IMS-BH"):
        for prefix in ["vnutrenniy_vysokonapornyy_kanalnyy_blok_igc_","vnutrenniy_kanalnyy_vysokonapornyy_blok_igc_","vnutrenniy_vysokonapor_kanalnyy_blok_igc_"]:
            options.append(root+"kanalnye_bloki_vrf/"+prefix+slug+"/")
    elif model.startswith("IMS-4T"):
        options.append(root+"kassetnye_vrf_4_kh_potochnye_komplekty/vnutrenniy_kassetnyy_4_kh_potoch_blok_igc_"+slug+"_komplekt/")
    elif model.startswith("IMS-QV"):
        for prefix in ["vnutrenniy_napolno_potolochnyy_blok_igc_","vnutrenniy_napolno_potolochnyy_blok_igc_","vnutrenniy_napolno_potolochnyy_blok_"]:
            options.append(root+"napolno_potolochnye_bloki_vrf/"+prefix+slug+"/")
    elif model.startswith("IMS-AHU"):
        for category in ["kanalnye_bloki_vrf","pritochnye_bloki_vrf","ventilyatsionnye_ustanovki_vrf"]:
            for prefix in ["vnutrenniy_blok_igc_","vnutrenniy_kanalnyy_blok_igc_"]:
                options.append(root+category+"/"+prefix+slug+"/")
    return list(dict.fromkeys(options))
pairs=[(m,url) for m in models for url in guesses(m)]
def inspect(pair):
    model,u=pair
    try:
        r=requests.get(u,timeout=14,headers={"User-Agent":"Mozilla/5.0"})
        if r.status_code != 200 or len(r.content)<4000:
            return model,u,r.status_code,"",0
        soup=BeautifulSoup(r.text,"html.parser")
        h1=" ".join(h.get_text(" ",strip=True) for h in soup.select("h1"))
        title=soup.title.get_text(" ",strip=True) if soup.title else ""
        valid=c.exact_model_in_text(model,h1+" "+title)
        return model,u,r.status_code,("EXACT "+h1[:130] if valid else "MISMATCH "+h1[:100]),len(soup.find_all("img"))
    except Exception as e:
        return model,u,"ERROR",str(e)[:65],0
print("TESTING",len(pairs),"CANDIDATES",flush=True)
with ThreadPoolExecutor(max_workers=15) as pool:
    responses=list(pool.map(inspect,pairs))
for model in models:
    rs=[x for x in responses if x[0]==model]
    matches=[x for x in rs if str(x[3]).startswith("EXACT")]
    exists=[x for x in rs if x[2]==200]
    print("MODEL",model,"MATCHES",matches,"HTTP200",exists[:3],"TOTAL",len(rs),flush=True)
