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
