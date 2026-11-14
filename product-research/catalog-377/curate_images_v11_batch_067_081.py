#!/usr/bin/env python3
"""v11 product-image pilot, only verified unfilled Catalog-744 SKUs.

Downloads the existing original source ZIP, never modifies source HTML,
uses manifest.image_files (the archived product gallery), applies safe image
normalization, and publishes source traceability and a contact sheet.
"""
import csv, hashlib, io, json, os, re, shutil, sys, zipfile
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

ROOT=Path("product-research/catalog-377")
STATUS=ROOT/"status/master_status.csv"
OUT=Path(os.environ.get("OUTPUT_DIR", "out/catalog377-v11"))
ARCHIVES={"catalog377-batch-067-081":Path(os.environ["SOURCE_ZIP"]),"catalog377-recovery-batch-067-081":Path(os.environ["SOURCE_ZIP_RECOVERY"])}
EXPECTED_ROWS=set(range(68,83))
TARGET_SERIES=None
NONPRODUCT=re.compile(r"(?:logo|banner|favicon|feature|advantage|wifi|filter|icon|brochure|catalog\.pdf|certif|instruction|schema|diagram)",re.I)
REMOTE=re.compile(r"(?:remote|controller|pult|pultik|kic-7|kic-8|kic_|пульт)",re.I)

def check_file(p):
    with Image.open(p) as im:
        im.verify()
    return Image.open(p)

def clean_image(im):
    if getattr(im,"is_animated",False):
        im.seek(0)
    im=ImageOps.exif_transpose(im)
    if im.mode=="RGBA":
        base=Image.new("RGBA",im.size,"white")
        base.alpha_composite(im)
        im=base.convert("RGB")
    else:
        im=im.convert("RGB")
    return im

def bounds(im):
    # Strict RGB >242 is background as described by the user.
    # Preserve all non-white foreground and the entirety of the product.
    from PIL import ImageChops
    pix=im.load()
    threshold=Image.new("L",im.size)
    mark=threshold.load()
    for y in range(im.height):
        for x in range(im.width):
            r,g,b=pix[x,y]
            mark[x,y]=0 if (r>242 and g>242 and b>242) else 255
    return threshold.getbbox() or (0,0,im.width,im.height)

def square_image(im):
    im=clean_image(im)
    rect=bounds(im)
    im=im.crop(rect)
    im.thumbnail((750,750),Image.Resampling.LANCZOS)
    can=Image.new("RGB",(850,850),"white")
    can.paste(im,((850-im.width)//2,(850-im.height)//2))
    return can

def remote_preview(inner, remote):
    # Both inputs are foreground-cropped images, safely composited.
    inner=clean_image(inner).crop(bounds(clean_image(inner)))
    remote=clean_image(remote).crop(bounds(clean_image(remote)))
    inner.thumbnail((710,420), Image.Resampling.LANCZOS)
    remote.thumbnail((260,255), Image.Resampling.LANCZOS)
    can=Image.new("RGB",(850,850),"white")
    can.paste(inner,((850-inner.width)//2,85))
    can.paste(remote,((850-remote.width)//2,525+(255-remote.height)//2))
    return can

def imhash(im):
    z=im.convert("RGB").resize((64,64),Image.Resampling.LANCZOS)
    return hashlib.sha256(z.tobytes()).hexdigest()

def safe_component(s):
    return re.sub(r'[\\/:*?"<>|]','-',s)

def find_model_folder(unz, model):
    opts=[]
    for p in unz.rglob("manifest.json"):
        try:
            j=json.loads(p.read_text(encoding="utf-8"))
        except (ValueError,UnicodeDecodeError):
            continue
        if j.get("model")==model and j.get("brand")=="Kentatsu":
            opts.append((p.parent,j))
    if len(opts)!=1:
        raise ValueError("Expected one exact SKU manifest, found "+str(len(opts))+" for "+model)
    return opts[0]

def classify(link, ratio):
    if REMOTE.search(link) and 0.12<ratio<0.85: return "remote"
    # More conservative: no remote inference solely from a slim crop.
    return "indoor"

def main():
    rows=list(csv.DictReader(STATUS.open(encoding="utf-8-sig",newline="")))
    wanted=[r for r in rows if int(r["excel_row"]) in EXPECTED_ROWS]
    assert len(wanted)==15
    assert all(r["brand"]=="Kentatsu"
               and r["status"]=="COMPLETE" and r["zip_verified"]=="YES" for r in wanted)
    assert len({r["archive_download_url"] for r in wanted})==2
    OUT.mkdir(parents=True,exist_ok=True)
    unz=OUT/"_source-unpacked"
    for tag,archive in ARCHIVES.items():
        dest_unz=unz/tag
        with zipfile.ZipFile(archive) as f:
            bad=f.testzip()
            assert bad is None, f"Bad original ZIP member {bad}"
            for member in f.infolist():
                target=(dest_unz/member.filename).resolve()
                if not str(target).startswith(str(dest_unz.resolve())+os.sep):
                    raise ValueError("Unsafe ZIP path")
            f.extractall(dest_unz)
    entries=[]
    errors=[]
    qa=[]
    carddata=[]
    for r in wanted:
        model=r["model"]
        real_row=int(r["excel_row"])+(69 if int(r["excel_row"])>=54 else 0)
        series=re.match(r"^[A-Z]+",model).group(0)
        dest=OUT/series/safe_component(model)
        dest.mkdir(parents=True,exist_ok=True)
        info={"model":model,"excel_row":real_row,"source_url":r["source_url"],
              "source_zip":r["archive_download_url"],"images":[]}
        try:
            archive_tag=r["archive_download_url"].split("/releases/download/")[1].split("/")[0]
            folder,manifest=find_model_folder(unz/archive_tag,model)
            assert manifest.get("status") in ("COMPLETE","PARTIAL"), manifest.get("status")
            assert str(manifest.get("model"))==model
            raw=manifest.get("image_files") or []
            if not raw: raise ValueError("No manifest.product gallery")
            uniq={}
            for n,item in enumerate(raw):
                source=item.get("file","")
                url=item.get("url","")
                if NONPRODUCT.search(url) or NONPRODUCT.search(source):
                    qa.append((model,"EXCLUDED_NONPRODUCT_URL",url))
                    continue
                src=folder/"page_files"/source
                if not src.is_file():
                    qa.append((model,"MISSING_IMAGE_FILE",source))
                    continue
                try:
                    im=clean_image(check_file(src))
                    w,h=im.size
                    if min(w,h)<180 or max(w,h)<430:
                        qa.append((model,"EXCLUDED_TOO_SMALL",f"{w}x{h} {url}"))
                        continue
                    hashv=imhash(im)
                    kind=classify(url+" "+source,w/h)
                    filedata=dict(source_file=source,url=url,kind=kind,width=w,height=h,
                                  pixels=w*h,hash=hashv,im=im,order=n)
                    existing=uniq.get(hashv)
                    if existing is None or filedata["pixels"]>existing["pixels"]:
                        uniq[hashv]=filedata
                except Exception as exc:
                    qa.append((model,"BAD_IMAGE",f"{source}: {exc}"))
            files=sorted(uniq.values(),key=lambda d:d["order"])
            remotes=[x for x in files if x["kind"]=="remote"]
            indoor=[x for x in files if x["kind"]=="indoor"]
            if not indoor: raise ValueError("No valid indoor-product photos")
            # Every model retains its own model folder; no unverified series sharing.
            final=[]
            if remotes:
                p=dest/"01.jpg"
                remote_preview(indoor[0]["im"],remotes[0]["im"]).save(p,quality=94,subsampling=0)
                final.append(("preview",p,"confirmed remote filename"))
            for x in indoor+remotes:
                p=dest/f"{len(final)+1:02d}.jpg"
                square_image(x["im"]).save(p,quality=94,subsampling=0)
                final.append((x["kind"],p,x["url"]))
                status="NEEDS_SOURCE_QA" if min(x["width"],x["height"])<600 else "SOURCE_DIMENSIONS_OK"
                entries.append(dict(row=real_row,model=model,series=series,
                                    file=str(p.relative_to(OUT)),kind=x["kind"],
                                    source_image=x["url"],source_page=r["source_url"],
                                    source_width=x["width"],source_height=x["height"],
                                    source_quality=status))
            if not final: raise ValueError("No output JPG")
            for _,fp,_ in final:
                verify=Image.open(fp)
                if verify.format!="JPEG" or verify.size!=(850,850):
                    raise ValueError("Output format/size is wrong")
            info["images"]=[{"file":fp.name,"kind":kind,"source":src}
                            for kind,fp,src in final]
            info["source_quality_review_required"]=any(min(x["width"],x["height"])<600
                                                        for x in files)
            info["status"]="CURATED_AWAITING_VISUAL_QA"
            carddata.append((model, dest, final))
            print("RESULT",model,len(final),"JPG",flush=True)
        except Exception as exc:
            errors.append({"model":model,"error":str(exc)})
            info["status"]="ERROR"
            info["error"]=str(exc)
            print("ERROR",model,str(exc),flush=True)
        (dest/"SOURCES.json").write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding="utf-8")
    # Preview contact sheet in the same public deliverable, with clear model labels.
    tw,th=360,410
    sheet=Image.new("RGB",(tw*len(carddata),th),"white")
    draw=ImageDraw.Draw(sheet)
    for i,(model,folder,final) in enumerate(carddata):
        view=Image.open(final[0][1]);view.thumbnail((340,360))
        sheet.paste(view,(i*tw+(tw-view.width)//2,16))
        draw.text((i*tw+16,380),model,fill="black")
    sheet.save(OUT/"CONTACT_SHEET.png")
    with (OUT/"PHOTO_SOURCES.csv").open("w",encoding="utf-8-sig",newline="") as f:
        fields=["row","model","series","file","kind","source_image","source_page",
                "source_width","source_height","source_quality"]
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader();writer.writerows(entries)
    with (OUT/"REVIEW_NOTES.csv").open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.writer(f);writer.writerow(["model","event","detail"]);writer.writerows(qa)
    summary={"scope":"Unfilled current Excel rows 137-151 (archived inventory rows 68-82) ONLY",
             "source":"Archived exact-model HTML and gallery from catalog-377",
             "models_target":len(wanted),
             "models_with_jpg":len(carddata),
             "total_jpg":sum(len(f) for _,_,f in carddata),
             "image_source_rows":len(entries),
             "errors":errors,
             "qa_exclusions":len(qa),
             "quality_gate":"Automated image dimensions and manifest source verified; visual QA remains required",
             "originals_modified":False}
    (OUT/"SUMMARY.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    (OUT/"README.txt").write_text(
       "Серии KTGV, KTYV, KTZV — изображения для незалитых строк 137–151.\n"
       "Каждая модель имеет отдельный комплект JPG 850x850. "
       "Ракурсы берутся только из исходной товарной галереи архивного HTML.\n"
       "Статус: CURATED_AWAITING_VISUAL_QA, не выдавать за финально проверенные "
       "без просмотра CONTACT_SHEET.png и JPG по отдельности.\n"
       "Архивные HTML и фотофайлы не изменялись. PHOTO_SOURCES.csv содержит происхождение.\n",
       encoding="utf-8")
    # Do not include the downloaded original HTML or assets in generated ZIP;
    # deliver only final JPG and auditable textual metadata.
    shutil.rmtree(unz)
    path=OUT.parent/"Kentatsu_KTGV_KTYV_KTZV_images_v11.zip"
    with zipfile.ZipFile(path,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in OUT.rglob("*"):
            if f.is_file():
                z.write(f,f.relative_to(OUT))
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        assert len([x for x in z.namelist() if x.lower().endswith(".jpg")])==summary["total_jpg"]
    print("SUMMARY",json.dumps(summary,ensure_ascii=False),flush=True)
    if not carddata:
        raise SystemExit("No valid images to publish")
if __name__=="__main__":
    main()
