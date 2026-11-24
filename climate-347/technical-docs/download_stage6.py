import csv,io,zipfile,re,hashlib,json,pathlib,concurrent.futures as cf,subprocess,collections
import requests,pymupdf as fitz
root=pathlib.Path("/tmp/climate347v6");root.mkdir(exist_ok=True)
old=root/"Climate_347_PDF_stage5_review.zip"
subprocess.run(["gh","release","download","climate-347-pdf-stage5-45499456111","-p",old.name,"-D",str(root)],check=True)
assert hashlib.file_digest(old.open("rb"),"sha256").hexdigest()=="b54298d7f8eff5088e51b0b5ed394342be93af59abd8a05c1d52b61762724563"
def readcsv(raw):return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
with zipfile.ZipFile(old) as z:
 assert z.testzip() is None
 coverage=readcsv(z.read("REPORTS/coverage_347.csv"))
 olddocs=readcsv(z.read("REPORTS/document_manifest.csv"))
 oldhits=readcsv(z.read("REPORTS/model_evidence.csv"))
 originals={n:z.read(n) for n in z.namelist() if n.startswith("ORIGINAL_PDF/") and n.endswith(".pdf")}
 excerpts={n:z.read(n) for n in z.namelist() if n.startswith("REVIEW_EXCERPTS/") and n.endswith(".pdf")}
assert len(coverage)==347 and len(originals)==33
inv={(r["brand"],r["model"]):r for r in coverage}
digest=hashlib.sha256("\n".join(sorted(b+"\t"+m for b,m in inv)).encode()).hexdigest()
assert digest=="b11a94ae13d7ee8d9563e23ec22c51136e968abdbe0d8261f74ded25e3c30343",digest
sources=[
("Midea","V8M_installation_and_user_manual_2025.pdf","manual",["https://air-midea.com/upload/iblock/8d7/dtg11bg6kb6x9x6d0bhza9vr45r33xcq.pdf","https://air-midea.com/support/marketing/download/8463/"]),
("Midea","V8M_engineering_data.pdf","technical",["https://www.c-o-k.ru/library/instructions/midea/kondicionery-promyshlennye/38659/142823.pdf?download="]),
("Midea","V8S_service_manual.pdf","service",["https://www.c-o-k.ru/library/instructions/midea/kondicionery-promyshlennye/38660/142824.pdf?download="]),
("Midea","V8S_installation_and_user_manual.pdf","manual",["https://air-midea.com/upload/iblock/33e/1w6uygpjui78setcdg7gv4yzdfi7tfey.pdf","https://www.c-o-k.ru/library/instructions/midea/kondicionery-promyshlennye/38661/142825.pdf?download="]),
("Midea","V8_PRO_and_V8i_PRO_catalog_pages.pdf","catalog",["https://onokom.ru/dok/midea/2024/catalog/2024-catalog-v8i-pro.pdf"]),
("Midea","Daichi_Midea_regional_catalog.pdf","catalog",["https://daichi.business/support/documents/download.php?ID=26398"]),
("Midea","V8M_manufacturer_catalog.pdf","catalog",["https://www.midea.com/content/dam/midea-aem/id/PD-Midea-V8-Mini-VRF-R410A-catalogue-2024-12-25-V3-1-.pdf"]),
("Midea","V8_PRO_manufacturer_catalog.pdf","catalog",["https://midea.kg/storage/2024/04/16/a35972c8cac20741523eca7738bc87a7444c5479.pdf"])]
def fetch(x):
 b,n,k,urls=x; errors=[]
 for u in urls:
  try:
   with requests.get(u,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf,*/*"},timeout=(10,30),stream=True) as r:
    r.raise_for_status();parts=[];size=0
    for c in r.iter_content(1024*1024):
     if not c:continue
     if not parts and not c.lstrip().startswith(b"%PDF-"):raise ValueError("not PDF")
     size+=len(c)
     if size>150*1024*1024:raise ValueError("size cap")
     parts.append(c)
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
hashes={hashlib.sha256(v).hexdigest():k for k,v in originals.items()}
docs={d["archive_path"]:d for d in olddocs}
attempts=[]
with cf.ThreadPoolExecutor(max_workers=8) as ex:
 for x,u,raw,error in ex.map(fetch,sources):
  b,n,k,urls=x;p=""
  if raw:
   sha=hashlib.sha256(raw).hexdigest();p=hashes.get(sha)
   if not p:
    p="ORIGINAL_PDF/"+b+"/"+n; originals[p]=raw;hashes[sha]=p
    docs[p]=dict(brand=b,archive_path=p,kind=k,source=u,bytes=len(raw),sha256=sha,pages=0,text_chars=0,models_exact=0)
  attempts.append(dict(brand=b,filename=n,source=u or urls[0],archive_path=p,bytes=len(raw) if raw else 0,error=error))
  print("FETCH",n,len(raw) if raw else 0,error[:120],flush=True)
# Separate actual catalogue matches from base-model-only documentation for winter suffix.
# A catalogue that lists -40 as a series option is not proof of exact installed kit.
base=[]; exact=[]; options=[]; previews={}; scan_diag=[]
for p,raw in originals.items():
 b=p.split("/")[1];d=docs[p];kind=d["kind"]
 excluded="MDCI_20_26_3_installation_manual_KK" in p
 if excluded: d["kind"]="QUARANTINE_WRONG_DOCUMENT"
 with fitz.open(stream=raw,filetype="pdf") as pdf:
  pages=[x.get_text() for x in pdf]
  d["pages"]=len(pdf);d["text_chars"]=sum(len(x) for x in pages);d["models_exact"]=0
  if excluded:continue
  if b=="IGC" and ("IMBR" in p or "IRFT" in p):
   scan_diag.append(dict(file=p,pages=len(pdf),chars_per_page=" ".join(str(len(t)) for t in pages),first_text=" ".join(pages[:3])[:1500]))
   for i in range(min(4,len(pdf))):
    pix=pdf[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False)
    name=pathlib.Path(p).stem+"_p"+str(i+1)+".jpg"
    previews[name]=pix.tobytes("jpeg",jpg_quality=83)
  if b=="Midea" and kind=="catalog":
   for i,t in enumerate(pages):
    if re.search(r"низкотемпературн\w*\s+комплект",t,re.I) and re.search(r"[-−–]\s*40",t):
     families=re.findall(r"\b(?:V8M|V8Si|V8S|V8i\s*PRO|V8\s*PRO|VC\s*MAX)\b",t,re.I)
     if families:options.append(dict(archive_path=p,source=d["source"],page=i+1,families=" | ".join(sorted(set(families))),status="OPTION_EVIDENCE_REVIEW_REQUIRED"))
  for (brand,m),r in inv.items():
   if b!=brand or not r["base_url"]:continue
   pp=[i+1 for i,t in enumerate(pages) if hit(m,t)]
   if pp:
    exact.append(dict(brand=b,model=m,document_kind=kind,archive_path=p,source=d["source"],sha256=d["sha256"],pages=" ".join(map(str,pp)),status="EXACT_TEXT_REVIEW_REQUIRED"));d["models_exact"]+=1
   if m.endswith("/-40"):
    pp2=[i+1 for i,t in enumerate(pages) if hit(m[:-4],t)]
    if pp2:
     base.append(dict(brand=b,model=m,base_model=m[:-4],document_kind=kind,archive_path=p,source=d["source"],pages=" ".join(map(str,pp2)),status="BASE_MODEL_ONLY_NOT_WINTER_APPROVAL"))
# Keep all original evidence including failed and previously created candidates, but exclude quarantined links.
byexact=collections.defaultdict(list);bybase=collections.defaultdict(list)
for h in exact:byexact[(h["brand"],h["model"])].append(h)
for h in base:bybase[(h["brand"],h["model"])].append(h)
for r in coverage:
 key=(r["brand"],r["model"]);e=byexact[key];tech=[h for h in e if h["document_kind"]!="declaration"];dec=[h for h in e if h["document_kind"]=="declaration"]
 r["technical_pdf_count"]=len(tech);r["declaration_count"]=len(dec);r["base_only_pdf_count"]=len(bybase[key]);r["files"]=" | ".join(h["archive_path"] for h in e)
 r["status"]="BLOCKED_NO_BASE_URL" if not r["base_url"] else "EXACT_TEXT_REVIEW_REQUIRED" if tech else "BASE_MODEL_ONLY_NOT_WINTER_APPROVAL" if bybase[key] else "DECLARATION_ONLY" if dec else "NO_EXACT_TECH_PDF"
def writecsv(name,rows):
 p=root/name
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  if rows:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
  else:f.write("no_records\n")
 return p
reports=[writecsv("coverage_347.csv",coverage),writecsv("model_evidence.csv",exact),writecsv("winter_base_evidence.csv",base),writecsv("winter_option_pages.csv",options),writecsv("document_manifest.csv",list(docs.values())),writecsv("download_attempts.csv",attempts),writecsv("scan_diagnostics.csv",scan_diag)]
counts=collections.Counter(r["status"] for r in coverage)
bybrand=collections.Counter(r["brand"] for r in coverage if r["technical_pdf_count"])
summary=dict(catalog_total=347,inventory_sha256=digest,original_pdfs=len(originals),new_original_pdfs=len(originals)-33,successful_new_downloads=sum(bool(a["archive_path"]) for a in attempts),exact_technical_text_models=sum(bybrand.values()),by_brand=dict(bybrand),status_counts=dict(counts),winter_base_evidence_models=len(bybase),winter_option_pages=len(options),review_excerpts=len(excerpts),ready_for_selectel=0,warning="All matches require applicability and visual review. Base codes do not establish winter configuration. Wrong Bosch instruction quarantined. No Selectel upload or Excel edits.")
outpath=root/"Climate_347_PDF_stage6_review.zip"
with zipfile.ZipFile(outpath,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p,v in originals.items():
  if docs[p]["kind"]=="QUARANTINE_WRONG_DOCUMENT":z.writestr(p.replace("ORIGINAL_PDF/","QUARANTINE/"),v)
  else:z.writestr(p,v)
 for p,v in excerpts.items():z.writestr(p,v)
 for p,v in previews.items():z.writestr("REVIEW_SCAN_IMAGES/"+p,v)
 for p in reports:z.write(p,"REPORTS/"+p.name)
 z.writestr("REPORTS/summary.json",json.dumps(summary,ensure_ascii=False,indent=2))
with zipfile.ZipFile(outpath) as z:assert z.testzip() is None
summary["archive_sha256"]=hashlib.file_digest(outpath.open("rb"),"sha256").hexdigest()
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
# Small public-source page previews for visual inspection in repository (not final upload).
previewdir=pathlib.Path("climate-347/technical-docs/stage6-scan-previews");previewdir.mkdir(exist_ok=True)
for n,v in previews.items():(previewdir/n).write_bytes(v)
print("RESULT",json.dumps(summary),flush=True)
for r in coverage:
 if r["status"] not in ("EXACT_TEXT_REVIEW_REQUIRED",):print("REMAINING",r["brand"],r["model"],r["status"],flush=True)
