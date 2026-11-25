import csv, hashlib, io, json, pathlib, re, zipfile, os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps, ImageDraw
ROOT=pathlib.Path("climate-347/images")
OUT=pathlib.Path("stage10-out"); OUT.mkdir(exist_ok=True)
headers={"User-Agent":"Mozilla/5.0 (compatible; product research; public image acquisition)","Accept":"image/avif,image/webp,image/png,image/jpeg,*/*;q=0.8"}
queue=list(csv.DictReader((ROOT/"audits/stage-10-download-queue.csv").open(encoding="utf-8"),delimiter=";"))
def safe(s): return re.sub(r'[^A-Za-z0-9_.()-]+','_',s)
def get(url,referer=None,maxsize=20_000_000):
    h=dict(headers)
    if referer:h["Referer"]=referer
    with requests.get(url,headers=h,timeout=(8,18),stream=True) as r:
        r.raise_for_status()
        data=bytearray()
        for chunk in r.iter_content(65536):
            data.extend(chunk)
            if len(data)>maxsize:raise ValueError("size cap")
        return bytes(data),r.url
def task(r):
    brand,model,page,url,basis=(r[k] for k in ("brand","model","page","image","basis"))
    rec=dict(r)
    rec.update(status="",detail="",file="",sha256="",pixel_sha256="",width="",height="",final_url="")
    try:
        if not url:
            if basis=="EXTERNAL_SERIES_LIST_ONLY":
                rec["status"]="SERIES_LIST_NO_EXACT_IMAGE"; return rec
            data,final=get(page)
            soup=BeautifulSoup(data,"html.parser")
            h1=" ".join(t.get_text(" ",strip=True) for t in soup.find_all("h1"))
            if model.casefold() not in h1.casefold():raise ValueError("exact H1 absent")
            tag=soup.find("meta",property="og:image")
            if not tag or not tag.get("content"):raise ValueError("no OG image")
            url=urljoin(final,tag["content"])
        rec["image"]=url
        data,final=get(url,page)
        with Image.open(io.BytesIO(data)) as im:
            fmt=im.format
            im.load()
            rgb=im.convert("RGB")
            w,h=im.size
            if fmt not in ("JPEG","PNG","WEBP","AVIF"):raise ValueError("not supported raster "+str(fmt))
            if w*h>35_000_000:raise ValueError("pixel cap")
            sha=hashlib.sha256(data).hexdigest()
            ext={"JPEG":"jpg","PNG":"png","WEBP":"webp","AVIF":"avif"}[fmt]
            dest=OUT/"originals"/safe(brand)/safe(model)/(sha[:16]+"."+ext);dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(data)
            rec.update(status="DOWNLOADED_CANDIDATE_NOT_APPROVED",file=str(dest.relative_to(OUT)),sha256=sha,pixel_sha256=hashlib.sha256(f"{w}x{h}:".encode()+rgb.tobytes()).hexdigest(),width=w,height=h,final_url=final)
    except Exception as e:rec.update(status="FAILED",detail=str(e)[:300])
    return rec
with ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(task,queue))
fields=list(rows[0])
with (OUT/"download-results.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
ok=[r for r in rows if r["status"].startswith("DOWNLOADED")]
unique={}
for r in ok:unique.setdefault(r["pixel_sha256"],r)
for n in range(0,len(unique),24):
    group=list(unique.values())[n:n+24]
    contact=Image.new("RGB",(1200,((len(group)+3)//4)*245),"white");d=ImageDraw.Draw(contact)
    for i,r in enumerate(group):
        x=(i%4)*300;y=(i//4)*245
        with Image.open(OUT/r["file"]) as im:
            im=ImageOps.contain(im.convert("RGB"),(285,197))
            contact.paste(im,(x+(300-im.width)//2,y))
        d.text((x+5,y+200),r["model"],fill="black")
        d.text((x+5,y+216),f'{r["width"]}x{r["height"]} {r["sha256"][:10]}',fill="black")
    contact.save(OUT/f"contact-{n//24+1:02}.jpg",quality=92)
summary={"queue_rows":len(rows),"queue_models":len({(r["brand"],r["model"]) for r in rows}),"downloaded_rows":len(ok),"downloaded_models":len({(r["brand"],r["model"]) for r in ok}),"unique_pixels":len(unique),"failed_rows":len(rows)-len(ok),"approved_models":0}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2))
with zipfile.ZipFile("Climate347_stage10_external_candidates.zip","w",compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob("*")):
        if p.is_file():z.write(p,p.relative_to(OUT))
with zipfile.ZipFile("Climate347_stage10_external_candidates.zip") as z:
    assert z.testzip() is None
print(json.dumps(summary))
