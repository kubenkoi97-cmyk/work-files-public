import pathlib,zipfile,hashlib,subprocess,io,csv,re,json,base64,collections
import fitz, requests
from PIL import Image,ImageOps,ImageDraw
import numpy as np
ROOT=pathlib.Path("climate-347/images"); OUT=pathlib.Path("stage12-out");OUT.mkdir(exist_ok=True)
tag="climate-347-pdf-stage17-45511680707"; name="Climate_347_stage17_partial_Selectel.zip"
subprocess.run(["gh","release","download",tag,"-p",name,"-D",str(OUT)],check=True)
p=OUT/name
h=hashlib.sha256()
with p.open("rb") as f:
    for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
assert h.hexdigest()=="bc853ccdeff05f353f1171be34a5872bbe5346b555a5c420b71280fdc1a7cd68"
wanted=re.compile(r"^(MDCI_catalog|MDCI-40_45-_-montazh|DX_PRO_A_user_manual|MIH_FS_FL_manual|V8i_ULTRA_installation_and_user_manual|V8S_winter_option_catalog|V8Si_catalog|VC_MAX_catalog|VRV_IVplus_winter_option_catalog|IGC_IMBR_IMBRG_R_installation_and_user_manual|IWF_Q_CAQ4T44_passport|VRV_IV_S_winter_option_catalog)\.pdf$",re.I)
groups=[]
with zipfile.ZipFile(p) as z:
    for n in z.namelist():
        if wanted.match(pathlib.PurePosixPath(n).name):
            groups.append((pathlib.PurePosixPath(n).name,z.read(n),"stage17:"+n))
# Use original factory catalogue sources from stage 9/10 evidence, not only prepared excerpts.
extra=[
("Kentatsu_catalog_original.pdf","https://www.c-o-k.ru/library/catalogs/kentatsu/37986/140011.pdf"),
("Midea_Daichi_catalog_original.pdf","https://daichi.business/upload/iblock/32c/M2_2024_DM24_02.01.02_Small_260824.pdf"),
("Bosch_MDCl_original.pdf","https://www.bosch-industrial.com/gb/media/country_pool/service/catalogues/br_bosch_climate_5000_vrf_mdci.pdf"),
("Daikin_winter_original.pdf","https://www.thermotrade.ru/wp-content/uploads/2024/04/daikin-vrv-2024.pdf")
]
attempts=[]
for name,url in extra:
    try:
        with requests.get(url,timeout=(10,30),stream=True) as r:
            r.raise_for_status(); d=bytearray()
            for b in r.iter_content(1024*1024):
                d.extend(b)
                if len(d)>100_000_000:raise ValueError("size cap")
        assert d[:4]==b"%PDF"
        groups.append((name,bytes(d),url));attempts.append(dict(name=name,url=url,status="PDF_ACQUIRED",detail=str(len(d))))
    except Exception as e:attempts.append(dict(name=name,url=url,status="FAILED",detail=str(e)[:200]))
targets=list(csv.DictReader((ROOT/"audits/stage-10-download-queue.csv").open(encoding="utf-8"),delimiter=";"))
models=sorted(set(x["model"] for x in targets))
# Allow exact base code as a lead, never automatic approval for winter version.
keys={m:m.replace("/-40","") for m in models}
def normalize(s):return re.sub(r"[^A-Z0-9]","",s.upper())
def match(s):
    n=normalize(s)
    return [m for m,k in keys.items() if normalize(k) in n]
def writecsv(path,rows,fields):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
rows=[];pages=[];docs=[];unique={}; allpages={}
for name,data,source in groups:
    doc=fitz.open(stream=data,filetype="pdf");sha=hashlib.sha256(data).hexdigest(); hits=[]
    for i,pg in enumerate(doc):
        txt=pg.get_text(); found=match(txt)
        if found:hits.append((i,found))
    selected=set()
    for i,found in hits:
        selected.update(j for j in (i-1,i,i+1) if 0<=j<len(doc))
    # Also inspect cover/first pages where labelled range product visuals commonly occur.
    selected.update(range(min(3,len(doc))))
    docs.append(dict(pdf=name,source=source,sha256=sha,pages=len(doc),exact_or_base_hits=len(hits),pages_examined=len(selected),models=" | ".join(sorted({m for _,a in hits for m in a}))))
    hitmap=dict(hits)
    for i in sorted(selected):
        pg=doc[i];near=sorted({m for j in (i-1,i,i+1) for m in hitmap.get(j,[])})
        # extract native PDF raster, including soft mask, not screenshots enlarged to simulate detail
        for img in pg.get_images(full=True):
            xref,smask,w,h=img[:4]
            if max(w,h)<450 or min(w,h)<140:continue
            try:
                pix=fitz.Pixmap(doc,xref)
                if smask:
                    try:pix=fitz.Pixmap(pix,fitz.Pixmap(doc,smask))
                    except Exception:pass
                if pix.colorspace is None:continue
                if pix.colorspace.n>3:pix=fitz.Pixmap(fitz.csRGB,pix)
                im=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")
                bg=Image.new("RGBA",im.size,"white");bg.alpha_composite(im);im=bg.convert("RGB")
                arr=np.asarray(im); mask=(arr<=242).any(axis=2)
                if not mask.any():continue
                yy,xx=np.where(mask);box=(int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1))
                bw,bh=box[2]-box[0],box[3]-box[1]
                if max(bw,bh)<450 or min(bw,bh)<100:continue
                pixhash=hashlib.sha256(f"{im.width}x{im.height}:".encode()+im.tobytes()).hexdigest()
                path=OUT/"native"/(pixhash[:24]+".png");path.parent.mkdir(exist_ok=True)
                if not path.exists():im.save(path)
                rects=pg.get_image_rects(xref)
                visible=[r for r in rects if not r.is_empty and r.intersects(pg.rect)]
                if not visible:continue
                rec=dict(pdf=name,pdf_sha256=sha,source=source,page=i+1,xref=xref,raster=f"{w}x{h}",object_px=f"{bw}x{bh}",native_long=max(bw,bh),screen="NATIVE_750_PLUS" if max(bw,bh)>=750 else "LOWER_RES_REVIEW",pixel_sha256=pixhash,file=str(path.relative_to(OUT)),page_models=" | ".join(hitmap.get(i,[])),near_models=" | ".join(near),page_rects=" | ".join(str(r) for r in visible),status="CANDIDATE_NOT_APPROVED")
                rows.append(rec);unique.setdefault(pixhash,rec);allpages[(name,i+1)]=(doc,i)
            except Exception:continue
    # save page contexts before closing the document, only pages containing qualifying native raster
    for key,(d,i) in list(allpages.items()):
        if key[0]!=name:continue
        pg=d[i]; scale=min(1.5,1250/max(pg.rect.width,pg.rect.height))
        pm=pg.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False)
        dest=OUT/"page-context"/(pathlib.Path(name).stem+f"-p{i+1:03d}.jpg");dest.parent.mkdir(exist_ok=True);pm.save(str(dest))
        pages.append(dict(pdf=name,page=i+1,file=str(dest.relative_to(OUT)),exact_or_base_models=" | ".join(hitmap.get(i,[]))))
        del allpages[key]
    doc.close()
fields=["pdf","pdf_sha256","source","page","xref","raster","object_px","native_long","screen","pixel_sha256","file","page_models","near_models","page_rects","status"]
writecsv(ROOT/"audits/stage-12-pdf-native-candidates.csv",rows,fields)
writecsv(ROOT/"audits/stage-12-pdf-source-scan.csv",docs,["pdf","source","sha256","pages","exact_or_base_hits","pages_examined","models"])
writecsv(ROOT/"audits/stage-12-pdf-downloads.csv",attempts,["name","url","status","detail"])
writecsv(OUT/"page-index.csv",pages,["pdf","page","file","exact_or_base_models"])
# Gallery sheets at review size, separately retained full native originals and PDF page contexts.
u=sorted(unique.values(),key=lambda r:(r["pdf"],r["page"],-r["native_long"]))
for k in range(0,len(u),16):
    group=u[k:k+16]; im=Image.new("RGB",(1200,((len(group)+3)//4)*235),"white");d=ImageDraw.Draw(im)
    for j,r in enumerate(group):
        x=j%4*300;y=j//4*235
        a=Image.open(OUT/r["file"]);a=ImageOps.contain(a,(286,185));im.paste(a,(x+(300-a.width)//2,y))
        d.text((x+3,y+185),r["pdf"][:35],fill="black");d.text((x+3,y+200),f'p{r["page"]} {r["object_px"]} {r["pixel_sha256"][:10]}',fill="black")
    bio=io.BytesIO();im.save(bio,format="JPEG",quality=78)
    n=f"stage-12-contact-{k//16+1:02d}"
    (OUT/(n+".jpg")).write_bytes(bio.getvalue())
    # small set available immediately through connector for visual review
    if k<128:(ROOT/"audits"/(n+".b64.txt")).write_text(base64.b64encode(bio.getvalue()).decode())
summary=dict(pdf_documents=len(docs),pdf_pages_examined=sum(x["pages_examined"] for x in docs),raster_occurrences=len(rows),unique_rasters=len(u),native_750_plus=sum(x["native_long"]>=750 for x in u),page_contexts=len(pages),contact_sheets=(len(u)+15)//16,approved=0)
(ROOT/"audits/stage-12-pdf-summary.json").write_text(json.dumps(summary,indent=2))
with zipfile.ZipFile("Climate347_stage12_PDF_native_candidates.zip","w",compression=zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.rglob("*")):
        if f.is_file() and f.suffix!=".zip":z.write(f,f.relative_to(OUT))
    for f in ROOT.glob("audits/stage-12-pdf-*"):z.write(f,f.name)
with zipfile.ZipFile("Climate347_stage12_PDF_native_candidates.zip") as z:assert z.testzip() is None
print(json.dumps(summary))
