import csv,io,zipfile,re,hashlib,json,pathlib,subprocess,collections,requests
import pymupdf as fitz
root=pathlib.Path("/tmp/climate347v16");root.mkdir(exist_ok=True)
tag="climate-347-pdf-stage9-45505224491"
def download(name,sha,tag=tag):
 p=root/name;subprocess.run(["gh","release","download",tag,"-p",name,"-D",str(root)],check=True)
 assert hashlib.file_digest(p.open("rb"),"sha256").hexdigest()==sha
 return p
review=download("Climate_347_stage9_review.zip","4add40ccdd6ca5296fc7268c08d5767fd0971595ee461d84a1044905cc91888b")
part=download("Climate_347_stage15_partial_Selectel.zip","a582989e6b60a8a85f5c36e5d71ea25a0d13be3470c78a7ec65d1ad07cb57723","climate-347-pdf-stage15-45509632335")
delta14=download("Climate_347_stage14_delta_review.zip","d997f00089193a4d599a96335f00816a9136716d4d4909e61403382abe183e4c","climate-347-pdf-stage14-45508922665")
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
with zipfile.ZipFile(delta14) as z:
 assert z.testzip() is None
 originals.update({n:z.read(n) for n in z.namelist() if n.startswith('CANDIDATE_PDF/') and n.endswith('.pdf')})
assert len(inv)==347 and len(ms)==334 and len(upload)==34
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
checks=[];new=[];attempts=[];newpdf={};previews={};winter=[]
# Each option page and each selected single-block technical table visually checked in stages 14–16.
# Exact base code and explicit series-wide cooling option support catalogue applicability,
# not a separate winter-kit installation or operating manual. No model suffix is fabricated.
p="ORIGINAL_PDF/Midea/Daichi_regional_catalog_27456.pdf"
raw=originals[p]
families=[
("V8M",r"MV8M-(?:80|100|120|140|160)WV2HN1/-40|MV8M-(?:120|140|160)WV2GN1/-40",91,[92],8),
("V8S",r"MV8S-\d+WV2GN1/-40",95,[97],9),
("V8Si",r"MV8Si-\d+WV2GN1/-40",95,[96],9),
("V8_PRO",r"MV8-\d+WV2GN1\(PRO\)/-40",103,[106,107],15),
("V8i_PRO",r"MV8i-\d+WV2GN1\(PRO\)/-40",103,[104,105],18),
("VC_MAX",r"MVC-M\d+WV2GN1/-40",117,[118,119],12)]
def excerpt(raw,pages):
 with fitz.open(stream=raw,filetype="pdf") as src,fitz.open(stream=raw,filetype="pdf") as dst:
  dst.select([i-1 for i in pages]);out=dst.tobytes(garbage=0,deflate=False)
  with fitz.open(stream=out,filetype="pdf") as d:
   assert len(d)==len(pages)
   for j,i in enumerate(pages):
    a=src[i-1].get_pixmap(alpha=False);b=d[j].get_pixmap(alpha=False)
    assert (a.width,a.height,a.n)==(b.width,b.height,b.n) and a.samples==b.samples, f"render differs page {i}"
    assert d[j].get_text()==src[i-1].get_text(),f"text differs page {i}"
  return out
with fitz.open(stream=raw,filetype="pdf") as d:
 for family,rx,option,tables,expected in families:
  found=[r for r in inv if r["brand"]=="Midea" and r["base_url"] and re.fullmatch(rx,r["model"])]
  try:
   assert len(found)==expected,(len(found),expected)
   t=d[option-1].get_text()
   assert re.search(r"низкотемпературн\w*\s+комплект",t,re.I) and re.search(r"[-−–]\s*40",t),repr(t[:900])
   hits={}
   for r in found:
    base=r["model"][:-4]
    hits[r["model"]]=[i for i in tables if exact(base,d[i-1].get_text())]
   assert all(hits.values()),[m for m,v in hits.items() if not v]
   pages=[option]+tables
   payload=excerpt(raw,pages);sha=hashlib.sha256(payload).hexdigest()
   name=family+"_winter_option_catalog.pdf";label="Страница каталога"
   add=[]
   for r in found:
    u=r["base_url"]+name;dest="UPLOAD_TO_SELECTEL/"+u.removeprefix("https://docs.proclimate5.ru/")
    assert not any(m["brand"]==r["brand"] and m["model"]==r["model"] and (m["full_url"]==u or m["sha256"]==sha) for m in ms)
    add.append(dict(brand=r["brand"],model=r["model"],filename=name,document_kind="catalog",label_ru=label,base_url=r["base_url"],full_url=u,html=html(u,label),archive_path=dest,sha256=sha,pages=" ".join(map(str,pages)),status="PREPARED_NOT_UPLOADED"))
    winter.append(dict(brand="Midea",model=r["model"],base_model=r["model"][:-4],series=family,source=p,source_sha256=hashlib.sha256(raw).hexdigest(),option_page=option,exact_base_pages=" ".join(map(str,hits[r["model"]])),status="CATALOG_SCOPE_CONFIRMED_KIT_MANUAL_MISSING",notes="Exact base table and series winter option (cooling to -40 C); product card confirms winter configuration; not a kit installation manual."))
   for m in add:upload[m["archive_path"]]=payload
   ms.extend(add);new.extend(add)
   checks.append(dict(source=family,result="PASS",detail=f"{len(add)} exact base+option catalogue assignments; source pages {pages}; unchanged render/text."))
  except Exception as e:checks.append(dict(source=family,result="REJECTED",detail=repr(e)))
# 170 models outside regional catalogue table: remain open, no inferred catalogue values.
for r in inv:
 if r["brand"]=="Midea" and r["model"].endswith("/-40") and not any(v["model"]==r["model"] for v in winter):
  winter.append(dict(brand="Midea",model=r["model"],base_model=r["model"][:-4],series="V8M" if r["model"].startswith("MV8M-") else "other",source=p,source_sha256=hashlib.sha256(raw).hexdigest(),option_page="",exact_base_pages="",status="REVIEW_REQUIRED",notes="Exact table or extraction gate unresolved. No automatic assignment."))
# Actual technical candidates only; blocked URL rows may have originals but not assignments.
sources=[
("Midea","SMK_D140HHN1_3_engineering_data.pdf","https://midea-pro.ru/library/midea-smk-d140hhn1-3-instruktsiya.pdf?v=83b3976d001be3f351c6f5f93aef005d54986fef86fed9c052773ac57ad14c04"),
("Midea","SMK_D140HHN1_3_service_manual.pdf","https://www.midea.com.ua/sites/default/files/downloadables-documents/pdf/sm-smk-d140hhn1-3-high-temperature-hydro-modulel.pdf"),
("Midea","V8M_2025_installation_manual_source.pdf","https://air-midea.com/support/marketing/download/8463/"),
("Midea","V8M_2026_engineering_data_candidate.pdf","https://air-midea.com/upload/iblock/cc6/emksezvaxif72jez7staaicqbpojneh7.pdf"),
("IGC","IMS_7_outdoor_installation_candidate.pdf","https://www.airventilation.ru/files/IGC/264879rukovodstvo-po-ustanovke-ekspluatacii-ims-narujny.pdf"),
("Daikin","RXYSQ_T8_installation_manual_RU.pdf","https://daikinair.ru/library/daikin-rxysq4-6t8v-rxysq4-6t8y-4pru482275-1-2017-04-iom-instruktsiya-montazh.pdf"),
("Daikin","VRV_IV_S_user_manual_RU.pdf","https://daikinair.ru/library/daikin-vrv-iv-s-iom-4pru404676-1-2015-05-instruktsiya-ekspluatatsiya.pdf"),
("Daikin","VRV_IV_S_service_manual_candidate.pdf","https://daikinair.ru/library/daikin-mini-vrv4-esie15-12b-servisnaya-instruktsiya.pdf"),
("Daikin","VRV_IVplus_installation_manual_RU.pdf","https://atlantcompany.ru/upload/pdf/%D0%98%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F%20%D0%BF%D0%BE%20%D0%BC%D0%BE%D0%BD%D1%82%D0%B0%D0%B6%D1%83%20Daikin%20VRV%20IV%2B%D0%A2%D0%B5%D0%BF%D0%BB%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BD%D0%B0%D1%81%D0%BE%D1%81%20%D1%81%D0%B5%D1%80%D0%B8%D0%B9%20RXYQU%20RYYQU%20RYMQU.pdf"),
("Daikin","REMQ5U_dimensional_drawing.pdf","https://www.daikin.es/content/dam/MDM/TechnicalDrawings/VRV/REYQ-U%20%2B%20REMQ-U/EN/REYQ8-12U_REMQ5U_dim_2D119001A_EN.pdf"),
("Daikin","REMQ5U_wiring_drawing_part2.pdf","https://www.daikin.es/content/dam/MDM/TechnicalDrawings/VRV/REYQ-U%20%2B%20REMQ-U/EN/REMQ5U_REYQ8-12U_wir3_2D120651A-2_EN.pdf")
]
import concurrent.futures
def fetch(item):
 b,n,u=item
 try:
  with requests.get(u,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf,*/*"},stream=True,timeout=(10,35)) as r:
   r.raise_for_status();buf=bytearray()
   for c in r.iter_content(65536):
    if c:
     if not buf and not c.startswith(b"%PDF-"):raise ValueError("not PDF")
     buf.extend(c)
     if len(buf)>120*1024*1024:raise ValueError("size cap")
  raw=bytes(buf)
  with fitz.open(stream=raw,filetype="pdf") as d:
   assert len(d)>0
   cover=d[0].get_text()[:1200]
   imgs={n+"_p1.jpg":d[0].get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False).tobytes("jpeg",jpg_quality=84)}
   hits=[]
   for i,pg in enumerate(d):
    t=pg.get_text()
    h=[r["model"] for r in inv if r["brand"]==b and exact(r["model"],t)]
    if h:hits.append((len(h),i,h))
   for _,i,h in sorted(hits,reverse=True)[:3]:
    imgs[n+"_p"+str(i+1)+".jpg"]=d[i].get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False).tobytes("jpeg",jpg_quality=84)
  return item,raw,imgs,cover,""
 except Exception as e:return item,None,{},"",str(e)[:240]
hashes={hashlib.sha256(v).hexdigest():p for p,v in originals.items()}
hashes.update({hashlib.sha256(v).hexdigest():p for p,v in upload.items()})
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for item,raw,imgs,cover,err in ex.map(fetch,sources):
  b,n,u=item;sha=hashlib.sha256(raw).hexdigest() if raw else "";status="FAILED";path=""
  if raw:
   status="DUPLICATE" if sha in hashes else "DOWNLOADED_REVIEW_REQUIRED"
   if sha not in hashes:
    path="CANDIDATE_PDF/"+b+"/"+n;newpdf[path]=raw;hashes[sha]=path
   else:path=hashes[sha]
   previews.update(imgs)
  attempts.append(dict(filename=n,url=u,bytes=len(raw) if raw else 0,sha256=sha,status=status,cover_text=cover,error=err,archive_path=path))
  print("FETCH",n,status,len(raw) if raw else 0,flush=True)
assert all(m["document_kind"] in allowed and not re.search(r"certificate|declaration|сертификат|деклараци|warranty|гарантийн",m["filename"]+" "+m["label_ru"],re.I) for m in ms)
previewdir=pathlib.Path("climate-347/technical-docs/stage16-previews");previewdir.mkdir(exist_ok=True)
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
 status="TECH_PREPARED" if substantive else "WINTER_CATALOG_ONLY" if tech and r["model"].endswith("/-40") else "CATALOG_ONLY" if tech else "BLOCKED_NO_BASE_URL" if not r["base_url"] else "WINTER_BASE_ONLY" if r["model"].endswith("/-40") else "NO_PREPARED_DOCUMENT"
 nextstep=("Check other applicable document types; no completeness claim" if status=="TECH_PREPARED" else "Find exact manuals beyond catalog" if status=="CATALOG_ONLY" else "Find exact technical manual, declaration not enough" if status=="DECLARATION_ONLY" else "User must supply URL path; do not infer" if status=="BLOCKED_NO_BASE_URL" else "Find applicable winter-kit instructions and exact scope; base manual alone insufficient" if status=="WINTER_BASE_ONLY" else "Find or verify exact source and prepare file")
 if r["model"].endswith("/-40") and rr:nextstep="Find exact winter-kit installation and operating documentation; catalog option alone insufficient"
 rec=dict(brand=k[0],model=k[1],base_url=r["base_url"],prepared_pdf_count=len(rr),technical_pdf_count=len(tech),substantive_technical_count=len(substantive),types=" | ".join(m["document_kind"] for m in rr),files=" | ".join(m["filename"] for m in rr),status=status,next_step=nextstep,selectel_status="NOT_UPLOADED")
 coverage.append(rec);brands[k[0]][status]+=1
 if status!="TECH_PREPARED" or k[1].endswith("/-40"):remaining.append(rec)
 if rr:htmlrows.append(dict(brand=k[0],model=k[1],document_count=len(rr),html="\n".join(m["html"] for m in rr),status="PREPARED_NOT_UPLOADED"))
summary=dict(winter_evidence_rows=len(winter),winter_exact_base_rows=sum(bool(r['exact_base_pages']) for r in winter),policy="UNIVERSAL_TECH_ONLY_NO_CERTIFICATES_OR_DECLARATIONS",total_models=347,prepared_models=len(by),technical_models=sum(r["technical_pdf_count"]>0 for r in coverage),substantive_technical_models=sum(r["substantive_technical_count"]>0 for r in coverage),declaration_only=sum(r["status"]=="DECLARATION_ONLY" for r in coverage),no_prepared_document=347-len(by),assignments=len(ms),prepared_files=len(upload),new_assignments=len(new),new_originals=len(newpdf),status_counts=dict(collections.Counter(r["status"] for r in coverage)),by_brand={b:dict(c) for b,c in brands.items()},checks=checks,attempts=attempts,selectel_uploaded=False,workbook_changed=False)
assert len(by)==len(htmlrows) and sum(summary["status_counts"].values())==347
files={"coverage_347.csv":data(coverage),"remaining.csv":data(remaining),"html_by_model.csv":data(htmlrows),"partial_selectel_manifest.csv":data(ms),"download_attempts.csv":data(attempts),"winter_scope_review.csv":data(winter)}
for n,v in files.items():(root/n).write_bytes(v)
for file,content in [("Climate_347_stage16_partial_Selectel.zip",upload),("Climate_347_stage16_delta_review.zip",{**newpdf,**{"PREVIEWS/"+n:v for n,v in previews.items()}})]:
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
u="https://github.com/kubenkoi97-cmyk/work-files-public/releases/download/climate-347-pdf-stage15-45509632335/Climate_347_stage15_partial_Selectel.zip"
try:
 with requests.get(u,headers={"Range":"bytes=0-3"},stream=True,timeout=(8,15)) as r:
  summary["stage15_anonymous_http"]=r.status_code;summary["stage15_anonymous_signature"]=next(r.iter_content(4)).hex()
except Exception as e:summary["stage15_anonymous_error"]=str(e)
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print("RESULT",json.dumps(summary,ensure_ascii=False),flush=True)
