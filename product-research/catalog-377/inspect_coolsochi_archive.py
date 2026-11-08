#!/usr/bin/env python3
import zipfile,subprocess,tempfile,re
from pathlib import Path
from bs4 import BeautifulSoup
tag="catalog377-recovery-batch-350-364";filename="catalog377-350-364.zip"
with tempfile.TemporaryDirectory() as t:
    p=subprocess.run(["gh","release","download",tag,"--repo","kubenkoi97-cmyk/work-files-public","-p",filename,"-D",t],capture_output=True,text=True)
    assert p.returncode==0,p.stderr
    z=zipfile.ZipFile(Path(t)/filename)
    matches=[x for x in z.namelist() if "Midea_MIH90GHN18_DP" in x]
    print("MATCHES",matches[:10],flush=True)
    html=next(x for x in matches if x.endswith("/original.html"))
    soup=BeautifulSoup(z.read(html).decode("utf-8","replace"),"html.parser")
    print("H1",[(x.get_text(" ",strip=True)) for x in soup.select("h1")][:2])
    print("TABLES",len(soup.select("table")),"TR",len(soup.select("tr")),"DLS",len(soup.select("dl")))
    for i,tr in enumerate(soup.select("tr")[:50]):
        vals=[x.get_text(" ",strip=True) for x in tr.find_all(["th","td"],recursive=False)]
        if any(vals):print("TR",i,repr(vals[:5]),flush=True)
    for key in ["Мощность нагревания","Охлаждения","Площадь (м²)","Уровень шума","Характеристики Midea"]:
        nodes=soup.find_all(string=lambda q:bool(q and key.lower() in q.lower()))
        print("KEY",key,"N",len(nodes),flush=True)
        for x in nodes[:3]:
            print("NODE",str(x)[:160],"PARENT",str(x.parent)[:500],"GRAND",str(x.parent.parent)[:650],flush=True)
