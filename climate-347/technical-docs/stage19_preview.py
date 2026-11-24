import pathlib,subprocess,zipfile,hashlib,csv,io,json,base64
import pymupdf as fitz
root=pathlib.Path("/tmp/climate347v19");root.mkdir(exist_ok=True)
name="Climate_347_stage18_focused_review.zip";src=root/name
subprocess.run(["gh","release","download","climate-347-pdf-stage18-45512224473","-p",name,"-D",str(root)],check=True)
assert hashlib.file_digest(src.open("rb"),"sha256").hexdigest()=="1a276176ca69683608b51450f03d7ab954e0c480c0d194fa487c664dfd37d5b9"
with zipfile.ZipFile(src) as z:
 assert z.testzip() is None
 attempts=list(csv.DictReader(io.StringIO(z.read("REPORTS/download_attempts.csv").decode("utf-8-sig"))))
 for n in ("linked_candidate_0.pdf","IMS7_catalog_COK.pdf"):
  r=next(x for x in attempts if x["filename"]==n)
  raw=z.read(r["archive_path"]);assert hashlib.sha256(raw).hexdigest()==r["sha256"]
  print("SOURCE",json.dumps({k:r[k] for k in ["filename","url","sha256","model_pages","cover"]},ensure_ascii=False),flush=True)
  with fitz.open(stream=raw,filetype="pdf") as d:
   print("DOC",n,"pages",len(d),"first",d[0].get_text()[:1500],flush=True)
   selected=[1,11,13,27] if n.startswith("linked") else [1,23]
   for i in selected:
    pg=d[i-1];text=pg.get_text()
    print("PAGE",n,i,text[:400],flush=True)
    # Render actual pages and commit only small visual evidence via contents API.
    img=pg.get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False).tobytes("jpeg",jpg_quality=86)
    fname=n.replace(".pdf","")+"_p"+str(i)+".jpg"
    path="climate-347/technical-docs/stage19-previews/"+fname
    payload={"message":"Save IMS7 verified-source review page "+fname,"content":base64.b64encode(img).decode(),"branch":"main"}
    q=root/"payload.json";q.write_text(json.dumps(payload))
    rr=subprocess.run(["gh","api","--method","PUT","repos/kubenkoi97-cmyk/work-files-public/contents/"+path,"--input",str(q),"--jq",".content.sha"],capture_output=True,text=True)
    print("PREVIEW",fname,rr.returncode,rr.stdout.strip(),rr.stderr[:180],flush=True)
