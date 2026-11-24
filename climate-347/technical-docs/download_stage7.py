import csv,io,zipfile,re,hashlib,json,pathlib,concurrent.futures as cf,subprocess,collections
import requests,pymupdf as fitz
root=pathlib.Path("/tmp/climate347v7");root.mkdir(exist_ok=True)
old=root/"Climate_347_PDF_stage6_review.zip"
subprocess.run(["gh","release","download","climate-347-pdf-stage6-45501618003","-p",old.name,"-D",str(root)],check=True)
assert hashlib.file_digest(old.open("rb"),"sha256").hexdigest()=="8a45a99ed3df8766e548a2abdd4b4fecc90399b14012b3425da27649fe7e7681"
def readcsv(raw):return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
with zipfile.ZipFile(old) as z:
 assert z.testzip() is None
 cov=readcsv(z.read("REPORTS/coverage_347.csv"))
 evidence=readcsv(z.read("REPORTS/model_evidence.csv"))
 docs=readcsv(z.read("REPORTS/document_manifest.csv"))
 entries={n:z.read(n) for n in z.namelist() if not n.startswith("REPORTS/")}
 reports={n:z.read(n) for n in z.namelist() if n.startswith("REPORTS/")}
assert len(cov)==347
inv={(r["brand"],r["model"]):r for r in cov}
assert hashlib.sha256("\n".join(sorted(b+"\t"+m for b,m in inv)).encode()).hexdigest()=="b11a94ae13d7ee8d9563e23ec22c51136e968abdbe0d8261f74ded25e3c30343"
sources=[
("Midea","MIH_DL_engineering_data.pdf","technical",["https://www.c-o-k.ru/library/instructions/midea/kondicionery-promyshlennye/38668/142835.pdf?download="]),
("Midea","MIH_T1_installation_and_user_manual.pdf","manual",["https://midea-pro.ru/library/midea-mih-t1hn18-instruktsiya.pdf","https://iclim.ru/library/midea-mih-t1hn18-instruktsiya.pdf","https://nn.iclim.ru/library/midea-mih-t1hn18-instruktsiya.pdf"]),
("Midea","V8i_ULTRA_installation_and_user_manual.pdf","manual",["https://midea-pro.ru/library/midea-v8-i-ultra-instruktsiya.pdf","https://iclim.ru/library/midea-v8-i-ultra-instruktsiya.pdf","https://nn.iclim.ru/library/midea-v8-i-ultra-instruktsiya.pdf"]),
("Midea","Daichi_regional_catalog_27456.pdf","catalog",["https://daichi.business/support/documents/download.php?ID=27456"]),
("Midea","V8_PRO_technical_data_ES.pdf","technical",["https://www.midea.es/wp-content/uploads/_pda/2023/08/230801_EDB_M_EXC_V8-PRO-ES.pdf"])]
def fetch(x):
 b,n,k,urls=x; errors=[]
 for u in urls:
  try:
   with requests.get(u,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf,*/*"},timeout=(10,25),stream=True) as r:
    r.raise_for_status();parts=[];size=0
    for ch in r.iter_content(1024*1024):
     if not ch:continue
     if not parts and not ch.lstrip().startswith(b"%PDF-"):raise ValueError("not PDF")
     size+=len(ch)
     if size>150*1024*1024:raise ValueError("size cap")
     parts.append(ch)
   raw=b"".join(parts)
   with fitz.open(stream=raw,filetype="pdf") as p:
    assert len(p);p[0].get_pixmap(matrix=fitz.Matrix(.3,.3))
   return x,u,raw,""
  except Exception as e:errors.append(str(e)[:160])
 return x,"",None," | ".join(errors)
def hit(m,t):
 m=re.sub(r"\s+","",m)
 pat=r"(?<![A-Za-z0-9])"+r"\s*".join(re.escape(c) if c!="-" else r"[-‐‑–−]" for c in m)+r"(?![A-Za-z0-9_/(‐‑–−-])"
 return bool(re.search(pat,t,re.I))
hashes={hashlib.sha256(v).hexdigest():n for n,v in entries.items() if n.startswith(("ORIGINAL_PDF/","QUARANTINE/"))}
attempts=[];newpaths=[];fresh=[]
with cf.ThreadPoolExecutor(max_workers=5) as ex:
 for x,u,raw,err in ex.map(fetch,sources):
  b,n,k,urls=x;p=""
  if raw:
   sha=hashlib.sha256(raw).hexdigest();p=hashes.get(sha)
   if not p:
    p="ORIGINAL_PDF/"+b+"/"+n;entries[p]=raw;hashes[sha]=p;newpaths.append(p)
    with fitz.open(stream=raw,filetype="pdf") as pdf:pages=[pg.get_text() for pg in pdf]
    count=0
    for (brand,m),r in inv.items():
     if brand!=b or not r["base_url"]:continue
     pp=[i+1 for i,t in enumerate(pages) if hit(m,t)]
     if pp:
      rec=dict(brand=b,model=m,document_kind=k,archive_path=p,source=u,sha256=sha,pages=" ".join(map(str,pp)),status="EXACT_TEXT_REVIEW_REQUIRED")
      evidence.append(rec);fresh.append(rec);count+=1
    docs.append(dict(brand=b,archive_path=p,kind=k,source=u,bytes=len(raw),sha256=sha,pages=len(pages),text_chars=sum(map(len,pages)),models_exact=count))
  attempts.append(dict(brand=b,filename=n,source=u or urls[0],archive_path=p,bytes=len(raw) if raw else 0,error=err))
  print("FETCH",n,len(raw) if raw else 0,err[:120],flush=True)
def original(s):
 matches=[p for p in entries if p.startswith("ORIGINAL_PDF/") and p.endswith("/"+s)]
 assert len(matches)==1,(s,matches)
 return matches[0]
passport=original("IGC_IMBR_passport.pdf")
decl=original("IGC_IRFT_Q_declaration.pdf")
# Visually inspected stage-6 rendered originals: cover explicitly uses IMBR(G)-C(H).
# Do not silently treat printed 1230 as 1320.
visual=[]
def visualrec(m,p,k,page,note):
 d=next(d for d in docs if d["archive_path"]==p)
 return dict(brand="IGC",model=m,document_kind=k,archive_path=p,source=d["source"],sha256=hashlib.sha256(entries[p]).hexdigest(),pages=page,status="VISUAL_SCOPE_CONFIRMED",notes=note)
for (b,m),r in inv.items():
 if b!="IGC":continue
 if re.fullmatch(r"IMBRG?-[CH](220|330|440|550|660|770|880|990|1100|1210)ANB",m):
  visual.append(visualrec(m,passport,"combined_manual_passport","1","Title page lists IMBR(G)-C(H) and exact capacity index; 1320 excluded due 1230 printed on cover."))
 if re.fullmatch(r"IRFT-\d{3}[HC]A/NB-Q",m):
  # All 17 inventory codes visually enumerated in signed declaration, pages 1-2.
  visual.append(visualrec(m,decl,"declaration","1,2","Exact code on declaration page 1; signed registration page 2; not a technical manual."))
assert collections.Counter(r["document_kind"] for r in visual)=={"combined_manual_passport":24,"declaration":17}
# Review pages for 1320 and potentially mismatched fan coil generations.
for i in [10,11,12,13,14,35,36,37,38]:
 with fitz.open(stream=entries[passport],filetype="pdf") as pdf:
  if i<len(pdf):
   pix=pdf[i].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False)
   entries["REVIEW_SCAN_IMAGES/IMBR_table_p"+str(i+1)+".jpg"]=pix.tobytes("jpeg",jpg_quality=88)
# Include engineering data ONLY if actual downloaded PDF title and exact cover model match.
dl=[p for p in newpaths if p.endswith("/MIH_DL_engineering_data.pdf")]
if dl:
 p=dl[0]
 with fitz.open(stream=entries[p],filetype="pdf") as pdf:
  cover=pdf[0].get_text()
  assert "Engineering Data" in cover
  for (b,m),r in inv.items():
   if b=="Midea" and re.fullmatch(r"MIH\d+DLHN18",m) and hit(m,cover):
    d=next(d for d in docs if d["archive_path"]==p)
    visual.append(dict(brand=b,model=m,document_kind="technical",archive_path=p,source=d["source"],sha256=d["sha256"],pages="1",status="VISUAL_SCOPE_CONFIRMED",notes="Engineering Data title page visually checked via source PDF screenshot; exact cover code rechecked in downloaded bytes."))
# Form real partial upload package with literal user paths and exact HTML template.
approved=collections.defaultdict(list);upload={};manifest=[]
for v in visual:
 r=inv[(v["brand"],v["model"])]
 kind=v["document_kind"]
 fname,label={"combined_manual_passport":("IGC_IMBR_IMBRG_R_installation_and_user_manual.pdf","Инструкция к товару"),"declaration":("IGC_IRFT_Q_declaration.pdf","Декларация соответствия"),"technical":("MIH_DL_engineering_data.pdf","Технические данные")}[kind]
 base=r["base_url"];assert base.startswith("https://docs.proclimate5.ru/") and base.endswith("/2026/")
 target=base+fname
 zpath="UPLOAD_TO_SELECTEL/"+target.removeprefix("https://docs.proclimate5.ru/")
 raw=entries[v["archive_path"]];assert raw.startswith(b"%PDF-")
 if zpath in upload:assert upload[zpath]==raw
 upload[zpath]=raw
 html='<p>\n <a href="'+target+'" target="_blank"><img src="/images/icons/pdf-icon2.jpg" alt="" style="height:41px; width:40px"></a> <a href="'+target+'" target="_blank">'+label+'</a>\n</p>'
 manifest.append(dict(brand=v["brand"],model=v["model"],filename=fname,document_kind=kind,label_ru=label,base_url=base,full_url=target,html=html,archive_path=zpath,sha256=v["sha256"],pages=v["pages"],status="PREPARED_NOT_UPLOADED"))
 approved[(v["brand"],v["model"])].append(v)
byexact=collections.defaultdict(list)
for e in evidence:byexact[(e["brand"],e["model"])].append(e)
for r in cov:
 key=(r["brand"],r["model"])
 tech=[e for e in byexact[key] if e["document_kind"]!="declaration"]
 vtech=[v for v in approved[key] if v["document_kind"]!="declaration"]
 vdec=[v for v in approved[key] if v["document_kind"]=="declaration"]
 r["visual_confirmed_technical_count"]=len(vtech);r["visual_confirmed_declaration_count"]=len(vdec)
 r["technical_pdf_count"]=len(tech)+sum(not any(e["archive_path"]==v["archive_path"] for e in tech) for v in vtech)
 r["declaration_count"]=max(int(r["declaration_count"]),len(vdec))
 r["files"]=" | ".join(dict.fromkeys([e["archive_path"] for e in byexact[key]]+[v["archive_path"] for v in approved[key]]))
 if vtech:r["status"]="VISUAL_TECH_SCOPE_CONFIRMED"
 elif tech:r["status"]="EXACT_TEXT_REVIEW_REQUIRED"
 elif vdec:r["status"]="VISUAL_DECLARATION_ONLY"
def csvbytes(rows):
 s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rows[0]),extrasaction="ignore");w.writeheader();w.writerows(rows);return s.getvalue().encode("utf-8-sig")
newreports={"coverage_347.csv":cov,"model_evidence.csv":evidence,"document_manifest.csv":docs,"stage7_download_attempts.csv":attempts,"visual_scope_evidence.csv":visual,"partial_selectel_manifest.csv":manifest}
for n,rows in newreports.items():
 data=csvbytes(rows);reports["REPORTS/"+n]=data;(root/n).write_bytes(data)
stats=collections.Counter(r["brand"] for r in cov if int(r["technical_pdf_count"])>0)
summary=dict(catalog_total=347,source_archive_sha256="8a45a99ed3df8766e548a2abdd4b4fecc90399b14012b3425da27649fe7e7681",original_pdfs_including_quarantine=sum(p.endswith(".pdf") and p.startswith(("ORIGINAL_PDF/","QUARANTINE/")) for p in entries),new_unique_originals=len(newpaths),new_successful_downloads=sum(bool(x["archive_path"]) for x in attempts),models_with_technical_scope_evidence=sum(stats.values()),by_brand=dict(stats),visual_scope_confirmed_technical=sum(bool(r["visual_confirmed_technical_count"]) for r in cov),visual_declaration_only=sum(r["status"]=="VISUAL_DECLARATION_ONLY" for r in cov),partial_upload_pdfs=len(upload),partial_upload_models=len(manifest),status_counts=dict(collections.Counter(r["status"] for r in cov)),note="Partial upload preparation only, not all available docs for models, no Selectel upload; original Excel unchanged. All other exact text matches still require document applicability review.")
reports["REPORTS/summary.json"]=json.dumps(summary,ensure_ascii=False,indent=2).encode()
out=root/"Climate_347_PDF_stage7_review.zip";part=root/"Climate_347_stage7_partial_Selectel.zip"
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p,v in {**entries,**reports,**upload}.items():z.writestr(p,v)
with zipfile.ZipFile(part,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p,v in upload.items():z.writestr(p,v)
 z.writestr("REPORTS/partial_selectel_manifest.csv",csvbytes(manifest))
 z.writestr("REPORTS/visual_scope_evidence.csv",csvbytes(visual))
 z.writestr("README.txt","Partial package. Upload only contents of UPLOAD_TO_SELECTEL; links are planned, not checked live. No final completeness claim. The original workbook was not modified.")
for p in [out,part]:
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
summary["archive_sha256"]=hashlib.file_digest(out.open("rb"),"sha256").hexdigest()
summary["partial_archive_sha256"]=hashlib.file_digest(part.open("rb"),"sha256").hexdigest()
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
previewdir=pathlib.Path("climate-347/technical-docs/stage7-scan-previews");previewdir.mkdir(exist_ok=True)
for p,v in entries.items():
 if p.startswith("REVIEW_SCAN_IMAGES/IMBR_table_"):(previewdir/pathlib.Path(p).name).write_bytes(v)
print("RESULT",json.dumps(summary,ensure_ascii=False),flush=True)
