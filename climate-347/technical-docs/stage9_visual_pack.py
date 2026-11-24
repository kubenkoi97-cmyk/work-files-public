import csv,io,zipfile,re,hashlib,json,pathlib,subprocess,collections,concurrent.futures
import pymupdf as fitz
import requests
root=pathlib.Path("/tmp/climate347v9");root.mkdir(exist_ok=True)
def download(tag,name,sha):
 p=root/name;subprocess.run(["gh","release","download",tag,"-p",name,"-D",str(root)],check=True)
 assert hashlib.file_digest(p.open("rb"),"sha256").hexdigest()==sha
 return p
review=download("climate-347-pdf-stage7-45502663476","Climate_347_PDF_stage7_review.zip","73944dad6b73a20d7a93305edfda6bbd2d67c8a084f08f250ebe2d7445495d35")
partial=download("climate-347-pdf-stage8-45504757609","Climate_347_stage8_partial_Selectel.zip","f1fab9429078858af28f1c20c0db0ce5d3cf514dda7413625bc688d96d20e58b")
subprocess.run(["gh","release","download","climate-347-pdf-stage8-45504757609","-p","coverage_347.csv","-D",str(root)],check=True)
def readcsv(raw):return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
def csvbytes(rs):
 s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rs[0]),extrasaction="ignore");w.writeheader();w.writerows(rs);return s.getvalue().encode("utf-8-sig")
inv=readcsv((root/"coverage_347.csv").read_bytes())
with zipfile.ZipFile(review) as z:
 assert z.testzip() is None
 entries={n:z.read(n) for n in z.namelist() if not n.startswith(("REPORTS/","UPLOAD_TO_SELECTEL/"))}
 reports={n:z.read(n) for n in z.namelist() if n.startswith("REPORTS/")}
with zipfile.ZipFile(partial) as z:
 assert z.testzip() is None
 upload={n:z.read(n) for n in z.namelist() if n.startswith("UPLOAD_TO_SELECTEL/")}
 manifest=readcsv(z.read("REPORTS/partial_selectel_manifest.csv"))
assert len(inv)==347 and len(manifest)==100 and len(upload)==6
assert hashlib.sha256("\n".join(sorted(r["brand"]+"\t"+r["model"] for r in inv)).encode()).hexdigest()=="b11a94ae13d7ee8d9563e23ec22c51136e968abdbe0d8261f74ded25e3c30343"
def hit(m,t):
 m=re.sub(r"\s+","",m)
 p=r"(?<![A-Za-z0-9])"+r"\s*".join(re.escape(c) if c!="-" else r"[-‐‑–−]" for c in m)+r"(?![A-Za-z0-9_/(‐‑–−-])"
 return bool(re.search(p,t,re.I))
# Each selected page was visually inspected before this run. No suffix inference.
# rule = brand, source, filename, label, kind, regex, count, evidence pages, extract pages
rules=[
("IGC","IGC_IMBR_passport.pdf","IGC_IMBR_IMBRG_R_installation_and_user_manual.pdf","Инструкция к товару","combined_manual_passport",r"IMBR-[CH]1320ANB",2,[14],None),
("IGC","IWF_X_K22W_A_passport.pdf","IWF_X_K22W_A_passport.pdf","Инструкция к товару","combined_manual_passport",r"IWF-X\d+K22W-A",5,[1],None),
("IGC","IWF_Q_CAQ4T44_passport.pdf","IWF_Q_CAQ4T44_passport.pdf","Технический паспорт","passport",r"IWF-Q1700CAQ4T44",1,[1],None),
("Kentatsu","KYRA_A_installation_and_user_manual.pdf","KYRA_A_installation_and_user_manual.pdf","Инструкция к товару","manual",r"KYRA\d+HZAN1-A",6,[1],None),
("Kentatsu","DX_PRO_VII_catalog.pdf","DX_PRO_VII_catalog.pdf","Страница каталога","catalog",r"KTRB\d+HZAN3",15,[33],[33]),
("Kentatsu","DX_PRO_VII_catalog.pdf","DX_PRO_VII_Individual_catalog.pdf","Страница каталога","catalog",r"KTRB\d+HZAN3-i",15,[35],[35]),
("Midea","MIH_T1_installation_and_user_manual.pdf","MIH_T1_installation_and_user_manual.pdf","Инструкция к товару","manual",r"MIH\d+T1HN18",12,[1],None),
("Midea","MIH_FS_FL_manual.pdf","MIH_FS_FL_manual.pdf","Инструкция к товару","manual",r"MIH\d+F[SL]HN18",10,[1],None),
("Midea","MIH_DL_installation_and_user_manual.pdf","MIH_DL_installation_and_user_manual.pdf","Инструкция к товару","manual",r"MIH\d+DLHN18",10,[1],None),
("Midea","MIH_F3_F4_F5_technical_manual.pdf","MIH_F3_F4_F5_technical_manual.pdf","Технические данные","technical",r"MIH\d+F[345]HN18",21,[1],None),
("Midea","VC_MAX_installation_manual.pdf","VC_MAX_installation_manual.pdf","Инструкция к товару","manual",r"MVC-M\d+WV2GN1",12,[1],None),
("Midea","VC_MAX_catalog.pdf","VC_MAX_catalog.pdf","Страница каталога","catalog",r"MVC-M\d+WV2GN1",12,[1,2],[1,2]),
("Midea","V8i_ULTRA_installation_and_user_manual.pdf","V8i_ULTRA_installation_and_user_manual.pdf","Инструкция к товару","manual",r"MV8i-\d+WV2GN1\(ULTRA\)",18,[1],None),
("Midea","V8Si_catalog.pdf","V8Si_catalog.pdf","Страница каталога","catalog",r"MV8Si-\d+WV2GN1",9,[1],[1]),
("Midea","ATOM_B_catalog.pdf","ATOM_B_catalog.pdf","Страница каталога","catalog",r"MVUH(?:35|50|60|100|120)BT-VA1",5,[4,16],[4,16]),
("Midea","V8_V8i_PRO_installation_and_user_manual.pdf","V8_V8i_PRO_installation_and_user_manual.pdf","Инструкция к товару","manual",r"MV8i-\d+WV2GN1\(PRO\)",3,[1],None),
("Bosch","MDCI-40_45-_-montazh.pdf","MDCI-40_45-_-montazh.pdf","Инструкция по монтажу","installation",r"MDCI\s*(40|45)-3",2,[1],None),
("Bosch","Bosch_VRF_RU_catalog.pdf","MDCI_catalog.pdf","Страница каталога","catalog",r"MDCI\s*\d+-[13]",11,[101,103],[101,103]),
("Daikin","RYMQ_U_technical_manual.pdf","RYYQ_RYMQ_U_technical_data.pdf","Технические данные","technical",r"RYMQ\d+U",7,[10,11],None),
("Daikin","Daikin_2024_Daichi_catalog.pdf","VRV_IV_S_winter_option_catalog.pdf","Страница каталога","catalog",r"RXYSQ.*\/-40",9,[127],[127]),
]
new=[];rejected=[];checks=[];keys={(m["brand"],m["model"],m["full_url"]) for m in manifest}
for b,source,name,label,kind,rx,n,pages,clip in rules:
 found=[r for r in inv if r["brand"]==b and r["base_url"] and re.fullmatch(rx,r["model"])]
 if len(found)!=n:
  rejected.append(dict(filename=name,reason="inventory count mismatch",actual=len(found),expected=n));continue
 ps=[p for p in entries if p.startswith("ORIGINAL_PDF/"+b+"/") and p.endswith("/"+source)]
 if len(ps)!=1:
  rejected.append(dict(filename=name,reason="missing source",actual=len(ps),expected=1));continue
 raw=entries[ps[0]]
 try:
  with fitz.open(stream=raw,filetype="pdf") as doc:
   texts=[doc[i-1].get_text() for i in pages]
   if not (b=="IGC" and source=="IGC_IMBR_passport.pdf"):
    bad=[r["model"] for r in found if not any(hit(r["model"],t) for t in texts)]
    if bad:raise ValueError("missing exact page code "+str(bad))
   if clip:
    if clip==list(range(1,len(doc)+1)):
     payload=raw;check="original excerpt already complete"
    else:
     with fitz.open() as out:
      for i in clip:out.insert_pdf(doc,from_page=i-1,to_page=i-1)
      payload=out.tobytes(garbage=4,deflate=True)
     with fitz.open(stream=payload,filetype="pdf") as out:
      assert len(out)==len(clip)
      for j,i in enumerate(clip):
       assert out[j].get_text()==doc[i-1].get_text(),"extracted text differs"
       a=doc[i-1].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False);c=out[j].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
       assert (a.width,a.height,a.n)==(c.width,c.height,c.n),"page render dimensions differ"
       if a.samples!=c.samples:
        # Small antialias differences may occur when PDF objects are renumbered.
        aa,cc=a.samples,c.samples
        diff=sum(abs(x-y) for x,y in zip(aa,cc))/len(aa)
        if diff>0.05:raise ValueError("page rendering differs; mean pixel delta "+str(diff))
      check="page text identical and render delta <=0.05/255"
   else:payload=raw;check="unaltered original PDF"
  sha=hashlib.sha256(payload).hexdigest()
  checks.append(dict(filename=name,source=ps[0],source_pages=" ".join(map(str,pages)),extracted_pages=" ".join(map(str,clip or [])),sha256=sha,validation=check,models=len(found)))
  for r in found:
   u=r["base_url"]+name;p="UPLOAD_TO_SELECTEL/"+u.removeprefix("https://docs.proclimate5.ru/")
   if p in upload:assert upload[p]==payload,"path collision"
   upload[p]=payload
   if (b,r["model"],u) in keys:continue
   html='<p>\n <a href="'+u+'" target="_blank"><img src="/images/icons/pdf-icon2.jpg" alt="" style="height:41px; width:40px"></a> <a href="'+u+'" target="_blank">'+label+'</a>\n</p>'
   row=dict(brand=b,model=r["model"],filename=name,document_kind=kind,label_ru=label,base_url=r["base_url"],full_url=u,html=html,archive_path=p,sha256=sha,pages=" ".join(map(str,pages)),status="PREPARED_NOT_UPLOADED")
   manifest.append(row);new.append(row);keys.add((b,r["model"],u))
 except Exception as e:rejected.append(dict(filename=name,reason=str(e),actual=0,expected=n))
# Download additional actual originals for the next applicability pass; no link is approved from titles alone.
sources=[("MIH_FHN18_installation_manual_candidate.pdf","https://midea-pro.ru/library/midea-mih-fhn18-instruktsiya.pdf"),("V8_indoor_service_manual.pdf","https://midea-pro.ru/library/midea-mih100q4hn18-mih90t3hn18-instruktsiya.pdf")]
def fetch(pair):
 name,url=pair
 try:
  resp=requests.get(url,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf"},timeout=(10,30))
  resp.raise_for_status();raw=resp.content
  assert raw.startswith(b"%PDF-") and len(raw)<100*1024*1024
  with fitz.open(stream=raw,filetype="pdf") as doc:
   assert len(doc)>0
   first=doc[0].get_text()[:2000];preview=doc[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).tobytes("jpeg",jpg_quality=86)
  return name,url,raw,preview,first,""
 except Exception as e:return name,url,None,None,"",str(e)[:250]
attempts=[];neworig=0
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 for name,url,raw,preview,first,error in ex.map(fetch,sources):
  path=""
  if raw:
   sha=hashlib.sha256(raw).hexdigest();matches=[p for p,v in entries.items() if p.endswith(".pdf") and hashlib.sha256(v).hexdigest()==sha]
   if matches:path=matches[0]
   else:
    path="ORIGINAL_PDF/Midea/"+name;entries[path]=raw;neworig+=1
   entries["REVIEW_SCAN_IMAGES/"+name+".jpg"]=preview
  attempts.append(dict(filename=name,url=url,archive_path=path,bytes=len(raw) if raw else 0,cover_text=first,status="REVIEW_REQUIRED" if raw else "DOWNLOAD_FAILED",error=error))
  print("NEW_SOURCE",name,len(raw) if raw else 0,error,flush=True)
# Stable per-model HTML, one block per distinct actual PDF, catalog first.
priority={"catalog":0,"manual":1,"combined_manual_passport":1,"installation":2,"technical":7,"wiring":8,"passport":10,"declaration":11}
manifest.sort(key=lambda m:(m["brand"],m["model"],priority.get(m["document_kind"],9),m["filename"]))
by=collections.defaultdict(list)
for m in manifest:
 assert m["archive_path"] in upload and hashlib.sha256(upload[m["archive_path"]]).hexdigest()==m["sha256"]
 assert m["html"].count(m["full_url"])==2
 by[(m["brand"],m["model"])].append(m)
htmlrows=[]
for r in inv:
 ms=by[(r["brand"],r["model"])]
 tech=[m for m in ms if m["document_kind"]!="declaration"]
 dec=[m for m in ms if m["document_kind"]=="declaration"]
 r["visual_confirmed_technical_count"]=len(tech);r["visual_confirmed_declaration_count"]=len(dec)
 if tech:r["status"]="VISUAL_TECH_SCOPE_CONFIRMED"
 elif dec:r["status"]="VISUAL_DECLARATION_ONLY"
 if tech:r["technical_pdf_count"]=max(int(r["technical_pdf_count"]),len(tech))
 if ms:htmlrows.append(dict(brand=r["brand"],model=r["model"],document_count=len(ms),html="\n".join(m["html"] for m in ms),status="PREPARED_NOT_UPLOADED"))
summary=dict(catalog_total=347,new_assignments=len(new),partial_upload_models=len(by),partial_upload_pdfs=len(upload),visual_technical_models=sum(r["status"]=="VISUAL_TECH_SCOPE_CONFIRMED" for r in inv),declaration_only_models=sum(r["status"]=="VISUAL_DECLARATION_ONLY" for r in inv),new_originals=neworig,originals_including_quarantine=sum(n.endswith(".pdf") and n.startswith(("ORIGINAL_PDF/","QUARANTINE/")) for n in entries),rejected_rules=rejected,not_uploaded_to_selectel=True)
for name,rs in [("coverage_347.csv",inv),("partial_selectel_manifest.csv",manifest),("html_by_model.csv",htmlrows),("new_verified_assignments.csv",new),("stage9_checks.csv",checks),("stage9_new_downloads.csv",attempts)]:
 data=csvbytes(rs) if rs else b"no_records\n";(root/name).write_bytes(data);reports["REPORTS/"+name]=data
reports["REPORTS/summary.json"]=json.dumps(summary,ensure_ascii=False,indent=2).encode()
for file,files in [("Climate_347_stage9_partial_Selectel.zip",upload),("Climate_347_stage9_review.zip",{**entries,**upload})]:
 p=root/file
 with zipfile.ZipFile(p,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
  for n,v in files.items():z.writestr(n,v)
  for n,v in reports.items():z.writestr(n,v)
  z.writestr("README_STAGE9.txt","Prepared paths only. Selectel not uploaded. Review originals are not automatically approved. Use UPLOAD_TO_SELECTEL and HTML manifest; incomplete documentation remains.")
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
 summary[file+"_sha256"]=hashlib.file_digest(p.open("rb"),"sha256").hexdigest()
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print("RESULT",json.dumps(summary,ensure_ascii=False),flush=True)
for c in checks:print("RULE_OK",c["filename"],c["models"],flush=True)
for r in rejected:print("RULE_REJECTED",r,flush=True)
for r in new:print("ASSIGN",r["brand"],r["model"],r["filename"],flush=True)
