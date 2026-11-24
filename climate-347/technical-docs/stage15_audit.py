import csv,io,zipfile,re,hashlib,json,pathlib,subprocess,collections,requests
import pymupdf as fitz
root=pathlib.Path("/tmp/climate347v15");root.mkdir(exist_ok=True)
tag="climate-347-pdf-stage9-45505224491"
def download(name,sha,tag=tag):
 p=root/name;subprocess.run(["gh","release","download",tag,"-p",name,"-D",str(root)],check=True)
 assert hashlib.file_digest(p.open("rb"),"sha256").hexdigest()==sha
 return p
review=download("Climate_347_stage9_review.zip","4add40ccdd6ca5296fc7268c08d5767fd0971595ee461d84a1044905cc91888b")
part=download("Climate_347_stage14_partial_Selectel.zip","5a0879e34c5c3e0b0c307e26b979bc3aec601e792d3488a6e4f79bc433162f47","climate-347-pdf-stage14-45508922665")
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
assert len(inv)==347 and len(ms)==318 and len(upload)==31
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
# Three Bosch original covers inspected in stage 15; exact scope and unchanged bytes.
rules=[
("MDCI_8_18_installation_6720862924_DE.pdf","MDCI_8_18_installation_manual_DE.pdf","Инструкция по монтажу (DE)","installation",r"MDCI\s*(?:12-1|14-1|16-1|12-3|14-3|16-3|18-3)",7,"12bc37bdd728bdabd7639ef6502019550ee44168eba712e15782f9100728b2ef"),
("MDCI_8_18_user_6720862925_DE.pdf","MDCI_8_18_user_manual_DE.pdf","Инструкция к товару (DE)","manual",r"MDCI\s*(?:12-1|14-1|16-1|12-3|14-3|16-3|18-3)",7,"ddee035274d6e7d107924890da4e5805a525a397d57f90338b0624b3dee5252a"),
("MDCI_20_26_user_6720862927_DE_candidate.pdf","MDCI_20_26_user_manual_DE.pdf","Инструкция к товару (DE)","manual",r"MDCI\s*(22|26)-3",2,"82d9676e2daba1a5882677f65351ca9c88a01de8f8da2fbe54007270770e23a9")]
for src,name,label,kind,rx,n,sha in rules:
 source="CANDIDATE_PDF/Bosch/"+src
 try:
  raw=originals[source];assert hashlib.sha256(raw).hexdigest()==sha
  found=[r for r in inv if r["brand"]=="Bosch" and re.fullmatch(rx,r["model"]) and r["base_url"]]
  assert len(found)==n,(len(found),n)
  with fitz.open(stream=raw,filetype="pdf") as d:
   t=d[0].get_text()
   assert all(exact(r["model"],t) for r in found)
   for pg in d:pg.get_pixmap(matrix=fitz.Matrix(.15,.15),alpha=False)
  add=[]
  for r in found:
   u=r["base_url"]+name;dest="UPLOAD_TO_SELECTEL/"+u.removeprefix("https://docs.proclimate5.ru/")
   assert not any(m["brand"]==r["brand"] and m["model"]==r["model"] and (m["full_url"]==u or m["sha256"]==sha) for m in ms)
   add.append(dict(brand=r["brand"],model=r["model"],filename=name,document_kind=kind,label_ru=label,base_url=r["base_url"],full_url=u,html=html(u,label),archive_path=dest,sha256=sha,pages="1",status="PREPARED_NOT_UPLOADED"))
  for m in add:upload[m["archive_path"]]=raw
  ms.extend(add);new.extend(add);checks.append(dict(source=source,result="PASS",detail=f"{n} exact model assignments; unchanged Bosch universal manual."))
 except Exception as e:checks.append(dict(source=source,result="REJECTED",detail=repr(e)))
# Winter evidence: same manufacturer catalogue, exact base model table and separate series option page.
# Do not put base-only files in Selectel or count as winter technical coverage without review.
p="ORIGINAL_PDF/Midea/Daichi_regional_catalog_27456.pdf"
raw=originals[p]
families=[("V8M",r"MV8M-.*",91,range(90,94)),("V8S",r"MV8S-.*",95,range(94,101)),("V8Si",r"MV8Si-.*",95,range(94,101)),("V8_PRO",r"MV8-.*",103,range(102,113)),("V8i_PRO",r"MV8i-.*\(PRO\).*",103,range(102,113)),("VC_MAX",r"MVC-M.*",117,range(116,124))]
winter=[]
with fitz.open(stream=raw,filetype="pdf") as d:
 for family,rx,option,window in families:
  rows=[r for r in inv if r["brand"]=="Midea" and r["model"].endswith("/-40") and re.fullmatch(rx,r["model"])]
  table=set()
  for r in rows:
   base=r["model"][:-4]
   hit=[i for i in window if i<=len(d) and exact(base,d[i-1].get_text())]
   table.update(hit)
   winter.append(dict(brand="Midea",model=r["model"],base_model=base,series=family,source=p,option_page=option,exact_base_pages=" ".join(map(str,hit)),status="REVIEW_REQUIRED_BASE_TABLE_AND_OPTION" if hit else "NO_EXACT_BASE_TABLE_IN_WINDOW"))
  for i in sorted(table|{option}):
   previews[f"{family}_catalog_p{i}.jpg"]=d[i-1].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).tobytes("jpeg",jpg_quality=88)
print("WINTER_EVIDENCE",len(winter),sum(bool(r["exact_base_pages"]) for r in winter),flush=True)
# Search evidence: no new IGC exact technical manuals in public search. Never use declarations.
attempts=[dict(filename="IGC_IRFT_Q_and_T22",url="https://igc-aircon.com/product/kryshnye_konditsionery_ruftop_/",bytes=0,sha256="",status="NO_EXACT_TECH_PDF_FOUND",cover_text="",error="Public product and library search yielded product descriptions only; certificates excluded."),dict(filename="Kentatsu_KTRB",url="https://kentatsu.group/documents/",bytes=0,sha256="",status="NO_EXACT_MANUAL_FOUND",cover_text="",error="KTRV/KTRA/KTRX/KTRZ are different generations."),dict(filename="Midea_winter_kit",url="https://daichi.business/support/documents/download.php?ID=27456",bytes=0,sha256="",status="SERIES_OPTION_CONFIRMED_ONLY",cover_text="",error="Separate winter-kit manual not located; base model table candidates recorded for visual review.")]
previewdir=pathlib.Path("climate-347/technical-docs/stage15-previews");previewdir.mkdir(exist_ok=True)
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
summary=dict(winter_evidence_rows=len(winter),winter_exact_base_rows=sum(bool(r['exact_base_pages']) for r in winter),policy="UNIVERSAL_TECH_ONLY_NO_CERTIFICATES_OR_DECLARATIONS",total_models=347,prepared_models=len(by),technical_models=sum(r["technical_pdf_count"]>0 for r in coverage),substantive_technical_models=sum(r["substantive_technical_count"]>0 for r in coverage),declaration_only=sum(r["status"]=="DECLARATION_ONLY" for r in coverage),no_prepared_document=347-len(by),assignments=len(ms),prepared_files=len(upload),new_assignments=len(new),new_originals=len(newpdf),status_counts=dict(collections.Counter(r["status"] for r in coverage)),by_brand={b:dict(c) for b,c in brands.items()},checks=checks,attempts=attempts,selectel_uploaded=False,workbook_changed=False)
assert len(by)==len(htmlrows) and sum(summary["status_counts"].values())==347
files={"coverage_347.csv":data(coverage),"remaining.csv":data(remaining),"html_by_model.csv":data(htmlrows),"partial_selectel_manifest.csv":data(ms),"download_attempts.csv":data(attempts),"winter_scope_review.csv":data(winter)}
for n,v in files.items():(root/n).write_bytes(v)
for file,content in [("Climate_347_stage15_partial_Selectel.zip",upload),("Climate_347_stage15_delta_review.zip",{**newpdf,**{"PREVIEWS/"+n:v for n,v in previews.items()}})]:
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
u="https://github.com/kubenkoi97-cmyk/work-files-public/releases/download/climate-347-pdf-stage14-45508922665/Climate_347_stage14_partial_Selectel.zip"
try:
 with requests.get(u,headers={"Range":"bytes=0-3"},stream=True,timeout=(8,15)) as r:
  summary["stage14_anonymous_http"]=r.status_code;summary["stage14_anonymous_signature"]=next(r.iter_content(4)).hex()
except Exception as e:summary["stage14_anonymous_error"]=str(e)
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print("RESULT",json.dumps(summary,ensure_ascii=False),flush=True)
