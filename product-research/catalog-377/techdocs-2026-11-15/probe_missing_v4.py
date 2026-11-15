#!/usr/bin/env python3
"""Fresh source audit for 49 model-unverified and 4 declaration-only SKUs."""
import requests,fitz,csv,re,json,concurrent.futures,time,hashlib
from pathlib import Path
root=Path("product-research/catalog-377/techdocs-2026-11-14/independent-audit-v7-2026-11-14/model_exact_coverage.csv")
rows=list(csv.DictReader(root.open(encoding="utf-8-sig",newline="")))
assert len(rows)==377
CANDIDATES=[
("Midea","MI2_G_DP","https://www.iclim.ru/library/midea-mi2-gdhn18-at-dp-instruktsiya.pdf"),
("Midea","MI2_DL","https://www.iclim.ru/library/midea-mi2-dldhn18-at-instruktsiya.pdf"),
("Midea","MI2_Q4","https://www.iclim.ru/library/midea-mi2-q4-instruktsiya.pdf"),
("Kentatsu","KTHV","https://www.iclim.ru/library/kentatsu-kthv-instruktsiya.pdf"),
("Kentatsu","KTHV","https://www.iclim.ru/library/kentatsu-kthv-hzbn1-instruktsiya.pdf"),
("Kentatsu","KTHV","https://www.iclim.ru/library/kentatsu-dx-pro-basic-kthv-hzbn1-instruktsiya.pdf"),
("Kentatsu","KTHV","https://daichi.business/upload/iblock/173/plt7xnrg9r0io2pcmkql6fs00ouc25oc/K3_2026_DK26_02.01.03_30.01.26_low_resolution.pdf"),
("Kentatsu","KTHV","https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf"),
("IGC","IMS_4TM","https://igc-aircon.com/upload/iblock/2fd/g7gqb0wx6uqkoxuz7qf9lnhfzsxzpmks.pdf"),
("IGC","IMS_4TM","https://igc-aircon.com/upload/iblock/ad9/ad99f9ee15dfc57e2620d5c588d1f108.pdf"),
("IGC","IMS_4TM","https://www.c-o-k.ru/library/catalogs/igc/38333/141247.pdf"),
("IGC","IMS_K","https://igc-aircon.com/upload/iblock/2fd/g7gqb0wx6uqkoxuz7qf9lnhfzsxzpmks.pdf"),
("IGC","IMS_K","https://www.c-o-k.ru/library/catalogs/igc/38333/141247.pdf"),
("IGC","IMS_K","https://www.c-o-k.ru/library/catalogs/igc/38195/140669.pdf"),
("IGC","IMS_BH","https://igc-aircon.com/upload/iblock/ad9/ad99f9ee15dfc57e2620d5c588d1f108.pdf"),
("IGC","IMS_BH","https://www.c-o-k.ru/library/catalogs/igc/38333/141247.pdf"),
("IGC","IMS_4T_Q","https://www.c-o-k.ru/library/catalogs/igc/38195/140669.pdf"),
("IGC","IMS_QV","https://igc-aircon.com/upload/iblock/2fd/g7gqb0wx6uqkoxuz7qf9lnhfzsxzpmks.pdf"),
]
def clean(s):return re.sub(r"[^a-z0-9]","",s.casefold())
def probe(it):
 brand,group,url=it
 ms=[r["model"] for r in rows if r["brand"]==brand and r["series_key"]==group]
 resp=requests.get(url,timeout=70,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf,*/*"})
 if not(resp.ok and resp.content.startswith(b"%PDF-")):
  return dict(brand=brand,group=group,url=url,http=resp.status_code,valid=False,bytes=len(resp.content),found=[],total=len(ms))
 with fitz.open(stream=resp.content,filetype="pdf") as doc:
  pages=[clean(page.get_text("text")) for page in doc]
  actual={m:[idx+1 for idx,p in enumerate(pages) if clean(m) in p] for m in ms}
  matches={m:p for m,p in actual.items() if p}
  sample=' '.join(p.get_text("text")[:450] for p in list(doc)[:2])
 return dict(brand=brand,group=group,url=url,http=resp.status_code,valid=True,bytes=len(resp.content),pages=len(pages),sha256=hashlib.sha256(resp.content).hexdigest(),found=list(matches),hits=matches,model_count=len(ms),text_sample=sample[:280])
def job(it):
 try:return probe(it)
 except Exception as exc:return dict(brand=it[0],group=it[1],url=it[2],error=str(exc)[:250])
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 results=list(pool.map(job,CANDIDATES))
for a in results:
 print(json.dumps(a,ensure_ascii=False),flush=True)
Path("/tmp/mixed_v4_probe.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
