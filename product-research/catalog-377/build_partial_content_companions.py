#!/usr/bin/env python3
"""40 attributed factual product-description companions, never fake original HTML.

Input: exact SKU pages from already independently verified public GitHub
Release ZIPs. Extract *only* the active product's first detailed specification
table, before the related-products area. Avoid other products' table data.
Output: original newly authored 1-3-sentence Russian descriptions, verified
field evidence, source links, status. The third-party source HTML remains
unchanged and is NOT embedded in this new archive.
"""
import csv,hashlib,io,json,re,subprocess,tempfile,time,zipfile
from collections import Counter,defaultdict
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path("product-research/catalog-377")
OUT=ROOT/"content-companions"
OUT.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((ROOT/"status/master_status.csv").open(encoding="utf-8-sig",newline="")))
targets=[x for x in rows if x["status"]=="PARTIAL"]
assert len(targets)==40,len(targets)
def safe(s):return re.sub(r"[^A-Za-z0-9._-]","_",str(s)).strip("_")[:85]
def matches(model,text):
    sku=re.sub(r"\s+","",model).upper()
    pat=re.escape(sku).replace(r"\(",r"\s*\(")
    return bool(re.search(r"(?<![A-Z0-9])"+pat+r"(?![A-Z0-9(])",str(text).upper()))
def getfields(soup):
    """Read first actual product table, never the recommendation widget."""
    current={}
    active=False
    seen_start=False
    for tr in soup.select("tr"):
        cells=[c.get_text(" ",strip=True) for c in tr.find_all(["td","th"],recursive=False)]
        if len(cells)!=2:continue
        k,v=(c.strip() for c in cells)
        if k=="На площадь (м2)":
            if seen_start:break # first recommendations product begins here
            active=True
            seen_start=True
        if active and k and v and k not in current:
            current[k]=v
    return current

def download(tag,name,destination):
    for attempt in range(5):
        try:
            p=subprocess.run(
             ["gh","release","download",tag,"--repo","kubenkoi97-cmyk/work-files-public",
               "--pattern",name,"--dir",str(destination),"--clobber"],
             text=True,capture_output=True,timeout=120)
            f=destination/name
            if p.returncode==0 and f.exists() and f.stat().st_size>1000:
                return f,""
            err=(p.stderr or p.stdout)[:170]
        except Exception as e:
            err=str(e)[:170]
        print("RETRY",tag,attempt+1,err,flush=True)
        time.sleep(2+2*attempt)
    return None,err

def sentence(brand,model,fields):
    """No unverified feature claims, only fields verbatim from exact SKU."""
    typ=fields.get("Тип внутреннего блока","").lower()
    series=fields.get("Серия","")
    cool=fields.get("Охлаждение (кВт)") or fields.get("Охлаждение, кВт")
    warm=fields.get("Обогрев (кВт)") or fields.get("Обогрев, кВт")
    air=fields.get("Расход воздуха (м3/час)")
    noise=fields.get("Уровень шума (дБ)")
    dims=fields.get("Габариты внутреннего блока ШхВхГ (мм)")
    if not (typ and cool and warm):
        return "",["Missing product-specific type or cooling/heating field"]
    parts=[f"{brand} {model} — {typ} внутренний блок VRF-системы"+(f" серии {series}" if series else "")+"."]
    parts.append(f"По характеристикам продавца, производительность охлаждения составляет {cool} кВт, обогрева — {warm} кВт.")
    attrs=[]
    if air:attrs.append(f"расход воздуха {air} м³/ч")
    if noise:attrs.append(f"уровень шума {noise} дБ")
    if dims:attrs.append(f"габариты блока {dims} мм")
    if attrs: parts.append("Указаны также: "+", ".join(attrs)+".")
    return " ".join(parts),[]
manifest=[]
with tempfile.TemporaryDirectory() as tmp:
    byrelease=defaultdict(list)
    for row in targets:
        m=re.search(r"/releases/download/([^/]+)/([^/]+\.zip)",row["archive_download_url"])
        assert m,(row["brand"],row["model"])
        byrelease[(m.group(1),m.group(2))].append(row)
    for (tag,name),model_rows in sorted(byrelease.items()):
        file,error=download(tag,name,Path(tmp))
        if not file:
            for row in model_rows:
                manifest.append(dict(brand=row["brand"],model=row["model"],
                    result="ARCHIVE_UNAVAILABLE",issue=error,source_url=row["source_url"],
                    original_archive=row["archive_download_url"]))
            continue
        with zipfile.ZipFile(file) as z:
            assert z.testzip() is None,"Corrupt original source ZIP "+tag
            members=set(z.namelist())
            for row in model_rows:
                brand,model=row["brand"],row["model"]
                dirname="products/"+brand+"_"+safe(model)
                html=dirname+"/original.html"
                original_manifest=dirname+"/manifest.json"
                result=dict(brand=brand,model=model,source_url=row["source_url"],
                    original_archive=row["archive_download_url"],
                    original_source_status="PARTIAL",
                    companion_not_original_html=True)
                if html not in members or original_manifest not in members:
                    result.update(result="SOURCE_MISSING",issue="No original HTML/manifest for exact model")
                    manifest.append(result);continue
                raw=z.read(html)
                soup=BeautifulSoup(raw.decode("utf-8","replace"),"html.parser")
                heading=" ".join(h.get_text(" ",strip=True) for h in soup.find_all("h1"))
                title=soup.title.get_text(" ",strip=True) if soup.title else ""
                if not matches(model,heading+" "+title) or brand.lower() not in (heading+" "+title).lower():
                    result.update(result="WRONG_MODEL",issue="Exact SKU or brand missing from heading")
                    manifest.append(result);continue
                source_manifest=json.loads(z.read(original_manifest))
                if source_manifest.get("model")!=model or not source_manifest.get("image_files"):
                    result.update(result="SOURCE_INCOMPLETE",issue="Source metadata mismatch or missing photo list")
                    manifest.append(result);continue
                fields=getfields(soup)
                original_description,errs=sentence(brand,model,fields)
                result.update(
                    raw_html_sha256=hashlib.sha256(raw).hexdigest(),
                    extracted_fields_count=len(fields),
                    original_gallery_image_count=len(source_manifest.get("image_files",[])),
                    source_is_original_html=True,
                    generated_description=original_description,
                    original_page_has_separate_description=False,
                    result="COMPANION_READY" if original_description else "FIELD_EXTRACTION_FAILED",
                    issue="; ".join(errs) if errs else ""
                )
                productdir=OUT/(brand+"_"+safe(model))
                productdir.mkdir(parents=True,exist_ok=True)
                (productdir/"verified_fields.json").write_text(
                    json.dumps({"brand":brand,"model":model,"source_html_url":row["source_url"],
                     "html_source_sha256":result["raw_html_sha256"],
                     "source_archive":row["archive_download_url"],
                     "fields":fields,"is_vendor_description":False},ensure_ascii=False,indent=2),
                    encoding="utf-8")
                (productdir/"factual_description.md").write_text(
                    "# "+brand+" "+model+"\n\n"
                    +"**Авторское описание на основе характеристик оригинальной карточки; не оригинальный текст продавца.**\n\n"
                    +(original_description if original_description else "*Недостаточно подтвержденных полей для описания.*")
                    +"\n\nИсточник: "+row["source_url"]+"\nОригинальный HTML: "+row["archive_download_url"]+"\n",
                    encoding="utf-8")
                manifest.append(result)
                print("COMPANION",brand,model,result["result"],"SPECS",len(fields),flush=True)
manifest.sort(key=lambda x:(x["brand"],x["model"]))
assert len(manifest)==40,len(manifest)
(OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
counts=Counter(r["result"] for r in manifest)
summary=dict(
    input_partial_models=40,results=dict(counts),
    authentic_existing_original_html_unchanged=True,
    facts_source="independently verified original exact-model HTML supplier specification tables",
    generated_text_is_not_vendor_description=True,
    note="No product description added to or passed off as original retailer HTML")
(OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
zipfile_path=ROOT/"output/catalog377-40-factual-content-companions.zip"
zipfile_path.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(zipfile_path,"w",compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob("*")):
        if p.is_file():z.write(p,p.relative_to(OUT))
print("COMPANION_COMPLETE",json.dumps(summary,ensure_ascii=False),zipfile_path.stat().st_size,flush=True)
