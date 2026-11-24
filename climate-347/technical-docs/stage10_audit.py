import csv,io,zipfile,re,hashlib,json,pathlib,subprocess,collections,requests
import pymupdf as fitz
root=pathlib.Path("/tmp/climate347v10");root.mkdir(exist_ok=True)
tag="climate-347-pdf-stage9-45505224491"
def download(name,sha):
 p=root/name;subprocess.run(["gh","release","download",tag,"-p",name,"-D",str(root)],check=True)
 assert hashlib.file_digest(p.open("rb"),"sha256").hexdigest()==sha
 return p
review=download("Climate_347_stage9_review.zip","4add40ccdd6ca5296fc7268c08d5767fd0971595ee461d84a1044905cc91888b")
part=download("Climate_347_stage9_partial_Selectel.zip","74b0a5f45c4b3fba3bb5e3446da5a1552d569142a1ea1542ae026d07a3a2a862")
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
 assert read(z.read("REPORTS/partial_selectel_manifest.csv"))==ms
assert len(inv)==347 and len(ms)==280 and len(upload)==24
keys={(r["brand"],r["model"]):r for r in inv}
assert len(keys)==347
assert hashlib.sha256("\n".join(sorted(b+"\t"+m for b,m in keys)).encode()).hexdigest()=="b11a94ae13d7ee8d9563e23ec22c51136e968abdbe0d8261f74ded25e3c30343"
def html(u,label):
 return '<p>\n <a href="'+u+'" target="_blank"><img src="/images/icons/pdf-icon2.jpg" alt="" style="height:41px; width:40px"></a> <a href="'+u+'" target="_blank">'+label+'</a>\n</p>'
def exact(m,t):
 m=re.sub(r"\s+","",m)
 p=r"(?<![A-Za-z0-9])"+r"\s*".join(re.escape(c) if c!="-" else r"[-‐‑–−]" for c in m)+r"(?![A-Za-z0-9_/(‐‑–−-])"
 return bool(re.search(p,t,re.I))
# Reattempt rejected ATOM B using source document page selection rather than page insertion.
checks=[];new=[]
source="ORIGINAL_PDF/Midea/ATOM_B_catalog.pdf"
raw=originals[source]
found=[r for r in inv if r["brand"]=="Midea" and re.fullmatch(r"MVUH(?:35|50|60|100|120)BT-VA1",r["model"])]
assert len(found)==5
try:
 with fitz.open(stream=raw,filetype="pdf") as original,fitz.open(stream=raw,filetype="pdf") as excerpt:
  idx=[3,15]
  assert all(any(exact(r["model"],original[i].get_text()) for i in idx) for r in found)
  excerpt.select(idx);payload=excerpt.tobytes(garbage=0,deflate=False)
  with fitz.open(stream=payload,filetype="pdf") as out:
   assert len(out)==2
   for j,i in enumerate(idx):
    assert out[j].get_text()==original[i].get_text()
    a=original[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False);b=out[j].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
    assert (a.width,a.height,a.n)==(b.width,b.height,b.n)
    assert a.samples==b.samples,"render differs"
 for r in found:
  name="ATOM_B_catalog.pdf";u=r["base_url"]+name;dest="UPLOAD_TO_SELECTEL/"+u.removeprefix("https://docs.proclimate5.ru/")
  upload[dest]=payload
  rec=dict(brand=r["brand"],model=r["model"],filename=name,document_kind="catalog",label_ru="Страница каталога",base_url=r["base_url"],full_url=u,html=html(u,"Страница каталога"),archive_path=dest,sha256=hashlib.sha256(payload).hexdigest(),pages="4 16",status="PREPARED_NOT_UPLOADED")
  ms.append(rec);new.append(rec)
 checks.append({"source":source,"result":"PASS","detail":"source pages 4,16 text and pixel identical; visual model table checked stage9"})
except Exception as e:checks.append({"source":source,"result":"REJECTED","detail":str(e)})
# Get new candidate from actual manufacturer library link, no approval without visual scope.
candidates=[("Midea","V4plusW_manual_candidate.pdf","https://midea-pro.ru/library/midea-v4-w-instruktsiya-ekspluatatsiya.pdf?v=fd5ed6eca11fa36da27de45c2f8e092d4d02b329e9ca7ba1ebc311134ee05c7c")]
newpdf={};previews={};attempts=[]
for brand,name,url in candidates:
 try:
  r=requests.get(url,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf"},timeout=(8,20));r.raise_for_status();raw=r.content
  assert raw.startswith(b"%PDF-") and len(raw)<100*1024*1024
  with fitz.open(stream=raw,filetype="pdf") as d:
   assert len(d)>0
   previews[name+"_p1.jpg"]=d[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).tobytes("jpeg",jpg_quality=90)
   first=d[0].get_text()[:1500]
  sha=hashlib.sha256(raw).hexdigest();duplicate=next((p for p,v in originals.items() if hashlib.sha256(v).hexdigest()==sha),"")
  if not duplicate:newpdf["ORIGINAL_PDF/"+brand+"/"+name]=raw
  attempts.append(dict(filename=name,url=url,bytes=len(raw),sha256=sha,status="DUPLICATE" if duplicate else "DOWNLOADED_REVIEW_REQUIRED",cover_text=first,error=""))
 except Exception as e:attempts.append(dict(filename=name,url=url,bytes=0,sha256="",status="FAILED",cover_text="",error=str(e)))
# Find exact model-bearing V4+W pages and render those and stage9 new sources.
for p,raw in {**originals,**newpdf}.items():
 if not any(s in p for s in ("V4plusW_catalog","V4plusW_manual_candidate","MIH_FHN18_installation_manual_candidate","V8_indoor_service_manual")):continue
 with fitz.open(stream=raw,filetype="pdf") as d:
  if "V4plusW_catalog" in p:
   hits=[i for i,page in enumerate(d) if all(exact(m,page.get_text()) for m in ["MVUW252A-VA3","MVUW280A-VA3","MVUW335A-VA3"])]
   print("V4_PAGES",p,[i+1 for i in hits],flush=True)
   selected=hits[:8]
  else:selected=[0]
  for i in selected:previews[pathlib.Path(p).stem+"_p"+str(i+1)+".jpg"]=d[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).tobytes("jpeg",jpg_quality=88)
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
for file,content in [("Climate_347_stage10_partial_Selectel.zip",upload),("Climate_347_stage10_delta_review.zip",{**newpdf,**{"PREVIEWS/"+n:v for n,v in previews.items()}})]:
 p=root/file
 with zipfile.ZipFile(p,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
  for n,v in content.items():z.writestr(n,v)
  for n,v in files.items():z.writestr("REPORTS/"+n,v)
  z.writestr("REPORTS/summary.json",json.dumps(summary,ensure_ascii=False,indent=2))
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
 summary[file+"_sha256"]=hashlib.file_digest(p.open("rb"),"sha256").hexdigest()
# Check previous published zip publicly without GitHub auth.
u="https://github.com/kubenkoi97-cmyk/work-files-public/releases/download/"+tag+"/Climate_347_stage9_partial_Selectel.zip"
try:
 with requests.get(u,headers={"Range":"bytes=0-3"},stream=True,timeout=(8,15)) as r:
  summary["stage9_anonymous_http"]=r.status_code;summary["stage9_anonymous_signature"]=next(r.iter_content(4)).hex()
except Exception as e:summary["stage9_anonymous_error"]=str(e)
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print("RESULT",json.dumps(summary,ensure_ascii=False),flush=True)
