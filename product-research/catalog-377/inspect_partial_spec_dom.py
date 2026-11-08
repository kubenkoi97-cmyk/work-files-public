import csv,requests
from pathlib import Path
from bs4 import BeautifulSoup
path=Path("product-research/catalog-377/status/master_status.csv")
with path.open(encoding="utf-8-sig",newline="") as f:
    rows={x["model"]:x for x in csv.DictReader(f)}
for model in ["KTKB18HZBN1","KTTB250HZBN1","KTHB40HZBN1","MIH90GHN18","MIH90GHN18(DP)"]:
    row=rows[model]
    try:
        r=requests.get(row["source_url"],timeout=17,headers={"User-Agent":"Mozilla/5.0"})
        soup=BeautifulSoup(r.text,"html.parser")
        print("MODEL",model,"STATUS",r.status_code,"BYTE",len(r.content),
            "TRS",len(soup.select("tr")),"DT",len(soup.select("dt")),flush=True)
        tr=soup.select("tr")
        for t in tr[:55]:
            vals=[x.get_text(" ",strip=True) for x in t.find_all(["th","td"],recursive=False)]
            if len(vals)>=2:
                print("SPECROW",model,repr(vals[:4]),flush=True)
        for dt in soup.select("dt")[:5]:
            print("DL",model,repr(dt.get_text(" ",strip=True)),repr(dt.find_next_sibling("dd").get_text(" ",strip=True) if dt.find_next_sibling("dd") else ""),flush=True)
    except Exception as e:print("EXCEPTION",model,str(e)[:180],flush=True)
