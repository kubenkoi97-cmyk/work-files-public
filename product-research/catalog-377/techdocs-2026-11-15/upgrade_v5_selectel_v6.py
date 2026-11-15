#!/usr/bin/env python3
"""Deterministic v5 -> v6 upgrade; no network re-download of 66 unchanged verified PDFs."""
import sys,csv,io,re,hashlib,json,zipfile,os
import requests,fitz
from pathlib import Path
SRC,OUT=map(Path,sys.argv[1:3])
SRC_SHA="e02b2a43097cf18a841b596d43d52aec11d8d8371cffd8d45b26fda7c53d3074"
URL="https://iclim.ru/library/igc-ims-5-vnutrennie-bloki-instruktsiya.pdf"
REMOTE="https://docs.proclimate5.ru/multizonalnye_vrv_i_vrf_sistemy/vnutrennie_bloki_VRF_sistem_IGC/2026/IMS_5_installation_and_user_manual_2026.pdf"
TARGET="UPLOAD_TO_SELECTEL/multizonalnye_vrv_i_vrf_sistemy/vnutrennie_bloki_VRF_sistem_IGC/2026/IMS_5_installation_and_user_manual_2026.pdf"
SOURCE_PATH="IGC/IMS_5/IMS_5_installation_and_user_manual_2026.pdf"
MODELS={
"IMS-4TM28NH (DC5)","IMS-4TM36NH(DC5)","IMS-4TM45NH(DC5)",
"IMS-4TM56NH(DC5)","IMS-QV100NH(DC)"}
def normalized(s):return re.sub(r"[^A-Z0-9]","",s.upper())
resp=requests.get(URL,timeout=(15,75),headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf"})
resp.raise_for_status();payload=resp.content
assert payload.startswith(b"%PDF-"),"IGC PDF invalid"
with fitz.open(stream=payload,filetype="pdf") as pdf:
 pages=[normalized(p.get_text("text")) for p in pdf]
 verified={m for m in MODELS if any(normalized(m) in page for page in pages)}
 assert verified==MODELS, "IMS5 PDF does not match all five exact requested SKU codes"
 print("IGC_PDF_VALIDATED",len(pdf),len(payload),sorted(verified),flush=True)
assert hashlib.file_digest(open(SRC,"rb"),"sha256").hexdigest()==SRC_SHA,"v5 release SHA-256 mismatch"
def csvrows(data):
 return list(csv.DictReader(io.StringIO(data.decode('utf-8-sig')),delimiter=","))
def tocsv(rows,headers):
 s=io.StringIO();w=csv.DictWriter(s,fieldnames=headers,extrasaction="ignore",lineterminator="\n");w.writeheader();w.writerows(rows)
 return s.getvalue().encode("utf-8-sig")
BLOCK='<p>\n <a href="{url}" target="_blank"><img src="/images/icons/pdf-icon2.jpg" alt="" style="height:41px; width:40px"></a> <a href="{url}" target="_blank">Инструкция к товару</a>\n</p>'.format(url=REMOTE)
with zipfile.ZipFile(SRC,"r") as inz:
 assert inz.testzip() is None
 audit=csvrows(inz.read("REPORTS/ALL_377.csv"))
 assert len(audit)==377
 statuses={}
 for a in audit:
  m=a["model"]
  if m in MODELS:
   assert a["brand"]=="IGC"
   statuses[m]=(a["new_proof"],a["document_count"])
   a["new_proof"]="DIRECT_IGC_IMS5_TECH_MANUAL_EXACT"
   prev=int(a["document_count"]);a["document_count"]=str(prev+1)
   a["doc_filenames"]=(a["doc_filenames"]+" | " if a["doc_filenames"] else "")+Path(SOURCE_PATH).name
   a["source_evidence"]=(a["source_evidence"]+" | " if a["source_evidence"] else "")+SOURCE_PATH
   a["target_urls"]=(a["target_urls"]+" | " if a["target_urls"] else "")+REMOTE
   a["html"]=(a["html"]+"\n" if a["html"] else "")+BLOCK
   a["action"]="UPLOAD_PDFS_AND_VERIFY_HTTP_200__LINKS_NOT_YET_LIVE"
 assert set(statuses)==MODELS,statuses
 need=[r for r in audit if r["new_proof"]=="NOT_MODEL_VERIFIED" or r["new_proof"]=="DECLARATION_ONLY"]
 assert len(need)==20,len(need)
 assert sum(r["new_proof"]=="DIRECT_IGC_IMS5_TECH_MANUAL_EXACT" for r in audit)==5
 servers=csvrows(inz.read("REPORTS/SERVER_FILE_MANIFEST.csv"))
 assert len(servers)==66,len(servers)
 servers.append(dict(zip_path=TARGET,sha256=hashlib.sha256(payload).hexdigest(),bytes=len(payload),target_url=REMOTE))
 changed={
  "REPORTS/ALL_377.csv":tocsv(audit,list(audit[0])),
  "REPORTS/NEED_MORE_PROOF.csv":tocsv(need,list(audit[0])),
  "REPORTS/SERVER_FILE_MANIFEST.csv":tocsv(servers,list(servers[0])),
  "REPORTS/NEW_IGC_IMS5_MODELS.csv":tocsv([{"model":m,"source_pdf":URL,"target_url":REMOTE,"pages_with_exact_model":"4"} for m in sorted(MODELS)],["model","source_pdf","target_url","pages_with_exact_model"]),
  "README_V6_SELECTEL.txt":("MIXED377 v6 after v5 original. 357 exact SKU technical PDF, 20 without proof, 0 declaration-only, 67 upload PDFs. New IGC IMS 5 installation/manual for 5 models exact listed on PDF p4. Reuse all original other documents unchanged. Upload only contents of UPLOAD_TO_SELECTEL. No Selectel publication performed. All target links require real upload and HTTP GET check.\nSource: "+URL+"\n").encode("utf-8"),
 }
 OUT.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(OUT,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=5,allowZip64=True) as out:
  for f in inz.infolist():
   if f.filename in changed:continue
   if f.filename==TARGET:raise AssertionError("target path already present")
   with inz.open(f.filename) as input, out.open(f.filename,"w",force_zip64=True) as dest:
    while chunk:=input.read(4*1024*1024):dest.write(chunk)
  out.writestr(TARGET,payload)
  for filename,body in changed.items():out.writestr(filename,body)
with zipfile.ZipFile(OUT) as check:
 assert check.testzip() is None
 assert len(csvrows(check.read("REPORTS/ALL_377.csv")))==377
 assert len(csvrows(check.read("REPORTS/NEED_MORE_PROOF.csv")))==20
 assert len(csvrows(check.read("REPORTS/SERVER_FILE_MANIFEST.csv")))==67
assert OUT.stat().st_size>500_000_000,"output not full"
result={"archive":str(OUT),"archive_bytes":OUT.stat().st_size,"archive_sha256":hashlib.file_digest(open(OUT,"rb"),"sha256").hexdigest(),"models":377,"exact_technical":357,"unverified":20,"declaration_only":0,"upload_pdf_files":67,"new_igc_models":sorted(MODELS),"pdf_sha256":hashlib.sha256(payload).hexdigest(),"not_uploaded_to_selectel":True}
Path(str(OUT)+".summary.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print("RESULT",json.dumps(result,ensure_ascii=False),flush=True)
