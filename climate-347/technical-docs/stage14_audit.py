import csv,io,zipfile,re,hashlib,json,pathlib,subprocess,collections,requests
import pymupdf as fitz
root=pathlib.Path("/tmp/climate347v14");root.mkdir(exist_ok=True)
tag="climate-347-pdf-stage9-45505224491"
def download(name,sha,tag=tag):
 p=root/name;subprocess.run(["gh","release","download",tag,"-p",name,"-D",str(root)],check=True)
 assert hashlib.file_digest(p.open("rb"),"sha256").hexdigest()==sha
 return p
review=download("Climate_347_stage9_review.zip","4add40ccdd6ca5296fc7268c08d5767fd0971595ee461d84a1044905cc91888b")
part=download("Climate_347_stage13_partial_Selectel.zip","86217f6c5aaec722db6ad774e2156421683909428c2436297def7966d5c8ff37","climate-347-pdf-stage13-45508467525")
delta13=download("Climate_347_stage13_delta_review.zip","ef83e2e931e51d914a4339441b370d7b61262720757808e71699a1b580953447","climate-347-pdf-stage13-45508467525")
delta11=download("Climate_347_stage11_delta_review.zip","a81cbcfad75c569783d8e114c592f33ba15113ee680546a90b88cf3b356dd9b4","climate-347-pdf-stage11-45506953322")
delta=download("Climate_347_stage10_delta_review.zip","65937f3b6a2ba630dc393995f7c770cf192cc17db3c6717800f865861588f51f","climate-347-pdf-stage10-45506222255")
def read(raw):return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
def data(rs):
 s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs);return s.getvalue().encode("utf-8-sig")
with zipfile.ZipFile(review) as z:
 assert z.testzip() is None
 inv=read(z.read("REPORTS/coverage_347.csv"))
 ms=read(z.read("REPORTS/partial_selectel_manifest.csv"))
 originals={n:z.read(n) for n in z.namelist() if n.startswith("ORIGINAL_PDF/") and n.endswith(".pdf")}
with zipfile.ZipFile(part) as z:
 assert z.testzip() is None
 upload={n:z.read(n) for n in z.namelist() if n.startswith("UPLOAD_TO_SELECTEL/")}
 ms=read(z.read("REPORTS/partial_selectel_manifest.csv"))
 inv=read(z.read("REPORTS/coverage_347.csv"))
with zipfile.ZipFile(delta) as z:
 assert z.testzip() is None
 originals.update({n:z.read(n) for n in z.namelist() if n.startswith("ORIGINAL_PDF/") and n.endswith(".pdf")})
 previews={pathlib.Path(n).name:z.read(n) for n in z.namelist() if n.startswith("PREVIEWS/") and n.endswith(".jpg")}
with zipfile.ZipFile(delta11) as z:
 assert z.testzip() is None
 originals.update({n:z.read(n) for n in z.namelist() if n.startswith("CANDIDATE_PDF/") and n.endswith(".pdf")})
with zipfile.ZipFile(delta13) as z:
 assert z.testzip() is None
 originals.update({n:z.read(n) for n in z.namelist() if n.startswith('CANDIDATE_PDF/') and n.endswith('.pdf')})
assert len(inv)==347 and len(ms)==316 and len(upload)==30
keys={(r["brand"],r["model"]):r for r in inv}
assert len(keys)==347
assert hashlib.sha256("\n".join(sorted(b+"\t"+m for b,m in keys)).encode()).hexdigest()=="b11a94ae13d7ee8d9563e23ec22c51136e968abdbe0d8261f74ded25e3c30343"
def html(u,label):
 return '<p>\n <a href="'+u+'" target="_blank"><img src="/images/icons/pdf-icon2.jpg" alt="" style="height:41px; width:40px"></a> <a href="'+u+'" target="_blank">'+label+'</a>\n</p>'
def exact(m,t):
 m=re.sub(r"\s+","",m)
 p=r"(?<![A-Za-z0-9])"+r"\s*".join(re.escape(c) if c!="-" else r"[-‐‑–−]" for c in m)+r"(?![A-Za-z0-9_/(‐‑–−-])"
 return bool(re.search(p,t,re.I))
allowed={"catalog","manual","combined_manual_passport","installation","technical","wiring","passport","service","datasheet","drawing","user_manual"}
assert all(m["document_kind"] in allowed and not re.search(r"certificate|declaration|сертификат|деклараци|warranty|гарантийн",m["filename"]+" "+m["label_ru"],re.I) for m in ms)
checks=[];new=[];attempts=[];newpdf={};previews={}
# Bosch original cover inspected in this session, exact SHA and codes.
rules=[
("CANDIDATE_PDF/Bosch/MDCI_installation_6720862926_candidate.pdf","MDCI_20_26_3_installation_manual_DE.pdf","Инструкция по монтажу (DE)","installation",r"MDCI\s*(22|26)-3",2,[1],None,"d2d0f0145287c04a2149d37b40f19c2d8407e313fb8b95a0952ce3bcd82ee6f3"),
("CANDIDATE_PDF/Bosch/Bosch_MDCI_catalog_2022_candidate.pdf","MDCI_dimensional_drawings.pdf","Габаритные чертежи","drawing",r"MDCI\s*\d+-[13]",11,[2,3],[4],"db0c9429cb0c628a2d35bb88971a29ca061ce3c7d62928034aa0aff1b184e9f6")]
for source,name,label,kind,rx,n,pages,clip,sha0 in rules:
 try:
  raw=originals[source];assert hashlib.sha256(raw).hexdigest()==sha0
  found=[r for r in inv if r["brand"]=="Bosch" and re.fullmatch(rx,r["model"]) and r["base_url"]]
  assert len(found)==n,(len(found),n)
  with fitz.open(stream=raw,filetype="pdf") as d:
   texts=[d[i-1].get_text() for i in pages]
   assert all(any(exact(r["model"],t) for t in texts) for r in found)
   if clip:
    with fitz.open(stream=raw,filetype="pdf") as out:
     out.select([i-1 for i in clip]);payload=out.tobytes(garbage=0,deflate=False)
    with fitz.open(stream=payload,filetype="pdf") as out:
     for j,i in enumerate(clip):
      a=d[i-1].get_pixmap(alpha=False);c=out[j].get_pixmap(alpha=False)
      assert out[j].get_text()==d[i-1].get_text() and (a.width,a.height,a.n)==(c.width,c.height,c.n) and a.samples==c.samples
   else:payload=raw
   # All pages render at low scale to validate file integrity.
   for pg in d:pg.get_pixmap(matrix=fitz.Matrix(.15,.15),alpha=False)
  sha=hashlib.sha256(payload).hexdigest();add=[]
  for r in found:
   u=r["base_url"]+name;dest="UPLOAD_TO_SELECTEL/"+u.removeprefix("https://docs.proclimate5.ru/")
   if dest in upload:assert upload[dest]==payload
   assert not any(m["brand"]==r["brand"] and m["model"]==r["model"] and (m["full_url"]==u or m["sha256"]==sha) for m in ms)
   add.append(dict(brand=r["brand"],model=r["model"],filename=name,document_kind=kind,label_ru=label,base_url=r["base_url"],full_url=u,html=html(u,label),archive_path=dest,sha256=sha,pages=" ".join(map(str,clip or pages)),status="PREPARED_NOT_UPLOADED"))
  for m in add:upload[m["archive_path"]]=payload
  ms.extend(add);new.extend(add)
  checks.append(dict(source=source,result="PASS",detail=f"{n} exact models; source page visually checked; universal document."))
 except Exception as e:checks.append(dict(source=source,result="REJECTED",detail=repr(e)))
# Official Bosch document numbers for the exact family; do not approve without viewing downloaded pages.
sources=[
("Bosch","MDCI_8_18_installation_6720862924_DE.pdf","https://bosch-de-de.boschhc-documents.com/download/pdf/file/6720862924"),
("Bosch","MDCI_8_18_user_6720862925_DE.pdf","https://bosch-de-de.boschhc-documents.com/download/pdf/file/6720862925"),
("Bosch","MDCI_20_26_user_6720862927_DE_candidate.pdf","https://bosch-de-de.boschhc-documents.com/download/pdf/file/6720862927"),
("Bosch","VRF_planning_6721818579_DE_candidate.pdf","https://buderus-de-de.boschtt-documents.com/download/file/file/6721818579.pdf")]
import concurrent.futures
def fetch(item):
 brand,name,u=item
 try:
  with requests.get(u,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf,*/*"},stream=True,timeout=(8,20)) as r:
   r.raise_for_status();buf=bytearray()
   for c in r.iter_content(65536):
    if c:
     if not buf and not c.startswith(b"%PDF-"):raise ValueError("not PDF")
     buf.extend(c)
     if len(buf)>100*1024*1024:raise ValueError("size cap")
  raw=bytes(buf)
  with fitz.open(stream=raw,filetype="pdf") as d:
   assert len(d)>0
   cover=d[0].get_text()[:1500]
   imgs={name+"_p1.jpg":d[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).tobytes("jpeg",jpg_quality=86)}
   hits=[]
   for i,pg in enumerate(d):
    t=pg.get_text();h=[r["model"] for r in inv if r["brand"]=="Bosch" and exact(r["model"],t)]
    if h:hits.append((len(h),i,h))
   for _,i,h in sorted(hits,reverse=True)[:4]:
    imgs[name+"_p"+str(i+1)+".jpg"]=d[i].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).tobytes("jpeg",jpg_quality=86)
  return item,raw,imgs,cover,""
 except Exception as e:return item,None,{},"",str(e)[:240]
hashes={hashlib.sha256(v).hexdigest() for v in originals.values()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for item,raw,imgs,cover,err in ex.map(fetch,sources):
  b,n,u=item;sha=hashlib.sha256(raw).hexdigest() if raw else "";status="FAILED"
  if raw:
   status="DUPLICATE" if sha in hashes else "DOWNLOADED_REVIEW_REQUIRED"
   if sha not in hashes:newpdf["CANDIDATE_PDF/"+b+"/"+n]=raw;hashes.add(sha)
   previews.update(imgs)
  attempts.append(dict(filename=n,url=u,bytes=len(raw) if raw else 0,sha256=sha,status=status,cover_text=cover,error=err))
# Separate scope evidence for Midea winter option pages. No automatic assignment.
for p,raw in originals.items():
 if "Daichi" not in p and "Midea" not in p:continue
 if not any(x in p.lower() for x in ("catalog","regional")):continue
 with fitz.open(stream=raw,filetype="pdf") as d:
  hits=[]
  for i,pg in enumerate(d):
   t=pg.get_text()
   if re.search(r"низкотемпературн\w*\s+комплект",t,re.I) and re.search(r"[-−–]\s*40",t) and re.search(r"V8M|V8S|V8i|VC\s*MAX",t,re.I):hits.append(i)
  for i in hits[:6]:
   n=pathlib.Path(p).stem+"_winter_p"+str(i+1)+".jpg"
   previews[n]=d[i].get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False).tobytes("jpeg",jpg_quality=86)
   print("WINTER_PAGE",p,i+1,flush=True)
assert all(m["document_kind"] in allowed and not re.search(r"certificate|declaration|сертификат|деклараци|warranty|гарантийн",m["filename"]+" "+m["label_ru"],re.I) for m in ms)
previewdir=pathlib.Path("climate-347/technical-docs/stage14-previews");previewdir.mkdir(exist_ok=True)
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
 status="TECH_PREPARED" if substantive else "CATALOG_ONLY" if tech else "BLOCKED_NO_BASE_URL" if not r["base_url"] else "WINTER_BASE_ONLY" if r["model"].endswith("/-40") else "NO_PREPARED_DOCUMENT"
 nextstep=("Check other applicable document types; no completeness claim" if status=="TECH_PREPARED" else "Find exact manuals beyond catalog" if status=="CATALOG_ONLY" else "Find exact technical manual, declaration not enough" if status=="DECLARATION_ONLY" else "User must supply URL path; do not infer" if status=="BLOCKED_NO_BASE_URL" else "Find applicable winter-kit instructions and exact scope; base manual alone insufficient" if status=="WINTER_BASE_ONLY" else "Find or verify exact source and prepare file")
 if r["model"].endswith("/-40") and rr:nextstep="Find exact winter-kit installation and operating documentation; catalog option alone insufficient"
 rec=dict(brand=k[0],model=k[1],base_url=r["base_url"],prepared_pdf_count=len(rr),technical_pdf_count=len(tech),substantive_technical_count=len(substantive),types=" | ".join(m["document_kind"] for m in rr),files=" | ".join(m["filename"] for m in rr),status=status,next_step=nextstep,selectel_status="NOT_UPLOADED")
 coverage.append(rec);brands[k[0]][status]+=1
 if status!="TECH_PREPARED" or k[1].endswith("/-40"):remaining.append(rec)
 if rr:htmlrows.append(dict(brand=k[0],model=k[1],document_count=len(rr),html="\n".join(m["html"] for m in rr),status="PREPARED_NOT_UPLOADED"))
summary=dict(policy="UNIVERSAL_TECH_ONLY_NO_CERTIFICATES_OR_DECLARATIONS",total_models=347,prepared_models=len(by),technical_models=sum(r["technical_pdf_count"]>0 for r in coverage),substantive_technical_models=sum(r["substantive_technical_count"]>0 for r in coverage),declaration_only=sum(r["status"]=="DECLARATION_ONLY" for r in coverage),no_prepared_document=347-len(by),assignments=len(ms),prepared_files=len(upload),new_assignments=len(new),new_originals=len(newpdf),status_counts=dict(collections.Counter(r["status"] for r in coverage)),by_brand={b:dict(c) for b,c in brands.items()},checks=checks,attempts=attempts,selectel_uploaded=False,workbook_changed=False)
assert len(by)==len(htmlrows) and sum(summary["status_counts"].values())==347
files={"coverage_347.csv":data(coverage),"remaining.csv":data(remaining),"html_by_model.csv":data(htmlrows),"partial_selectel_manifest.csv":data(ms),"download_attempts.csv":data(attempts)}
for n,v in files.items():(root/n).write_bytes(v)
for file,content in [("Climate_347_stage14_partial_Selectel.zip",upload),("Climate_347_stage14_delta_review.zip",{**newpdf,**{"PREVIEWS/"+n:v for n,v in previews.items()}})]:
 p=root/file
 with zipfile.ZipFile(p,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
  for n,v in content.items():z.writestr(n,v)
  for n,v in files.items():
   if "partial_Selectel" in file and n=="excluded_documents_audit.csv":continue
   z.writestr("REPORTS/"+n,v)
  z.writestr("REPORTS/summary.json",json.dumps(summary,ensure_ascii=False,indent=2))
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
 summary[file+"_sha256"]=hashlib.file_digest(p.open("rb"),"sha256").hexdigest()
# Check previous published zip publicly without GitHub auth.
u="https://github.com/kubenkoi97-cmyk/work-files-public/releases/download/climate-347-pdf-stage13-45508467525/Climate_347_stage13_partial_Selectel.zip"
try:
 with requests.get(u,headers={"Range":"bytes=0-3"},stream=True,timeout=(8,15)) as r:
  summary["stage13_anonymous_http"]=r.status_code;summary["stage13_anonymous_signature"]=next(r.iter_content(4)).hex()
except Exception as e:summary["stage13_anonymous_error"]=str(e)
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print("RESULT",json.dumps(summary,ensure_ascii=False),flush=True)
