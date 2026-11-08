import sys
sys.path.insert(0,"product-research/catalog-377")
import capture_batch as c
from bs4 import BeautifulSoup

for model in ["IMS-BS22NHQ(DC)", "IMS-1T28NH (DC)", "IMS-4TM28NH (DC5)", "IMS-BH220NH(DC)"]:
    links=c.igc_http_candidates(model)
    print("CANDIDATES",model,len(links),links[:5],flush=True)
    for u in links[:2]:
        r=c.get(u,timeout=17)
        print("RESPONSE",r.status_code if r else None,r.url if r else u,len(r.content) if r else 0,flush=True)
        if r:
            soup=BeautifulSoup(r.text,"html.parser")
            print("HEADS",[(x.get_text(" ",strip=True))[:140] for x in soup.select("h1")][:4],
                  "TITLE",soup.title.get_text(" ",strip=True)[:140] if soup.title else "",flush=True)
            p=c.parse_source(u,"IGC",model,r)
            print("PARSED",bool(p),"DETAILS",{k:p[k] for k in ["has_description","has_specs","title","photos"]} if p else {},flush=True)

print("HTTP_INDEX_LINES",len(c.IGC_HTTP_INDEX))
for segment in ["bs22nhq","1t28nh","4tm28nh","4t140nhq","ahu220nh"]:
    hits=[(title,url) for title,url in c.IGC_HTTP_INDEX if segment in (title+" "+url).lower()]
    print("INDEX_HITS",segment,len(hits),hits[:5],flush=True)
known_urls=[
"http://igc-aircon.com/product/kanalnye_bloki_vrf/vnutrenniy_kanalnyy_ploskiy_blok_igc_ims_bs22nhq_dc/",
"http://igc-aircon.com/product/kassetnye_vrf_1_potochnye_komplekty/vnutrenniy_kassetnyy_1_potochnyy_blok_igc_ims_1t28nh_dc_komplekt/"
]
for u in known_urls:
    r=c.get(u,timeout=16)
    p=c.parse_source(u,"IGC","IMS-BS22NHQ(DC)" if "bs22" in u else "IMS-1T28NH (DC)",r)
    soup=BeautifulSoup(r.text,"html.parser") if r else None
    print("KNOWN_URL",u,"status",r.status_code if r else None,
          "h1",[x.get_text(" ",strip=True) for x in soup.select("h1")] if soup else None,
          "parsed",bool(p),"gallery",len(p["photos"]) if p else 0,flush=True)
