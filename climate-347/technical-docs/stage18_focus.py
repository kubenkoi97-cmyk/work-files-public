import csv,io,zipfile,re,hashlib,json,pathlib,subprocess,collections,concurrent.futures as cf
import requests,pymupdf as fitz
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
root=pathlib.Path("/tmp/climate347v18");root.mkdir(exist_ok=True)
tag="climate-347-pdf-stage17-45511680707"
def dl(tag,name,sha=None):
 p=root/name;subprocess.run(["gh","release","download",tag,"-p",name,"-D",str(root)],check=True)
 if sha:assert hashlib.file_digest(p.open("rb"),"sha256").hexdigest()==sha
 return p
def read(b):return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"))))
def csvbytes(rs):
 s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs);return s.getvalue().encode("utf-8-sig")
inv=read(dl(tag,"coverage_347.csv").read_bytes());assert len(inv)==347
focus=[r for r in inv if int(r["prepared_pdf_count"])==0];assert len(focus)==20
assert hashlib.sha256("\n".join(sorted(r["brand"]+"\t"+r["model"] for r in inv)).encode()).hexdigest()=="b11a94ae13d7ee8d9563e23ec22c51136e968abdbe0d8261f74ded25e3c30343"
print("FOCUS",[(r["brand"],r["model"]) for r in focus],flush=True)
headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf,text/html,*/*"}
def exact(m,t):
 m=re.sub(r"\s+","",m);p=r"(?<![A-Za-z0-9])"+r"\s*".join(re.escape(c) if c!="-" else r"[-‐‑–−]" for c in m)+r"(?![A-Za-z0-9_/(‐‑–−-])"
 return bool(re.search(p,t,re.I))
seeds=["https://chel.igc-aircon.com/product/promyshlennye_konditsionery/ruftop/","https://www.igc-aircon.com/product/kryshnye_konditsionery_ruftop/","https://igc.com.ru/library/","https://kzn.iclim.ru/library/?brand=IGC","https://masterxoloda.ru/tehnicheskaya-biblioteka/servisnaya-dokumentatsiya/servis-manual-igc/","https://igc.com.ru/catalog/naruzhnye_bloki_vrf_sistemy/igc_ims_ex330nb_7/","https://iclim.ru/catalog/promyshlennye_konditsionery/fankoyly/igc_iwf_q1700caq4t22/","https://toplan.ru/igc-iwf-q1700caq4t22.html"]
for r in focus:
 m=r["model"]
 if m.startswith("IRFT-"):
  slug=m.lower().replace("-","_").replace("/","_")
  seeds.extend(["https://igc.com.ru/catalog/kryshnye_konditsionery/igc_"+slug+"/","https://igc-aircon.com/product/kryshnye_konditsionery_ruftop/kryshnyy_konditsioner_ruftop_"+("tolko_kholod_" if "CA/" in m else "")+slug+"/"])
def page(u):
 try:
  r=requests.get(u,headers=headers,timeout=(7,16));r.raise_for_status()
  soup=BeautifulSoup(r.text,"html.parser");links=[]
  for a in soup.find_all("a",href=True):
   dst=urljoin(r.url,a["href"]);label=" ".join(a.stripped_strings)
   if urlparse(dst).scheme not in ("http","https"):continue
   if re.search(r"\.pdf(?:$|\?)|download\.php",dst,re.I):
    if re.search(r"сертификат|деклараци|certificate|declaration|гарантийн|warranty|оферта|offer|референс|reference",label+" "+dst,re.I):continue
    if re.search(r"IRFT|руфтоп|CAQ4T22|IMS.?7|IMS-EX330",label+" "+dst,re.I):links.append((dst,label))
  return dict(url=u,http=r.status_code,links=len(links),error=""),links
 except Exception as e:return dict(url=u,http=0,links=0,error=str(e)[:240]),[]
pages=[];found={}
with cf.ThreadPoolExecutor(max_workers=12) as ex:
 for rec,links in ex.map(page,list(dict.fromkeys(seeds))):
  pages.append(rec)
  for u,label in links:found.setdefault(u,label)
print("PAGE_AUDIT",len(pages),len(found),flush=True)
# Candidate mirrors are tried with ordinary TLS verification. No bypass.
passport_path="/upload/iblock/4ac/n32mwonne52y8c1h825ug2ycqtqdtr0x.pdf"
alt_path="/upload/iblock/6e2/6e2ddb6516f0a13ecb68f6facaff6ec2.pdf"
sources=[("IMS7_catalog_COK.pdf","https://www.c-o-k.ru/library/catalogs/igc/38195/140669.pdf"),("IMS7_catalog_regional.pdf","https://chel.igc-aircon.com/upload/iblock/8e1/f2umkqwfiqx3p6b65iz03odbvjqw01vo.pdf"),("IGC_industrial_catalog_mirror.pdf","https://frostweld.ru/upload/iblock/44f/q2xhhqxappc3rwiyxksxqjk61iwg0gfb.pdf"),("IGC_industrial_catalog_official.pdf","https://igc-aircon.com/upload/iblock/8f9/8f98b005f051961e1a68d1afb83fb3fa.pdf")]
for host in ["www.igc-aircon.com","chel.igc-aircon.com","nsk.igc-aircon.com","www.nsk.igc-aircon.com"]:
 sources.append(("IMS7_passport_"+host+".pdf","https://"+host+passport_path))
 sources.append(("IMS7_alt_"+host+".pdf","https://"+host+alt_path))
# Explicitly unverified counterpart URL, inferred only as a search probe from T44 naming pattern.
for host in ["igc.com.ru","iclim.ru","kzn.iclim.ru","spb.iclim.ru"]:
 sources.append(("T22_probe_"+host+".pdf","https://"+host+"/library/igc-iwf-q-caq4t22-pasport.pdf"))
for i,u in enumerate(found):
 if i<20:sources.append(("linked_candidate_"+str(i)+".pdf",u))
def fetch(item):
 n,u=item
 try:
  with requests.get(u,headers=headers,timeout=(8,25),stream=True) as r:
   r.raise_for_status();buf=bytearray()
   for c in r.iter_content(65536):
    if c:
     if not buf and not c.startswith(b"%PDF-"):raise ValueError("not PDF")
     buf.extend(c)
     if len(buf)>110*1024*1024:raise ValueError("size cap")
  raw=bytes(buf);hits={};imgs={}
  with fitz.open(stream=raw,filetype="pdf") as d:
   assert len(d)>0
   for i,pg in enumerate(d):
    t=pg.get_text();h=[r["model"] for r in focus if exact(r["model"],t)]
    # Explicit generation heading plus base SKU, only for IMS7.
    if re.search(r"IMS\s*7",t,re.I) and exact("IMS-EX330NB",t):h.append("IMS-EX330NB(7) [series heading + base]")
    if h:hits[i+1]=h
   for i in sorted(set([1]+sorted(hits,key=lambda k:-len(hits[k]))[:6])):
    imgs[n+"_p"+str(i)+".jpg"]=d[i-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).tobytes("jpeg",jpg_quality=90)
   cover=d[0].get_text()[:500]
  return item,raw,hits,imgs,cover,""
 except Exception as e:return item,None,{},{},"",str(e)[:240]
newpdf={};preview={};attempts=[];seen={}
with cf.ThreadPoolExecutor(max_workers=8) as ex:
 for item,raw,hits,imgs,cover,error in ex.map(fetch,sources):
  n,u=item;sha=hashlib.sha256(raw).hexdigest() if raw else "";status="FAILED";dest=""
  if raw:
   if sha in seen:status="DUPLICATE";dest=seen[sha]
   else:
    status="EXACT_TEXT_REVIEW_REQUIRED" if hits else "NO_EXACT_MODEL_TEXT_REVIEW"
    dest="CANDIDATES/"+n;newpdf[dest]=raw;seen[sha]=dest;preview.update(imgs)
  attempts.append(dict(filename=n,url=u,bytes=len(raw) if raw else 0,sha256=sha,status=status,archive_path=dest,model_pages=json.dumps(hits,ensure_ascii=False),cover=cover,error=error))
  print("FETCH",n,status,len(raw) if raw else 0,hits,error,flush=True)
# Preserve confirmed SMK service original separately (no target URL; no coverage increase).
prev=dl(tag,"Climate_347_stage17_delta_review.zip","765e994d3134d6855a797da267c265b55c24a27e9667b2ce4fecddb23d62f632")
with zipfile.ZipFile(prev) as z:
 names=[n for n in z.namelist() if n.startswith("BLOCKED_NO_BASE_URL/") and n.endswith(".pdf")];assert len(names)==1
 raw=z.read(names[0]);assert hashlib.sha256(raw).hexdigest()=="d06d15a648b9f1bffa4d7815308cf2b3ef286a7d792c2a679975b0f60956ccf8"
 with fitz.open(stream=raw,filetype="pdf") as d:
  assert exact("SMK-D140HHN1-3",d[0].get_text())
  preview["SMK_confirmed_service_p1.jpg"]=d[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).tobytes("jpeg",jpg_quality=90)
 blocked={names[0]:raw}
# Actual public ZIP test, not token-authenticated.
public={}
try:
 u="https://github.com/kubenkoi97-cmyk/work-files-public/releases/download/"+tag+"/Climate_347_stage17_partial_Selectel.zip"
 with requests.get(u,headers={"Range":"bytes=0-3"},stream=True,timeout=(8,15)) as r:public={"http":r.status_code,"signature":next(r.iter_content(4)).hex()}
except Exception as e:public={"error":str(e)}
summary=dict(focus_models=20,covered_unchanged=327,source_attempts=len(attempts),unique_downloaded_candidates=len(newpdf),exact_text_candidates=sum(x["status"]=="EXACT_TEXT_REVIEW_REQUIRED" for x in attempts),confirmed_blocked=1,new_selectel_assignments=0,stage17_public=public,notes="Candidates and blocked originals only. Not an upload package. No certificates/declarations intended. Existing 327 not modified.")
reports={"focus_20.csv":csvbytes(focus),"download_attempts.csv":csvbytes(attempts),"page_search_audit.csv":csvbytes(pages)}
for n,v in reports.items():(root/n).write_bytes(v)
out=root/"Climate_347_stage18_focused_review.zip"
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for n,v in {**newpdf,**blocked,**{"PREVIEWS/"+n:v for n,v in preview.items()},**{"REPORTS/"+n:v for n,v in reports.items()}}.items():z.writestr(n,v)
 z.writestr("REPORTS/summary.json",json.dumps(summary,ensure_ascii=False,indent=2))
with zipfile.ZipFile(out) as z:assert z.testzip() is None
summary["archive_sha256"]=hashlib.file_digest(out.open("rb"),"sha256").hexdigest()
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print("RESULT",json.dumps(summary,ensure_ascii=False),flush=True)
