#!/usr/bin/env python3
"""Fetch only regional manufacturer PDF/manual candidates and verify exact remaining 25 SKUs."""
import requests,csv,re,json,concurrent.futures,hashlib,fitz,os
from pathlib import Path
path=Path("product-research/catalog-377/techdocs-2026-11-14/independent-audit-v7-2026-11-14/model_exact_coverage.csv")
rows=list(csv.DictReader(path.open(encoding="utf-8-sig",newline="")))
bygroup={(r['brand'],r['series_key']):[] for r in rows}
for r in rows:bygroup[(r['brand'],r['series_key'])].append(r['model'])
SOURCES={
 "IGC_IMS_5_INSTRUCTION":"https://iclim.ru/library/igc-ims-5-vnutrennie-bloki-instruktsiya.pdf",
 "IGC_IMS_6_INSTRUCTION":"https://iclim.ru/library/igc-ims-6-vnutrennie-bloki-instruktsiya.pdf",
 "IGC_IMS_7_INSTALL":"https://iclim.ru/library/igc-ims-7-instruktsiya-montazh.pdf",
 "IGC_IMS_5_KATALOG_FULL":"https://www.c-o-k.ru/library/catalogs/igc/38333/141247.pdf",
 "IGC_MANUFACTURER_DC5":"https://igc-aircon.com/upload/iblock/6e2/6e2ddb6516f0a13ecb68f6facaff6ec2.pdf",
 "KENTATSU_DXPRO_2026":"https://www.thermotrade.ru/wp-content/uploads/2026/01/kentatsu-kotly-bytovogo-i-promyshlennogo-naznacheniya-2026_280126.pdf",
 "KENTATSU_DXPRO_BASIC_2026":"https://daichi.business/upload/iblock/173/plt7xnrg9r0io2pcmkql6fs00ouc25oc/K3_2026_DK26_02.01.03_30.01.26_low_resolution.pdf",
 "KENTATSU_DXPRO_CATALOG":"https://www.c-o-k.ru/library/catalogs/kentatsu/37986/140011.pdf",
 "KENTATSU_DXPRO_SALES":"https://kentatsu.group/wa-content/docs/vrf.pdf",
}
TARGETS=["IMS_K","IMS_BH","IMS_4TM","IMS_4T_Q","IMS_QV","KTHV"]
target_models=[r for r in rows if r['series_key'] in TARGETS and ((r['brand']=="Kentatsu" and r['series_key']=="KTHV") or r['brand']=="IGC")]
def clean(x):return re.sub(r"[^A-Z0-9]","",str(x).upper())
def probe(item):
 name,url=item
 try:
  r=requests.get(url,timeout=(15,100),headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf"})
  if not(r.ok and r.content.startswith(b"%PDF-")):
   return dict(name=name,url=url,status=r.status_code,bytes=len(r.content),error='not_pdf')
  with fitz.open(stream=r.content,filetype="pdf") as doc:
   pg=[clean(p.get_text("text")) for p in doc]
   hits={r['model']:[i+1 for i,p in enumerate(pg) if clean(r['model']) in p] for r in target_models}
   hits={k:v for k,v in hits.items() if v}
   grp_hits={g:sum(bool(re.search("(?<![A-Z0-9])"+re.escape(g)+"(?![A-Z0-9])",p)) for p in pg) for g in TARGETS}
   return dict(name=name,url=url,status=r.status_code,bytes=len(r.content),pages=len(doc),sha256=hashlib.sha256(r.content).hexdigest(),exact_hits=hits,series_page_counts=grp_hits)
 except Exception as e:return dict(name=name,url=url,error=str(e)[:400])
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
 result=list(pool.map(probe,SOURCES.items()))
for r in result:print('RESULT_V6',json.dumps(r,ensure_ascii=False),flush=True)
Path('/tmp/mixed_v6_probe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
