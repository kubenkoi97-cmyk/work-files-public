import csv,io,zipfile,re,hashlib,json,pathlib,subprocess,collections
import pymupdf as fitz
import requests
root=pathlib.Path("/tmp/climate347v8");root.mkdir(exist_ok=True)
src=root/"Climate_347_PDF_stage7_review.zip"
subprocess.run(["gh","release","download","climate-347-pdf-stage7-45502663476","-p",src.name,"-D",str(root)],check=True)
assert hashlib.file_digest(src.open("rb"),"sha256").hexdigest()=="73944dad6b73a20d7a93305edfda6bbd2d67c8a084f08f250ebe2d7445495d35"
def rows(raw):return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
def csvdata(rs):
 s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rs[0]),extrasaction="ignore");w.writeheader();w.writerows(rs);return s.getvalue().encode("utf-8-sig")
with zipfile.ZipFile(src) as z:
 assert z.testzip() is None
 inv=rows(z.read("REPORTS/coverage_347.csv"))
 evidence=rows(z.read("REPORTS/model_evidence.csv"))
 manifest=rows(z.read("REPORTS/partial_selectel_manifest.csv"))
 docs=rows(z.read("REPORTS/document_manifest.csv"))
 entries={n:z.read(n) for n in z.namelist() if not n.startswith("REPORTS/")}
 reports={n:z.read(n) for n in z.namelist() if n.startswith("REPORTS/")}
assert len(inv)==347 and len(manifest)==51
bykey={(r["brand"],r["model"]):r for r in inv}
assert hashlib.sha256("\n".join(sorted(b+"\t"+m for b,m in bykey)).encode()).hexdigest()=="b11a94ae13d7ee8d9563e23ec22c51136e968abdbe0d8261f74ded25e3c30343"
def exact(m,t):
 m=re.sub(r"\s+","",m)
 pat=r"(?<![A-Za-z0-9])"+r"\s*".join(re.escape(c) if c!="-" else r"[-‐‑–−]" for c in m)+r"(?![A-Za-z0-9_/(‐‑–−-])"
 return bool(re.search(pat,t,re.I))
# Render the real source covers and model-bearing pages for subsequent scope review.
previewdir=pathlib.Path("climate-347/technical-docs/stage8-previews");previewdir.mkdir(exist_ok=True)
index=[]
for p,raw in entries.items():
 if not p.startswith("ORIGINAL_PDF/") or not p.endswith(".pdf"):continue
 with fitz.open(stream=raw,filetype="pdf") as pdf:
  base=pathlib.Path(p).stem
  hits=collections.Counter()
  for e in evidence:
   if e["archive_path"]==p:
    for n in re.findall(r"\d+",e["pages"]):hits[int(n)-1]+=1
  chosen=list(dict.fromkeys([0]+[i for i,_ in hits.most_common(2) if i<len(pdf)]))
  if "IGC_IMBR_passport" in p:chosen=list(dict.fromkeys(chosen+[11,12,13,14,35,36,37]))
  for i in chosen:
   if i>=len(pdf):continue
   n=base+"_p"+str(i+1)+".jpg"
   pix=pdf[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
   (previewdir/n).write_bytes(pix.tobytes("jpeg",jpg_quality=86))
   index.append(dict(archive_path=p,page=i+1,preview=n,exact_model_hits=hits[i],sha256=hashlib.sha256(raw).hexdigest()))
# Use only source scopes visually inspected in prior stages: Kentatsu DX PRO A cover;
# Midea ATOM 200 cover and Daikin REMQ5U drawing. Validate exact full codes again.
rules=[
("Kentatsu","DX_PRO_A_user_manual.pdf","DX_PRO_A_user_manual.pdf","Инструкция к товару","manual",r"KV(?:AH|AG|AM).*",47),
("Midea","ATOM_B_200_installation_and_user_manual.pdf","ATOM_B_200_installation_and_user_manual.pdf","Инструкция к товару","manual",r"MVUH200BT-VA1",1),
("Daikin","REMQ5U_wiring_diagram.pdf","REMQ5U_wiring_diagram.pdf","Схема подключения","wiring",r"REMQ5U",1)]
added=[];reject=[]
for brand,source,name,label,kind,regex,expected in rules:
 ps=[p for p in entries if p.startswith("ORIGINAL_PDF/"+brand+"/") and p.endswith("/"+source)]
 if len(ps)!=1:
  reject.append(dict(source=source,reason="source filename missing or ambiguous",found=len(ps)));continue
 p=ps[0];raw=entries[p]
 with fitz.open(stream=raw,filetype="pdf") as pdf:
  first=pdf[0].get_text()
  found=[r for r in inv if r["brand"]==brand and re.fullmatch(regex,r["model"]) and r["base_url"] and exact(r["model"],first)]
 if len(found)!=expected:
  reject.append(dict(source=source,reason="cover model count differs from prior visual audit",found=len(found)));continue
 for r in found:
  url=r["base_url"]+name
  dest="UPLOAD_TO_SELECTEL/"+url.removeprefix("https://docs.proclimate5.ru/")
  if dest in entries:assert entries[dest]==raw
  entries[dest]=raw
  html='<p>\n <a href="'+url+'" target="_blank"><img src="/images/icons/pdf-icon2.jpg" alt="" style="height:41px; width:40px"></a> <a href="'+url+'" target="_blank">'+label+'</a>\n</p>'
  row=dict(brand=brand,model=r["model"],filename=name,document_kind=kind,label_ru=label,base_url=r["base_url"],full_url=url,html=html,archive_path=dest,sha256=hashlib.sha256(raw).hexdigest(),pages="1",status="PREPARED_NOT_UPLOADED")
  if not any(m["brand"]==brand and m["model"]==r["model"] and m["full_url"]==url for m in manifest):
   manifest.append(row);added.append(row)
  r["visual_confirmed_technical_count"]=max(int(r["visual_confirmed_technical_count"]),1)
  r["status"]="VISUAL_TECH_SCOPE_CONFIRMED"
# Ensure every planned path resolves to actual bytes in package.
for m in manifest:
 assert m["archive_path"] in entries
 assert hashlib.sha256(entries[m["archive_path"]]).hexdigest()==m["sha256"]
 assert m["full_url"]==m["base_url"]+m["filename"]
 assert m["html"].count(m["full_url"])==2
upload={p:v for p,v in entries.items() if p.startswith("UPLOAD_TO_SELECTEL/")}
summary=dict(catalog_total=347,original_pdfs_including_quarantine=45,new_approved_document_assignments=len(added),partial_upload_pdfs=len(upload),partial_upload_models=len({(m["brand"],m["model"]) for m in manifest}),visual_confirmed_technical=sum(int(r["visual_confirmed_technical_count"])>0 for r in inv),visual_declaration_only=sum(r["status"]=="VISUAL_DECLARATION_ONLY" for r in inv),review_previews=len(index),rejected_rules=reject,not_uploaded_to_selectel=True)
for n,rs in [("coverage_347.csv",inv),("partial_selectel_manifest.csv",manifest),("preview_index.csv",index)]:
 data=csvdata(rs);reports["REPORTS/"+n]=data;(root/n).write_bytes(data)
reports["REPORTS/summary.json"]=json.dumps(summary,ensure_ascii=False,indent=2).encode()
part=root/"Climate_347_stage8_partial_Selectel.zip"
with zipfile.ZipFile(part,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p,v in upload.items():z.writestr(p,v)
 z.writestr("REPORTS/partial_selectel_manifest.csv",csvdata(manifest))
 z.writestr("README.txt","Partial upload preparation. No live Selectel verification. Not all documents for each SKU are included.")
with zipfile.ZipFile(part) as z:assert z.testzip() is None
summary["partial_archive_sha256"]=hashlib.file_digest(part.open("rb"),"sha256").hexdigest()
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print("RESULT",json.dumps(summary,ensure_ascii=False),flush=True)
for a in added:print("APPROVED",a["brand"],a["model"],a["filename"],flush=True)
for r in reject:print("REJECTED",r,flush=True)
# Verify previous public download URL without credentials, using ranged GET.
u="https://github.com/kubenkoi97-cmyk/work-files-public/releases/download/climate-347-pdf-stage7-45502663476/Climate_347_stage7_partial_Selectel.zip"
try:
 with requests.get(u,headers={"Range":"bytes=0-3"},stream=True,timeout=(10,15)) as response:
  print("PUBLIC_DOWNLOAD_CHECK",response.status_code,next(response.iter_content(4)).hex(),flush=True)
except Exception as e:print("PUBLIC_DOWNLOAD_CHECK_FAILED",str(e),flush=True)
