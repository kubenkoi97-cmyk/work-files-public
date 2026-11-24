import csv,io,zipfile,re,hashlib,json,pathlib,subprocess,collections,requests
import pymupdf as fitz
root=pathlib.Path("/tmp/climate347v17");root.mkdir(exist_ok=True)
tag="climate-347-pdf-stage9-45505224491"
def download(name,sha,tag=tag):
 p=root/name;subprocess.run(["gh","release","download",tag,"-p",name,"-D",str(root)],check=True)
 assert hashlib.file_digest(p.open("rb"),"sha256").hexdigest()==sha
 return p
part=download("Climate_347_stage16_partial_Selectel.zip","7c79364ce914ae8d6fc66f3c75cd8dc2008445dab193560520478f290d5f11e5","climate-347-pdf-stage16-45510205798")
delta=download("Climate_347_stage16_delta_review.zip","6509e3d2a9061bb742b90a32f05d0fa49729b126e2fb1cb835f88c017d77ed72","climate-347-pdf-stage16-45510205798")
def read(raw):return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
def data(rs):
 s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs);return s.getvalue().encode("utf-8-sig")
with zipfile.ZipFile(part) as z:
 assert z.testzip() is None
 upload={n:z.read(n) for n in z.namelist() if n.startswith("UPLOAD_TO_SELECTEL/")}
 ms=read(z.read("REPORTS/partial_selectel_manifest.csv"))
 inv=read(z.read("REPORTS/coverage_347.csv"))
 winter=read(z.read("REPORTS/winter_scope_review.csv"))
with zipfile.ZipFile(delta) as z:
 assert z.testzip() is None
 originals={n:z.read(n) for n in z.namelist() if n.startswith("CANDIDATE_PDF/") and n.endswith(".pdf")}
assert len(inv)==347 and len(ms)==405 and len(upload)==40
keys={(r["brand"],r["model"]):r for r in inv}
assert len(keys)==347
assert hashlib.sha256("\n".join(sorted(b+"\t"+m for b,m in keys)).encode()).hexdigest()=="b11a94ae13d7ee8d9563e23ec22c51136e968abdbe0d8261f74ded25e3c30343"
existing={(m["brand"],m["model"]) for m in ms}
missing=[r for r in inv if (r["brand"],r["model"]) not in existing]
assert len(missing)==22
for r in missing:print("FOCUS",r["brand"],r["model"],r["base_url"],flush=True)
def html(u,label):
 return '<p>\n <a href="'+u+'" target="_blank"><img src="/images/icons/pdf-icon2.jpg" alt="" style="height:41px; width:40px"></a> <a href="'+u+'" target="_blank">'+label+'</a>\n</p>'
def exact(m,t):
 m=re.sub(r"\s+","",m)
 p=r"(?<![A-Za-z0-9])"+r"\s*".join(re.escape(c) if c!="-" else r"[-‐‑–−]" for c in m)+r"(?![A-Za-z0-9_/(‐‑–−-])"
 return bool(re.search(p,t,re.I))
allowed={"catalog","manual","combined_manual_passport","installation","technical","wiring","passport","service","datasheet","drawing","user_manual"}
assert all(m["document_kind"] in allowed and not re.search(r"certificate|declaration|сертификат|деклараци|warranty|гарантийн",m["filename"]+" "+m["label_ru"],re.I) for m in ms)
checks=[];new=[];attempts=[];newpdf={};previews={};blocked=[]
import concurrent.futures as cf
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
S=requests.Session()
headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf,text/html,*/*"}
def fetch(item):
 b,n,u=item
 try:
  with requests.get(u,headers=headers,stream=True,timeout=(10,30)) as r:
   r.raise_for_status();buf=bytearray()
   for c in r.iter_content(65536):
    if c:
     if not buf and not c.startswith(b"%PDF-"):raise ValueError("not PDF")
     buf.extend(c)
     if len(buf)>80*1024*1024:raise ValueError("size cap")
  raw=bytes(buf)
  with fitz.open(stream=raw,filetype="pdf") as d:
   assert len(d)>0
   cover=d[0].get_text()[:1200]
   imgs={n+"_p1.jpg":d[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).tobytes("jpeg",jpg_quality=88)}
   hits={}
   for i,pg in enumerate(d):
    t=pg.get_text()
    h=[r["model"] for r in missing if r["brand"]==b and (exact(r["model"],t) or (r["model"].endswith("/-40") and exact(r["model"][:-4],t)))]
    if h:hits[i+1]=h
   for i,h in sorted(hits.items(),key=lambda x:-len(x[1]))[:4]:
    imgs[n+"_p"+str(i)+".jpg"]=d[i-1].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).tobytes("jpeg",jpg_quality=88)
  return item,raw,imgs,cover,hits,""
 except Exception as e:return item,None,{},"",{},str(e)[:240]
sources=[
("Midea","V8M_2025_base_installation_manual.pdf","https://air-midea.com/support/marketing/download/8463/"),
("Midea","V8M_2024_global_catalog.pdf","https://www.midea.com/content/dam/midea-aem/id/PD-Midea-V8-Mini-VRF-R410A-catalogue-2024-12-25-V3-1-.pdf"),
("IGC","IMS7_technical_passport_2026.pdf","https://igc-aircon.com/upload/iblock/4ac/n32mwonne52y8c1h825ug2ycqtqdtr0x.pdf"),
("IGC","IMS7_technical_passport_alternate.pdf","https://igc-aircon.com/upload/iblock/6e2/6e2ddb6516f0a13ecb68f6facaff6ec2.pdf")]
# Discover links directly from official target-category and product pages. Do not download certs/declarations.
seeds=["https://www.igc-aircon.com/product/kryshnye_konditsionery_ruftop_/","https://igc-aircon.com/product/kryshnye_konditsionery_ruftop_/","https://www.igc-aircon.com/product/kassetnye_2_kh_trubnye_fankoyly/","https://igc-aircon.com/product/kassetnye_2_kh_trubnye_fankoyly/","https://iclim.ru/catalog/promyshlennye_konditsionery/fankoyly/igc_iwf_q1700caq4t22/"]
for r in missing:
 if r["model"].startswith("IRFT-"):
  slug=r["model"].lower().replace("-","_").replace("/","_")
  seeds.append("https://iclim.ru/catalog/promyshlennye_konditsionery/kryshnye_konditsionery/igc_"+slug+"/")
def getpage(u):
 try:
  r=requests.get(u,headers=headers,timeout=(8,18));r.raise_for_status()
  soup=BeautifulSoup(r.text,"html.parser")
  links=[]
  for a in soup.find_all("a",href=True):
   dest=urljoin(r.url,a["href"]);label=" ".join(a.stripped_strings)
   if urlparse(dest).scheme not in ("http","https"):continue
   if ".pdf" in urlparse(dest).path.lower() or ("download.php" in dest and re.search(r"паспорт|инструкц|каталог|руководств",label,re.I)):
    links.append((dest,label,"pdf"))
   elif "/product/" in dest and (re.search(r"IRFT-\d|IWF-Q\d+CAQ4T22",label,re.I) or re.search(r"irft_\d|iwf_q\d+caq4t22",dest,re.I)):
    links.append((dest,label,"product"))
  return u,r.status_code,links,""
 except Exception as e:return u,0,[],str(e)[:200]
pageaudit=[];more=set();pdfurls={}
def collect(results):
 for u,status,links,error in results:
  pageaudit.append(dict(url=u,http=status,links=len(links),error=error))
  for dest,label,kind in links:
   if kind=="product":
    if urlparse(dest).hostname in ("igc-aircon.com","www.igc-aircon.com"):more.add(dest)
   elif re.search(r"паспорт|инструкц|каталог|руководств|technical|manual|catalog|passport",label+" "+dest,re.I) and not re.search(r"сертификат|деклараци|certificate|declaration|гарантийн|warranty",label+" "+dest,re.I):
    pdfurls.setdefault(dest,[]).append((u,label))
with cf.ThreadPoolExecutor(max_workers=12) as ex:collect(ex.map(getpage,list(dict.fromkeys(seeds))))
with cf.ThreadPoolExecutor(max_workers=12) as ex:collect(ex.map(getpage,sorted(more-set(seeds))[:35]))
for i,(u,where) in enumerate(pdfurls.items()):
 if i>=25:break
 # Universal candidate from actual linked page; unknown scope, not approved.
 sources.append(("IGC","discovered_technical_"+str(i)+".pdf",u))
print("DISCOVERY",len(pageaudit),len(more),len(pdfurls),flush=True)
hashes={hashlib.sha256(v).hexdigest():p for p,v in {**originals,**upload}.items()}
fetched={}
with cf.ThreadPoolExecutor(max_workers=10) as ex:
 for item,raw,imgs,cover,hits,err in ex.map(fetch,sources):
  b,n,u=item;sha=hashlib.sha256(raw).hexdigest() if raw else "";status="FAILED";path=""
  if raw:
   status="DUPLICATE" if sha in hashes else "DOWNLOADED_REVIEW_REQUIRED"
   if sha not in hashes:
    path="CANDIDATE_PDF/"+b+"/"+n;newpdf[path]=raw;hashes[sha]=path
   else:path=hashes[sha]
   previews.update(imgs);fetched[n]=(raw,sha,path,hits)
  attempts.append(dict(filename=n,url=u,bytes=len(raw) if raw else 0,sha256=sha,status=status,cover_text=cover,error=err,archive_path=path,model_page_hits=json.dumps(hits,ensure_ascii=False)))
  print("FETCH",n,status,len(raw) if raw else 0,flush=True)
# Add only 2 previously empty Midea rows; explicit BASE BLOCK label, not winter-specific instructions.
# Exact product cards confirm winter kit added to these exact base codes; original cover visually inspected.
try:
 raw,sha,path,hits=fetched["V8M_2025_base_installation_manual.pdf"]
 assert sha=="2ba8cb3fb1b744f8ad119bc4c1084be79b4516b8a6b2eaa1b44dd5a81e1ad8ab"
 found=[r for r in missing if r["model"] in ("MV8M-170WV2HN1/-40","MV8M-170WV2GN1/-40")]
 assert len(found)==2
 with fitz.open(stream=raw,filetype="pdf") as d:
  assert all(exact(r["model"][:-4],d[0].get_text()) for r in found)
  for pg in d:pg.get_pixmap(matrix=fitz.Matrix(.15,.15),alpha=False)
 name="V8M_base_installation_and_user_manual_2025.pdf";label="Инструкция базового блока (без зимнего комплекта)"
 for r in found:
  u=r["base_url"]+name;dest="UPLOAD_TO_SELECTEL/"+u.removeprefix("https://docs.proclimate5.ru/")
  upload[dest]=raw
  rec=dict(brand=r["brand"],model=r["model"],filename=name,document_kind="manual",label_ru=label,base_url=r["base_url"],full_url=u,html=html(u,label),archive_path=dest,sha256=sha,pages="1",status="PREPARED_NOT_UPLOADED")
  ms.append(rec);new.append(rec)
 checks.append(dict(source=path,result="PASS_BASE_ONLY",detail="Exact 170 base models, label explicitly excludes winter kit; no change to prior 325 models."))
except Exception as e:checks.append(dict(source="V8M 170 manual",result="REJECTED",detail=repr(e)))
# Confirm hydro module cover against prior visual check, but keep outside final package until BASE_URL.
for p,raw in originals.items():
 if not p.endswith("SMK_D140HHN1_3_service_manual.pdf"):continue
 sha=hashlib.sha256(raw).hexdigest()
 with fitz.open(stream=raw,filetype="pdf") as d:
  assert sha=="d06d15a648b9f1bffa4d7815308cf2b3ef286a7d792c2a679975b0f60956ccf8" and exact("SMK-D140HHN1-3",d[0].get_text())
  blocked.append(dict(brand="Midea",model="SMK-D140HHN1-3",file=p,sha256=sha,status="EXACT_MANUAL_CONFIRMED_NO_BASE_URL"))
  newpdf["BLOCKED_NO_BASE_URL/Midea/SMK-D140HHN1-3_service_manual.pdf"]=raw
# Separate actual new target evidence, not already covered.
assert all((r["brand"],r["model"]) not in existing for r in new)
assert len([m for m in ms if (m["brand"],m["model"]) in existing])==405
previewdir=pathlib.Path("climate-347/technical-docs/stage17-previews");previewdir.mkdir(exist_ok=True)
for n,v in previews.items():(previewdir/pathlib.Path(n).name).write_bytes(v)
# Exact audit from nonempty manifest only, no defaultdict pollution.
priority={"catalog":0,"manual":1,"combined_manual_passport":1,"installation":2,"technical":7,"wiring":8,"passport":10,"declaration":11}
by={};seen=set();sha_seen=set()
for m in ms:
 k=(m["brand"],m["model"]);assert k in keys and keys[k]["base_url"]==m["base_url"]
 assert m["full_url"]==m["base_url"]+m["filename"] and m["html"]==html(m["full_url"],m["label_ru"])
 assert m["archive_path"]=="UPLOAD_TO_SELECTEL/"+m["full_url"].removeprefix("https://docs.proclimate5.ru/")
 assert m["archive_path"] in upload and hashlib.sha256(upload[m["archive_path"]]).hexdigest()==m["sha256"]
 assert (k,m["full_url"]) not in seen and (k,m["sha256"]) not in sha_seen
 seen.add((k,m["full_url"]));sha_seen.add((k,m["sha256"]));by.setdefault(k,[]).append(m)
assert set(upload)=={m["archive_path"] for m in ms}
coverage=[];remaining=[];htmlrows=[];brands=collections.defaultdict(collections.Counter)
for r in inv:
 k=(r["brand"],r["model"]);rr=sorted(by.get(k,[]),key=lambda x:(priority.get(x["document_kind"],9),x["filename"]))
 tech=[m for m in rr if m["document_kind"] not in ("declaration","certificate")]
 substantive=[m for m in tech if m["document_kind"] not in ("catalog","drawing")]
 status="WINTER_BASE_MANUAL_ONLY" if rr and all("без зимнего комплекта" in m["label_ru"] for m in rr) else "TECH_PREPARED" if substantive else "WINTER_CATALOG_ONLY" if tech and r["model"].endswith("/-40") else "CATALOG_ONLY" if tech else "BLOCKED_NO_BASE_URL" if not r["base_url"] else "WINTER_BASE_ONLY" if r["model"].endswith("/-40") else "NO_PREPARED_DOCUMENT"
 nextstep=("Check other applicable document types; no completeness claim" if status=="TECH_PREPARED" else "Find exact manuals beyond catalog" if status=="CATALOG_ONLY" else "Find exact technical manual, declaration not enough" if status=="DECLARATION_ONLY" else "User must supply URL path; do not infer" if status=="BLOCKED_NO_BASE_URL" else "Find applicable winter-kit instructions and exact scope; base manual alone insufficient" if status=="WINTER_BASE_ONLY" else "Find or verify exact source and prepare file")
 if r["model"].endswith("/-40") and rr:nextstep="Find exact winter-kit installation and operating documentation; catalog option alone insufficient"
 rec=dict(brand=k[0],model=k[1],base_url=r["base_url"],prepared_pdf_count=len(rr),technical_pdf_count=len(tech),substantive_technical_count=len(substantive),types=" | ".join(m["document_kind"] for m in rr),files=" | ".join(m["filename"] for m in rr),status=status,next_step=nextstep,selectel_status="NOT_UPLOADED")
 coverage.append(rec);brands[k[0]][status]+=1
 if status!="TECH_PREPARED" or k[1].endswith("/-40"):remaining.append(rec)
 if rr:htmlrows.append(dict(brand=k[0],model=k[1],document_count=len(rr),html="\n".join(m["html"] for m in rr),status="PREPARED_NOT_UPLOADED"))
summary=dict(winter_evidence_rows=len(winter),winter_exact_base_rows=sum(bool(r['exact_base_pages']) for r in winter),policy="UNIVERSAL_TECH_ONLY_NO_CERTIFICATES_OR_DECLARATIONS",total_models=347,prepared_models=len(by),technical_models=sum(r["technical_pdf_count"]>0 for r in coverage),substantive_technical_models=sum(r["substantive_technical_count"]>0 and r["status"]!="WINTER_BASE_MANUAL_ONLY" for r in coverage),base_manual_only=sum(r["status"]=="WINTER_BASE_MANUAL_ONLY" for r in coverage),declaration_only=sum(r["status"]=="DECLARATION_ONLY" for r in coverage),no_prepared_document=347-len(by),assignments=len(ms),prepared_files=len(upload),new_assignments=len(new),new_originals=sum(p.startswith("CANDIDATE_PDF/") for p in newpdf),status_counts=dict(collections.Counter(r["status"] for r in coverage)),by_brand={b:dict(c) for b,c in brands.items()},checks=checks,attempts=attempts,selectel_uploaded=False,workbook_changed=False)
assert len(by)==len(htmlrows) and sum(summary["status_counts"].values())==347
files={"coverage_347.csv":data(coverage),"remaining.csv":data(remaining),"html_by_model.csv":data(htmlrows),"partial_selectel_manifest.csv":data(ms),"download_attempts.csv":data(attempts),"winter_scope_review.csv":data(winter),"focus_22.csv":data(missing),"page_search_audit.csv":data(pageaudit),"blocked_confirmed.csv":data(blocked) if blocked else b"no_records\n"}
for n,v in files.items():(root/n).write_bytes(v)
for file,content in [("Climate_347_stage17_partial_Selectel.zip",upload),("Climate_347_stage17_delta_review.zip",{**newpdf,**{"PREVIEWS/"+n:v for n,v in previews.items()}})]:
 p=root/file
 with zipfile.ZipFile(p,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
  for n,v in content.items():z.writestr(n,v)
  for n,v in files.items():
   if "partial_Selectel" in file and n in ("excluded_documents_audit.csv","blocked_confirmed.csv","page_search_audit.csv"):continue
   z.writestr("REPORTS/"+n,v)
  z.writestr("REPORTS/summary.json",json.dumps(summary,ensure_ascii=False,indent=2))
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
 summary[file+"_sha256"]=hashlib.file_digest(p.open("rb"),"sha256").hexdigest()
# Check previous published zip publicly without GitHub auth.
u="https://github.com/kubenkoi97-cmyk/work-files-public/releases/download/climate-347-pdf-stage16-45510205798/Climate_347_stage16_partial_Selectel.zip"
try:
 with requests.get(u,headers={"Range":"bytes=0-3"},stream=True,timeout=(8,15)) as r:
  summary["stage16_anonymous_http"]=r.status_code;summary["stage16_anonymous_signature"]=next(r.iter_content(4)).hex()
except Exception as e:summary["stage16_anonymous_error"]=str(e)
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print("RESULT",json.dumps(summary,ensure_ascii=False),flush=True)
