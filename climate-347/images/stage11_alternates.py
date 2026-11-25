import csv, hashlib, io, json, pathlib, re, zipfile, os, base64, subprocess
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps, ImageDraw
ROOT=pathlib.Path("climate-347/images")
OUT=pathlib.Path("stage11-out"); OUT.mkdir(exist_ok=True)
tag="climate347-images-stage10-45521367832"
subprocess.run(["gh","release","download",tag,"-p","Climate347_stage10_external_candidates.zip","-D",str(OUT)],check=True)
p=OUT/"Climate347_stage10_external_candidates.zip"
assert hashlib.sha256(p.read_bytes()).hexdigest()=="609050e1bbac3587d05b782645bb5c5fe1236a6d8c3f3008c43be16c76c00a43"
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    old=list(csv.DictReader(io.StringIO(z.read("download-results.csv").decode("utf-8"))))
    local=list(csv.DictReader((ROOT/"audits/stage-07-html-candidates.csv").open(encoding="utf-8"),delimiter=";"))
    matches=[]
    for r in old:
        if not r["file"]:continue
        data=z.read(r["file"])
        assert hashlib.sha256(data).hexdigest()==r["sha256"]
        eq=[a for a in local if a["SHA256"]==r["sha256"] and a["Model"]==r["model"]]
        matches.append(dict(model=r["model"],brand=r["brand"],width=r["width"],height=r["height"],sha256=r["sha256"],pixel_sha256=r["pixel_sha256"],exact_local_byte_matches=len(eq),local_paths=" | ".join(a["Local resource"] for a in eq),image=r["image"]))
    contacts=[n for n in z.namelist() if n.startswith("contact-") and n.endswith(".jpg")]
    for n in contacts:
        im=Image.open(io.BytesIO(z.read(n))).convert("RGB")
        im.thumbnail((1100,1600))
        bio=io.BytesIO();im.save(bio,format="JPEG",quality=72)
        (ROOT/"audits"/("stage-11-stage10-"+pathlib.Path(n).stem+".b64.txt")).write_text(base64.b64encode(bio.getvalue()).decode())
def writecsv(path,rows,fields=None):
    if not rows and fields is None:return
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
writecsv(ROOT/"audits/stage-11-stage10-comparison.csv",matches)
queue=[]
for r in csv.DictReader((ROOT/"audits/stage-10-download-queue.csv").open(encoding="utf-8"),delimiter=";"):
    m=r["model"];b=r["brand"]
    if b=="Kentatsu":
        queue.append((b,m,"https://kentatsuair.ru/catalog/naruzhnye_bloki_vrf_sistemy/kentatsu_"+m.lower()+"/"))
    elif b=="Midea" and "ULTRA" in m:
        queue.append((b,m,"https://midea-pro.ru/catalog/naruzhnye-bloki-vrf-sistemy/midea-"+m.lower().replace("(ultra)","-ultra")+"/"))
    elif b=="Midea" and m.startswith("MIH"):
        queue.append((b,m,"https://ryazan.vsekondicioneri.ru/category/vrv-sistemy/midea/?page="+("15" if m in ("MIH450FLHN18","MIH560FLHN18") else "14")))
queue.append(("IGC","IMBR-H440ANB","https://www.igc-aircon.com/product/modulnye_chillery_30_kw_2080_kw/"))
queue=list(dict.fromkeys(queue))
def get(url,ref=None):
    h={"User-Agent":"Mozilla/5.0 (compatible; product research)","Accept":"*/*"}
    if ref:h["Referer"]=ref
    with requests.get(url,headers=h,timeout=(8,20),stream=True) as r:
        r.raise_for_status(); d=bytearray()
        for c in r.iter_content(65536):
            d.extend(c)
            if len(d)>20_000_000:raise ValueError("size limit")
        return bytes(d),r.url
def norm(s):return re.sub(r"[^a-z0-9]","",s.lower())
def exact(text,m):
    return bool(re.search(r"(?<![A-Za-z0-9])"+re.escape(m)+r"(?![A-Za-z0-9])",text,re.I))
def safe(s):return re.sub(r"[^A-Za-z0-9_.()-]+","_",s)
def work(t):
    b,m,url=t
    results=[]
    def fail(msg):
        return [dict(brand=b,model=m,page=url,source="",status="FAILED",detail=str(msg)[:300],file="",sha256="",pixel_sha256="",width="",height="")]
    try:
        d,final=get(url);s=BeautifulSoup(d,"html.parser")
        # Follow actual product link in a listing, never assign series OG.
        h=" ".join(n.get_text(" ",strip=True) for n in s.find_all("h1"))
        if not exact(h,m):
            links=[]
            for a in s.find_all("a",href=True):
                txt=a.get_text(" ",strip=True)+" "+" ".join(x.get("alt","") for x in a.find_all("img"))
                if exact(txt,m) or norm(m) in norm(a["href"]):
                    u=urljoin(final,a["href"])
                    if u!=final and urlparse(u).netloc==urlparse(final).netloc:links.append(u)
            for u in list(dict.fromkeys(links))[:4]:
                try:
                    d2,f2=get(u);s2=BeautifulSoup(d2,"html.parser");h2=" ".join(n.get_text(" ",strip=True) for n in s2.find_all("h1"))
                    if exact(h2,m):s,final,h=s2,f2,h2;break
                except Exception:pass
            if not exact(h,m):
                # An explicitly model-labelled image on the listing is a separate candidate, not a product card.
                imgs=[i for i in s.find_all("img") if exact(i.get("alt","")+" "+i.get("title",""),m)]
                if not imgs:return fail("exact H1 or exact labeled listing image absent")
                mode="EXACT_LABEL_LISTING_NOT_CARD"
            else:imgs=[i for i in s.find_all("img") if exact(i.get("alt","")+" "+i.get("title",""),m)];mode="EXACT_H1"
        else:
            imgs=[i for i in s.find_all("img") if exact(i.get("alt","")+" "+i.get("title",""),m)];mode="EXACT_H1"
        urls=[]
        if mode=="EXACT_H1":
            og=s.find("meta",property="og:image")
            if og and og.get("content"):urls.append(og["content"])
        for i in imgs:
            for k in ["data-src","data-lazy","data-original","src"]:
                if i.get(k):urls.append(i[k])
            a=i.find_parent("a",href=True)
            if a and re.search(r"\.(jpe?g|png|webp)(\?|$)",a["href"],re.I):urls.append(a["href"])
        urls=list(dict.fromkeys(urljoin(final,u) for u in urls if u and not u.startswith("data:")))[:10]
        if not urls:return fail("no labelled or OG image")
        for u in urls:
            rec=dict(brand=b,model=m,page=final,source=u,status="",detail=mode,file="",sha256="",pixel_sha256="",width="",height="")
            try:
                data,f=get(u,final)
                with Image.open(io.BytesIO(data)) as im:
                    im.load();w,h=im.size
                    if min(w,h)<150:raise ValueError("thumbnail")
                    rgb=im.convert("RGB");sha=hashlib.sha256(data).hexdigest();pix=hashlib.sha256(f"{w}x{h}:".encode()+rgb.tobytes()).hexdigest()
                    ext={"JPEG":"jpg","PNG":"png","WEBP":"webp","AVIF":"avif"}.get(im.format)
                    if not ext:raise ValueError("format")
                    dest=OUT/"originals"/safe(b)/safe(m)/(sha[:16]+"."+ext);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
                    rec.update(status="CANDIDATE_NOT_APPROVED",file=str(dest.relative_to(OUT)),sha256=sha,pixel_sha256=pix,width=w,height=h)
            except Exception as e:rec.update(status="FAILED",detail=mode+" "+str(e)[:200])
            results.append(rec)
        return results
    except Exception as e:return fail(e)
with ThreadPoolExecutor(max_workers=8) as pool: new=[r for batch in pool.map(work,queue) for r in batch]
writecsv(ROOT/"audits/stage-11-alternative-sources.csv",new)
ok=[r for r in new if r["status"]=="CANDIDATE_NOT_APPROVED"]
uniq={}
for r in ok:uniq.setdefault(r["pixel_sha256"],r)
for k in range(0,len(uniq),12):
    grp=list(uniq.values())[k:k+12]; im=Image.new("RGB",(960,((len(grp)+2)//3)*235),"white");draw=ImageDraw.Draw(im)
    for i,r in enumerate(grp):
        x=i%3*320;y=i//3*235
        a=Image.open(OUT/r["file"]).convert("RGB");a=ImageOps.contain(a,(305,195));im.paste(a,(x+(320-a.width)//2,y))
        draw.text((x+5,y+196),r["model"],fill="black");draw.text((x+5,y+211),f'{r["width"]}x{r["height"]} {r["pixel_sha256"][:12]}',fill="black")
    b=io.BytesIO();im.save(b,format="JPEG",quality=75)
    (ROOT/"audits"/f"stage-11-new-contact-{k//12+1:02}.b64.txt").write_text(base64.b64encode(b.getvalue()).decode())
    (OUT/f"new-contact-{k//12+1:02}.jpg").write_bytes(b.getvalue())
summary=dict(stage10_verified_files=len(matches),stage10_exact_local_byte_matches=sum(x["exact_local_byte_matches"]>0 for x in matches),stage10_unique_pixels=len({x["pixel_sha256"] for x in matches}),alternative_models_targeted=len(queue),alternative_models_downloaded=len({(r["brand"],r["model"]) for r in ok}),alternative_files=len(ok),alternative_unique_pixels=len(uniq),new_pixel_hashes=len(set(uniq)-{x["pixel_sha256"] for x in matches}),h440_downloaded=any(r["model"]=="IMBR-H440ANB" for r in ok),approved=0)
(ROOT/"audits/stage-11-acquisition-summary.json").write_text(json.dumps(summary,indent=2))
with zipfile.ZipFile("Climate347_stage11_alternatives.zip","w",compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.suffix!=".zip":z.write(p,p.relative_to(OUT))
    for n in ["stage-11-stage10-comparison.csv","stage-11-alternative-sources.csv","stage-11-acquisition-summary.json"]:z.write(ROOT/"audits"/n,n)
with zipfile.ZipFile("Climate347_stage11_alternatives.zip") as z:assert z.testzip() is None
print(json.dumps(summary))
