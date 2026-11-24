import pathlib,subprocess,zipfile,hashlib,csv,io,json,base64,re
import pymupdf as fitz
root=pathlib.Path("/tmp/climate347v20");root.mkdir(exist_ok=True)
tag="climate-347-pdf-stage18-45512224473";name="Climate_347_stage18_focused_review.zip";src=root/name
subprocess.run(["gh","release","download",tag,"-p",name,"-D",str(root)],check=True)
assert hashlib.file_digest(src.open("rb"),"sha256").hexdigest()=="1a276176ca69683608b51450f03d7ab954e0c480c0d194fa487c664dfd37d5b9"
def digest(raw):return hashlib.sha256(raw).hexdigest()
with zipfile.ZipFile(src) as z:
 assert z.testzip() is None
 recs=list(csv.DictReader(io.StringIO(z.read("REPORTS/download_attempts.csv").decode("utf-8-sig"))))
 manrec=next(r for r in recs if r["filename"]=="linked_candidate_0.pdf")
 catrec=next(r for r in recs if r["filename"]=="IMS7_catalog_COK.pdf")
 manual=z.read(manrec["archive_path"]);cat=z.read(catrec["archive_path"])
 hydro=z.read(next(n for n in z.namelist() if n.startswith("BLOCKED_NO_BASE_URL/") and n.endswith(".pdf")))
assert digest(manual)=="3f5358216fc4bf005c3996105de13558338eef418def81c12f9e9584118cf6df"
assert digest(cat)=="8dcab450ff00320d5f455b06f659866414992e694163206ba0ce96d71ea65893"
assert digest(hydro)=="d06d15a648b9f1bffa4d7815308cf2b3ef286a7d792c2a679975b0f60956ccf8"
def norm(s):return re.sub(r"\s+","",s)
with fitz.open(stream=manual,filetype="pdf") as d:
 assert "IMS7" in norm(d[0].get_text()) and "Руководство" in d[0].get_text()
 for i in [10,12,26]:assert "IMS-EX330NB(7)" in norm(d[i].get_text())
 # Preserve entire factory technical manual, but reject a standalone certificate/guarantee form as a document.
 assert not re.search(r"^\s*(сертификат соответствия|декларация соответствия|гарантийный талон)",d[0].get_text(),re.I)
 for pg in d:pg.get_pixmap(matrix=fitz.Matrix(.12,.12),alpha=False)
 mcount=len(d)
 cover=d[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).tobytes("jpeg",jpg_quality=90)
with fitz.open(stream=hydro,filetype="pdf") as d:
 assert "SMK-D140HHN1-3" in norm(d[0].get_text()) and "ServiceManual" in norm(d[0].get_text())
 for pg in d:pg.get_pixmap(matrix=fitz.Matrix(.12,.12),alpha=False)
 hcount=len(d)
caterror=""
try:
 with fitz.open(stream=cat,filetype="pdf") as d,fitz.open(stream=cat,filetype="pdf") as e:
  page=d[22];t=norm(page.get_text());assert "IMS7" in t and "IMS-EX330NB" in t
  e.select([22]);excerpt=e.tobytes(garbage=0,deflate=False)
  with fitz.open(stream=excerpt,filetype="pdf") as o:
   assert len(o)==1 and o[0].get_text()==page.get_text()
   a=page.get_pixmap(alpha=False);b=o[0].get_pixmap(alpha=False)
   assert (a.width,a.height,a.n)==(b.width,b.height,b.n) and a.samples==b.samples
except Exception as ex:excerpt=None;caterror=repr(ex)
files={"IGC/IMS7_design_installation_service_manual.pdf":manual,"Midea/SMK-D140HHN1-3_service_manual.pdf":hydro}
rows=[dict(brand="IGC",model="IMS-EX330NB(7)",filename="IGC/IMS7_design_installation_service_manual.pdf",kind="technical",source=manrec["url"],source_pages="11,13,27 (exact model scope)",pages=mcount,sha256=digest(manual),base_url="",status="BLOCKED_NO_BASE_URL"),dict(brand="Midea",model="SMK-D140HHN1-3",filename="Midea/SMK-D140HHN1-3_service_manual.pdf",kind="service",source="https://www.midea.com.ua/sites/default/files/downloadables-documents/pdf/sm-smk-d140-hhn1-3-high-temperature-hydro-modulel.pdf".replace("d140-hhn1","d140hhn1"),source_pages="1",pages=hcount,sha256=digest(hydro),base_url="",status="BLOCKED_NO_BASE_URL")]
if excerpt:
 files["IGC/IMS7_catalog_page.pdf"]=excerpt
 rows.append(dict(brand="IGC",model="IMS-EX330NB(7)",filename="IGC/IMS7_catalog_page.pdf",kind="catalog",source=catrec["url"],source_pages="23",pages=1,sha256=digest(excerpt),base_url="",status="BLOCKED_NO_BASE_URL"))
s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);report=s.getvalue().encode("utf-8-sig")
(root/"blocked_manifest.csv").write_bytes(report)
summary=dict(covered_selectel_unchanged=327,blocked_models=2,prepared_blocked_files=len(files),catalog_pixel_exact=bool(excerpt),catalog_error=caterror,unresolved_models_without_verified_pdf=18,selectel_uploaded=False,workbook_changed=False,manual_pages=mcount,hydro_pages=hcount)
out=root/"Climate_347_stage20_blocked_paths.zip"
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for n,v in files.items():z.writestr(n,v)
 z.writestr("REPORTS/blocked_manifest.csv",report)
 z.writestr("REPORTS/summary.json",json.dumps(summary,ensure_ascii=False,indent=2))
 z.writestr("README.txt","Technical files for 2 previously empty models. No destination URL supplied. Do not upload until exact category paths are supplied. No certificates or declarations.")
with zipfile.ZipFile(out) as z:assert z.testzip() is None
summary["archive_sha256"]=hashlib.file_digest(out.open("rb"),"sha256").hexdigest()
(root/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
# Cover preview available separately in release (no concurrent repo push).
(root/"IMS7_manual_cover.jpg").write_bytes(cover)
print("RESULT",json.dumps(summary,ensure_ascii=False),flush=True)
