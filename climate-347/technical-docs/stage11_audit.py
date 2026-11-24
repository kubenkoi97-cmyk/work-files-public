import csv,io,zipfile,re,hashlib,json,pathlib,subprocess,collections,requests
import pymupdf as fitz
root=pathlib.Path("/tmp/climate347v11");root.mkdir(exist_ok=True)
tag="climate-347-pdf-stage9-45505224491"
def download(name,sha,tag=tag):
 p=root/name;subprocess.run(["gh","release","download",tag,"-p",name,"-D",str(root)],check=True)
 assert hashlib.file_digest(p.open("rb"),"sha256").hexdigest()==sha
 return p
review=download("Climate_347_stage9_review.zip","4add40ccdd6ca5296fc7268c08d5767fd0971595ee461d84a1044905cc91888b")
part=download("Climate_347_stage10_partial_Selectel.zip","70e89960f4b17b67b29d708181d6ace1fd788270c357184f859d1ac4acff60a4","climate-347-pdf-stage10-45506222255")
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
assert len(inv)==347 and len(ms)==285 and len(upload)==25
keys={(r["brand"],r["model"]):r for r in inv}
assert len(keys)==347
assert hashlib.sha256("\n".join(sorted(b+"\t"+m for b,m in keys)).encode()).hexdigest()=="b11a94ae13d7ee8d9563e23ec22c51136e968abdbe0d8261f74ded25e3c30343"
def html(u,label):
 return '<p>\n <a href="'+u+'" target="_blank"><img src="/images/icons/pdf-icon2.jpg" alt="" style="height:41px; width:40px"></a> <a href="'+u+'" target="_blank">'+label+'</a>\n</p>'
def exact(m,t):
 m=re.sub(r"\s+","",m)
 p=r"(?<![A-Za-z0-9])"+r"\s*".join(re.escape(c) if c!="-" else r"[-‐‑–−]" for c in m)+r"(?![A-Za-z0-9_/(‐‑–−-])"
 return bool(re.search(p,t,re.I))
# Exact Daikin winter catalogue page visually inspected (PDF page 111, printed 109).
checks=[];new=[];attempts=[];newpdf={}
source="ORIGINAL_PDF/Daikin/VRV_IV_S_winter_catalog.pdf"
try:
 raw=originals[source]
 found=[r for r in inv if r["brand"]=="Daikin" and re.fullmatch(r"RXYQ(?:8|10|12|14|16|18|20)U/-40",r["model"])]
 assert len(found)==7
 with fitz.open(stream=raw,filetype="pdf") as orig,fitz.open(stream=raw,filetype="pdf") as clip:
  i=110;t=orig[i].get_text()
  assert all(exact(r["model"],t) for r in found),repr(t[-3500:])
  clip.select([i]);payload=clip.tobytes(garbage=0,deflate=False)
  with fitz.open(stream=payload,filetype="pdf") as out:
   assert len(out)==1 and out[0].get_text()==t
   a=orig[i].get_pixmap(alpha=False);b=out[0].get_pixmap(alpha=False)
   assert (a.width,a.height,a.n)==(b.width,b.height,b.n) and a.samples==b.samples
  previews["Daikin_RXYQ_U_winter_catalog_p111.jpg"]=orig[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).tobytes("jpeg",jpg_quality=90)
 name="VRV_IVplus_winter_option_catalog.pdf"
 for r in found:
  u=r["base_url"]+name;dest="UPLOAD_TO_SELECTEL/"+u.removeprefix("https://docs.proclimate5.ru/")
  upload[dest]=payload
  rec=dict(brand=r["brand"],model=r["model"],filename=name,document_kind="catalog",label_ru="Страница каталога",base_url=r["base_url"],full_url=u,html=html(u,"Страница каталога"),archive_path=dest,sha256=hashlib.sha256(payload).hexdigest(),pages="111",status="PREPARED_NOT_UPLOADED")
  ms.append(rec);new.append(rec)
 checks.append(dict(source=source,result="PASS",detail="Seven exact RXYQ-U/-40 models; page 111 catalog only; no winter-kit manual claim. Text and pixel identical."))
except Exception as e:checks.append(dict(source=source,result="REJECTED",detail=str(e)))
# Extract embedded document links and decode catalogue QR codes, preserving exact provenance.
import cv2,numpy as np
from urllib.parse import urlparse
allowed=("daichi.business","daichi.ru","kentatsu.ru","kentatsu.group","kentatsuair.ru","kentatsu.global","kentatsurussia.ru","midea-pro.ru","air-midea.com","midea.com","midea.ru","qrco.de","qrcod.ru","qr-code.ru","q-r.to")
def permitted(url):
 h=(urlparse(url).hostname or "").lower()
 return urlparse(url).scheme in ("http","https") and any(h==d or h.endswith("."+d) for d in allowed)
urls={}
for p,raw in originals.items():
 if not any(s in p for s in ["DX_PRO_VII_catalog","V8Si_catalog","ATOM_B_catalog","V4plusW_catalog","VC_MAX_catalog"]):continue
 with fitz.open(stream=raw,filetype="pdf") as d:
  if "DX_PRO_VII_catalog" in p:ids=[31,32,33,34]
  elif "V4plusW_catalog" in p:ids=list(range(143,148))
  else:ids=list(range(min(4,len(d))))
  for i in ids:
   if i>=len(d):continue
   pg=d[i]
   for link in pg.get_links():
    u=link.get("uri","")
    if u:urls.setdefault(u,[]).append(p+"#"+str(i+1)+" annotation")
   r=pg.rect
   # The manual QR codes are typically in the top right; inspect a wider band.
   clip=fitz.Rect(r.width*.62,0,r.width,r.height*.34)
   pix=pg.get_pixmap(matrix=fitz.Matrix(4,4),clip=clip,alpha=False)
   img=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)
   detector=cv2.QRCodeDetector()
   try:
    val,_,_=detector.detectAndDecode(img)
    if val:urls.setdefault(val,[]).append(p+"#"+str(i+1)+" QR")
    ok,vals,_,_=detector.detectAndDecodeMulti(img)
    if ok:
     for val in vals:
      if val:urls.setdefault(val,[]).append(p+"#"+str(i+1)+" QR")
   except cv2.error:pass
   if "DX_PRO_VII_catalog" in p or "V4plusW_catalog" in p:
    previews[pathlib.Path(p).stem+"_p"+str(i+1)+".jpg"]=pg.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).tobytes("jpeg",jpg_quality=88)
# Follow only known manufacturer/library domains. Do not fetch arbitrary annotation targets.
links=[]
hashes={hashlib.sha256(v).hexdigest():p for p,v in originals.items()}
for i,(u,where) in enumerate(urls.items()):
 rec=dict(url=u,source=" | ".join(sorted(set(where))),status="RECORDED",final_url="",bytes=0,sha256="",error="")
 if permitted(u):
  try:
   with requests.get(u,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf,*/*"},timeout=(8,18),stream=True) as r:
    rec["final_url"]=r.url;r.raise_for_status()
    it=r.iter_content(65536);first=next(it,b"")
    if first.startswith(b"%PDF-"):
     buf=bytearray(first)
     for chunk in it:
      buf.extend(chunk)
      if len(buf)>80*1024*1024:raise ValueError("size limit")
     raw=bytes(buf);sha=hashlib.sha256(raw).hexdigest();rec.update(bytes=len(raw),sha256=sha)
     if sha in hashes:rec["status"]="DUPLICATE"
     else:
      with fitz.open(stream=raw,filetype="pdf") as pdf:
       assert len(pdf)>0
       fname="catalog_link_"+str(i)+"_"+sha[:8]+".pdf"
       newpdf["CANDIDATE_PDF/"+fname]=raw
       previews[fname+"_p1.jpg"]=pdf[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).tobytes("jpeg",jpg_quality=88)
      hashes[sha]=fname;rec["status"]="DOWNLOADED_REVIEW_REQUIRED"
    else:rec["status"]="NON_PDF_DESTINATION"
  except Exception as e:rec["error"]=str(e)[:240];rec["status"]="FAILED"
 links.append(rec)
 print("LINK",json.dumps(rec,ensure_ascii=False),flush=True)
if not links:links=[dict(url="",source="",status="NO_DECODED_LINKS",final_url="",bytes=0,sha256="",error="")]
attempts=links
# Save actual rendered pages as individual files for next visual audit.
previewdir=pathlib.Path("climate-347/technical-docs/stage11-previews");previewdir.mkdir(exist_ok=True)
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
 substantive=[m for m in tech if m["document_kind"]!="catalog"]
 status="TECH_PREPARED" if substantive else "CATALOG_ONLY" if tech else "DECLARATION_ONLY" if rr else "BLOCKED_NO_BASE_URL" if not r["base_url"] else "WINTER_BASE_ONLY" if r["model"].endswith("/-40") else "NO_PREPARED_DOCUMENT"
 nextstep=("Check other applicable document types; no completeness claim" if status=="TECH_PREPARED" else "Find exact manuals beyond catalog" if status=="CATALOG_ONLY" else "Find exact technical manual, declaration not enough" if status=="DECLARATION_ONLY" else "User must supply URL path; do not infer" if status=="BLOCKED_NO_BASE_URL" else "Find applicable winter-kit instructions and exact scope; base manual alone insufficient" if status=="WINTER_BASE_ONLY" else "Find or verify exact source and prepare file")
 if r["model"].endswith("/-40") and rr:nextstep="Find exact winter-kit installation and operating documentation; catalog option alone insufficient"
 rec=dict(brand=k[0],model=k[1],base_url=r["base_url"],prepared_pdf_count=len(rr),technical_pdf_count=len(tech),substantive_technical_count=len(substantive),types=" | ".join(m["document_kind"] for m in rr),files=" | ".join(m["filename"] for m in rr),status=status,next_step=nextstep,selectel_status="NOT_UPLOADED")
 coverage.append(rec);brands[k[0]][status]+=1
 if status!="TECH_PREPARED" or k[1].endswith("/-40"):remaining.append(rec)
 if rr:htmlrows.append(dict(brand=k[0],model=k[1],document_count=len(rr),html="\n".join(m["html"] for m in rr),status="PREPARED_NOT_UPLOADED"))
summary=dict(total_models=347,prepared_models=len(by),technical_models=sum(r["technical_pdf_count"]>0 for r in coverage),substantive_technical_models=sum(r["substantive_technical_count"]>0 for r in coverage),declaration_only=sum(r["status"]=="DECLARATION_ONLY" for r in coverage),no_prepared_document=347-len(by),assignments=len(ms),prepared_files=len(upload),new_assignments=len(new),new_originals=len(newpdf),status_counts=dict(collections.Counter(r["status"] for r in coverage)),by_brand={b:dict(c) for b,c in brands.items()},checks=checks,attempts=attempts,selectel_uploaded=False,workbook_changed=False)
assert len(by)==len(htmlrows) and sum(summary["status_counts"].values())==347
files={"coverage_347.csv":data(coverage),"remaining.csv":data(remaining),"html_by_model.csv":data(htmlrows),"partial_selectel_manifest.csv":data(ms),"download_attempts.csv":data(attempts)}
for n,v in files.items():(root/n).write_bytes(v)
for file,content in [("Climate_347_stage11_partial_Selectel.zip",upload),("Climate_347_stage11_delta_review.zip",{**newpdf,**{"PREVIEWS/"+n:v for n,v in previews.items()}})]:
 p=root/file
 with zipfile.ZipFile(p,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
  for n,v in content.items():z.writestr(n,v)
  for n,v in files.items():z.writestr("REPORTS/"+n,v)
  z.writestr("REPORTS/summary.json",json.dumps(summary,ensure_ascii=False,indent=2))
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
 summary[file+"_sha256"]=hashlib.file_digest(p.open("rb"),"sha256").hexdigest()
# Check previous published zip publicly without GitHub auth.
u="https://github.com/kubenkoi97-cmyk/work-files-public/releases/download/climate-347-pdf-stage10-45506222255/Climate_347_stage10_partial_Selectel.zip"
try:
 with requests.get(u,headers={"Range":"bytes=0-3"},stream=True,timeout=(8,15)) as r:
  summary["stage10_anonymous_http"]=r.status_code;summary["stage10_anonymous_signature"]=next(r.iter_content(4)).hex()
except Exception as e:summary["stage10_anonymous_error"]=str(e)
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print("RESULT",json.dumps(summary,ensure_ascii=False),flush=True)
