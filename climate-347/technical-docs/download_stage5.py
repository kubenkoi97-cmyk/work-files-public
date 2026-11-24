import csv,io,zipfile,re,hashlib,json,pathlib,concurrent.futures as cf,subprocess,collections
import requests,fitz
root=pathlib.Path("/tmp/climate347v5");root.mkdir(exist_ok=True)
old=root/"Climate_347_PDF_stage4_partial.zip"
subprocess.run(["gh","release","download","climate-347-pdf-stage4-45498327706","-p",old.name,"-D",str(root)],check=True)
assert hashlib.sha256(old.read_bytes()).hexdigest()=="d341a6192d60b071620c43440c08feecaf2a9983b5e432bd24323b2ebb191533"
def readcsv(raw):return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
with zipfile.ZipFile(old) as z:
 assert z.testzip() is None
 previous=readcsv(z.read("REPORTS/model_evidence.csv"))
 olddocs=readcsv(z.read("REPORTS/document_manifest.csv"))
 originals={n:z.read(n) for n in z.namelist() if n.startswith("ORIGINAL_PDF/") and n.endswith(".pdf")}
assert len(originals)==17
inventory={}
for r in previous:
 if r["model"]=="IRFT-035CA/NB-Q":continue
 inventory[(r["brand"],r["model"])]=r["target_folder"]
for m in ["IWF-X"+str(n)+"K22W-A" for n in [200,300,400,500,600]]:inventory[("IGC",m)]="fankoyly/nastennye_fankoyly/nastennye_fankoyly_IGC/2026/"
for m in ["IWF-Q1700CAQ4T22","IWF-Q1700CAQ4T44"]:inventory[("IGC",m)]="fankoyly/kassetnye_fankoyly/kassetnye_fankoyly_IGC/2026/"
inventory[("IGC","IMS-EX330NB(7)")]=""
inventory[("Midea","SMK-D140HHN1-3")]=""
assert len(inventory)==347, len(inventory)
assert collections.Counter(b for b,m in inventory)=={"IGC":51,"Midea":178,"Daikin":24,"Bosch":11,"Kentatsu":83}
# New and alternate originals; blocked categories stay outside upload processing.
sources=[
("Midea","MIH_FS_FL_manual.pdf","manual",["https://midea-pro.ru/library/midea-mih252-560fshn18-mih252-560flhn18-instruktsiya.pdf?v=5409f04e973f5167e28117dee24b06228a72cacf73bbec319ef806585a4226ea","https://midea-pro.ru/library/midea-mih252-560fshn18-mih252-560flhn18-instruktsiya.pdf"]),
("Midea","VC_MAX_catalog.pdf","catalog",["https://onokom.ru/dok/midea/2024/catalog/2024-catalog-vcmax.pdf"]),
("Midea","ATOM_B_catalog.pdf","catalog",["https://video.abokpress.keenetic.pro/MyWeb/video/work/mini-VRF_Midea_atom.pdf"]),
("Midea","ATOM_B_catalog_2022.pdf","catalog",["https://www.s-c-u.ru/wp-content/uploads/2024/07/m3_2022_291122_small.pdf","https://pkholod.ru/upload/iblock/ba4/8zpqxqmazom1ls00tl228x5s9fqy12p1/M3_2022_small.pdf"]),
("Bosch","Climate_5000_VRF_catalog_2021.pdf","catalog",["https://www.bosch-homecomfort.com/ke/media/country_pool/pdfs/catalogues/vrf_2021_en.pdf"]),
("Bosch","MDCI_8_16_1_installation_manual_KK.pdf","installation",["https://bosch-kz-ru.boschhc-documents.com/download/pdf/file/6720844634"]),
("Bosch","MDCI_20_26_3_installation_manual_KK.pdf","installation",["https://bosch-kz-ru.boschhc-documents.com/download/pdf/file/6720844650"]),
("Bosch","MDCI_26_3_datasheet.pdf","datasheet",["https://www.heiz24.de/mediafiles/pdf/mdci_26-3.pdf"]),
("IGC","IWF_X_K22W_A_passport.pdf","passport",["https://igc.com.ru/library/igc-iwf-x-k22w-a-pasport.pdf?v=6526168b3d2e3a200e321b83db65d1bd884457f13fca5c5544b28fef93eb2aa1","https://igc.com.ru/library/igc-iwf-x-k22w-a-pasport.pdf"]),
("IGC","IWF_Q_CAQ4T44_passport.pdf","passport",["https://igc.com.ru/library/igc-iwf-q-caq4t44-pasport.pdf?v=00919e08805e1e8be4da87a2d1f843e214739d9eaf17a0391e62ececb8878ae1"]),
("IGC","IWF_X_K22W_installation_manual_legacy.pdf","manual",["https://chel.igc-aircon.com/upload/iblock/c12/2szk2r8gmty1gxsd6zur1007jrepadnw.pdf"]),
("Daikin","Daikin_2021_catalog.pdf","catalog",["https://www.c-o-k.ru/library/catalogs/daikin/31163/112294.pdf"]),
("Daikin","Daikin_2022_catalog.pdf","catalog",["https://anapa.split-nastroi.ru/uploads/61fa68cf6698ddoc2021124809/62f3b401e4730.pdf"]),
("Daikin","Daikin_2025_catalog.pdf","catalog",["https://amonraenergy.eu/wp-content/uploads/2026/03/daikin_split_2025.pdf"]),
("Daikin","Daikin_split_catalog.pdf","catalog",["https://termo-pro.ru/wa-data/public/shop/products/79/07/779/attachments/Katalog-Daikin_split.pdf"]),
("Daikin","Daikin_2024_Daichi_catalog.pdf","catalog",["https://daichi.business/upload/iblock/fe1/D1_2024_DD24_02.01.01_260124.pdf"]),
("Midea","VC_MAX_installation_manual.pdf","manual",["https://24wvent.ru/documentation/3/MD23IU-046B-RU_27_11_23.pdf"]),
("Midea","ATOM_B_installation_manual.pdf","manual",["https://air-midea.com/upload/iblock/1f4/euymk0wyekscfn9tbt73pdjzeq12tfwu.pdf"]),
("Bosch","Bosch_VRF_RU_catalog.pdf","catalog",["https://www.c-o-k.ru/library/catalogs/bosch/33333/118605.pdf"]),
("Bosch","MDCI_technical_training.pdf","technical",["https://hvacgroup.ro/wp-content/uploads/2024/08/Mini-VRF_MDCI_Installation.pdf"]),
("Midea","Midea_2024_Daichi_catalog.pdf","catalog",["https://daichi.business/upload/iblock/32c/M2_2024_DM24_02.01.02_Small_260824.pdf"]),
]
def fetch(item):
 b,name,kind,urls=item;errors=[]
 for u in urls:
  try:
   with requests.get(u,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf,*/*"},timeout=(10,35),stream=True) as r:
    r.raise_for_status();parts=[];n=0
    for ch in r.iter_content(1024*1024):
     if not ch:continue
     if not parts and not ch.lstrip().startswith(b"%PDF-"):raise ValueError("not PDF")
     n+=len(ch)
     if n>150*1024*1024:raise ValueError("size cap")
     parts.append(ch)
   raw=b"".join(parts)
   with fitz.open(stream=raw,filetype="pdf") as pdf:
    assert len(pdf)>0
    pdf[0].get_pixmap(matrix=fitz.Matrix(.25,.25))
   return item,u,raw,""
  except Exception as e:errors.append(str(e)[:180])
 return item,"",None," | ".join(errors)
def match(model,text):
 m=re.sub(r"\s+","",model)
 # preserve explicit hyphens, parentheses, and suffixes; no cross-page stitching
 pat=r"(?<![A-Za-z0-9])"+r"\s*".join(re.escape(ch) if ch!="-" else r"[-‐‑–−]" for ch in m)+r"(?![A-Za-z0-9_/(‐‑–−-])"
 return bool(re.search(pat,text,re.I))
byhash={hashlib.sha256(v).hexdigest():k for k,v in originals.items()}
metadata={}
for d in olddocs:
 if d["archive_path"]:metadata.setdefault(d["archive_path"],[]).append(d["source"])
kinds={p:("declaration" if "declaration" in p else "catalog" if "catalog" in p else "technical") for p in originals}
attempts=[]
with cf.ThreadPoolExecutor(max_workers=10) as ex:
 for item,u,raw,err in ex.map(fetch,sources):
  b,name,kind,urls=item;path="";sha=""
  if raw:
   sha=hashlib.sha256(raw).hexdigest();path=byhash.get(sha)
   if not path:
    path="ORIGINAL_PDF/"+b+"/"+name
    if path in originals:path=path[:-4]+"_"+sha[:8]+".pdf"
    originals[path]=raw;byhash[sha]=path;kinds[path]=kind
   metadata.setdefault(path,[]).append(u)
  attempts.append(dict(brand=b,filename=name,source=u or urls[0],archive_path=path,bytes=len(raw) if raw else 0,sha256=sha,error=err))
  print("FETCH",b,name,len(raw) if raw else 0,err[:120],flush=True)
# Reaudit every PDF against the corrected 347 SKU inventory. Exact text is evidence, not final applicability.
matches=[]; docrows=[]; excerpts={}; bymodel=collections.defaultdict(list)
for path,raw in originals.items():
 brand=path.split("/")[1];kind=kinds[path]
 sha=hashlib.sha256(raw).hexdigest()
 with fitz.open(stream=raw,filetype="pdf") as pdf:
  pages=[p.get_text() for p in pdf]
  # Render original page for basic integrity; human visual review remains pending.
  pdf[0].get_pixmap(matrix=fitz.Matrix(.3,.3))
  hits={}
  for (b,m),folder in inventory.items():
   if b!=brand or not folder:continue
   pp=[i for i,t in enumerate(pages) if match(m,t)]
   if pp:
    hits[m]=pp
    rec=dict(brand=b,model=m,document_kind=kind,archive_path=path,source=" | ".join(dict.fromkeys(metadata.get(path,[]))),sha256=sha,pages=" ".join(str(i+1) for i in pp),status="EXACT_TEXT_REVIEW_REQUIRED",target_folder=folder)
    matches.append(rec);bymodel[(b,m)].append(rec)
  # Select exact model-bearing pages from long catalogs, retain unaltered originals.
  # Each excerpt is a review candidate, not a final series catalogue.
  if kind=="catalog" and hits:
   group=collections.defaultdict(set)
   for m,pp in hits.items():
    if brand=="Midea":
     if m.startswith("MIH"): key=re.sub(r"^MIH\d+","MIH_",m)
     elif m.startswith("MVUH"):key="ATOM_B"
     elif m.startswith("MVUW"):key="V4plusW"
     elif m.startswith("MVC-M"):key="VC_MAX"
     else:key=re.sub(r"\d+WV.*","",m)+"_"+("ULTRA" if "ULTRA" in m else "PRO" if "PRO" in m else "standard")
    elif brand=="Kentatsu":key="DX_PRO_VII_Individual" if m.endswith("-i") else "DX_PRO_VII"
    elif brand=="Daikin":key="VRV_IV_S" if m.startswith("RXYSQ") else "VRV_IVplus"
    else:key="MDCI"
    group[key].update(pp)
   for groupkey,pp in group.items():
    name="REVIEW_EXCERPTS/"+brand+"/"+re.sub(r"[^A-Za-z0-9_-]","_",groupkey)+"_"+sha[:8]+".pdf"
    with fitz.open() as out:
     for i in sorted(pp):out.insert_pdf(pdf,from_page=i,to_page=i)
     data=out.tobytes(garbage=4,deflate=True)
    try:
     with fitz.open(stream=data,filetype="pdf") as out:
      assert len(out)==len(pp)
      for j,i in enumerate(sorted(pp)):
       assert out[j].get_text()==pages[i]
       a=pdf[i].get_pixmap(matrix=fitz.Matrix(.2,.2));b=out[j].get_pixmap(matrix=fitz.Matrix(.2,.2))
       assert a.samples==b.samples
     excerpts[name]=data
    except Exception as e:
     print("EXCERPT_REJECTED",name,str(e),flush=True)
  docrows.append(dict(brand=brand,archive_path=path,kind=kind,source=" | ".join(dict.fromkeys(metadata.get(path,[]))),bytes=len(raw),sha256=sha,pages=len(pages),text_chars=sum(len(t) for t in pages),models_exact=len(hits)))
coverage=[]
for (b,m),folder in inventory.items():
 rs=bymodel[(b,m)]; tech=[r for r in rs if r["document_kind"]!="declaration"];dec=[r for r in rs if r["document_kind"]=="declaration"]
 coverage.append(dict(brand=b,model=m,base_url="https://docs.proclimate5.ru/"+folder if folder else "",technical_pdf_count=len(tech),declaration_count=len(dec),status="BLOCKED_NO_BASE_URL" if not folder else "EXACT_TEXT_REVIEW_REQUIRED" if tech else "DECLARATION_ONLY" if dec else "NO_EXACT_TECH_PDF",files=" | ".join(r["archive_path"] for r in rs)))
def writecsv(name,rows):
 p=root/name
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 return p
paths=[writecsv("coverage_347.csv",coverage),writecsv("model_evidence.csv",matches),writecsv("document_manifest.csv",docrows),writecsv("download_attempts.csv",attempts)]
stats=collections.Counter(r["brand"] for r in coverage if r["technical_pdf_count"])
summary=dict(catalog_total=347,original_pdfs=len(originals),new_original_pdfs=len(originals)-17,new_sources_downloaded=sum(bool(r["archive_path"]) for r in attempts),new_sources_attempted=len(attempts),review_excerpts=len(excerpts),exact_technical_text_models=sum(stats.values()),by_brand=dict(stats),blocked_no_base_url=2,ready_for_selectel=0,warning="Review archive. Exact text matches are not final approval; regional scope, document type, version and page completeness require human review. No Selectel upload or Excel edits.")
outpath=root/"Climate_347_PDF_stage5_review.zip"
with zipfile.ZipFile(outpath,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for n,v in {**originals,**excerpts}.items():z.writestr(n,v)
 for p in paths:z.write(p,"REPORTS/"+p.name)
 z.writestr("REPORTS/stage4_model_evidence.csv",(lambda: None)() or b"") if False else None
 z.writestr("REPORTS/summary.json",json.dumps(summary,ensure_ascii=False,indent=2))
with zipfile.ZipFile(outpath) as z:assert z.testzip() is None
summary["archive_sha256"]=hashlib.file_digest(outpath.open("rb"),"sha256").hexdigest()
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print("RESULT",json.dumps(summary),flush=True)
