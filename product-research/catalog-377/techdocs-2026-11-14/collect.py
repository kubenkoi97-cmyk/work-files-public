#!/usr/bin/env python3
"""Series-based verified technical PDF collection for the 377 unfilled MIXED catalog rows."""
import csv, hashlib, json, os, re, shutil, time, zipfile
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlparse
import fitz, requests

ROOT=Path("product-research/catalog-377/techdocs-2026-11-14")
INVENTORY=ROOT/"series_inventory.csv"
OUT=ROOT/"output"
SHARED=OUT/"Общие каталоги"
SESSION=requests.Session()
SESSION.headers.update({"User-Agent":"Mozilla/5.0 (compatible; HVAC-document-inventory/1.0)"})
SOURCES=[
 ("Kentatsu","DX_PRO_2025_2026","https://www.c-o-k.ru/library/catalogs/kentatsu/140011.pdf","full"),
 ("Kentatsu","DX_PRO_2023","https://kentatsu.group/wa-content/docs/vrf.pdf","full"),
 ("Midea","VRF_2024_2025","https://www.thermotrade.ru/wp-content/uploads/2024/08/midea_vrf_2024-2025.pdf","full"),
 ("Midea","ATOM_2024","https://www.midea.com/content/dam/midea-aem/id/PD-Midea-Atom-Catalogue-2024-12-25-V7-1.pdf","full"),
 ("IGC","VRF_technical","https://www.c-o-k.ru/library/instructions/igc/kondicionery-promyshlennye/38333/141247.pdf","full"),
 ("Daikin","FXKQ_A_technical","https://easyspec.daikin.fr/EasySpec/VRV/Documentations/UI/J4_FXKQ-A/Manuel%20technique/ManTech_J4_FXKQ-A.pdf","technical_data"),
 ("Daikin","FXMQ_A_user_installation","https://www.daikin.eu/content/dam/document-library/installation-manuals/ac/vrv/fxmq-a/FXMQ-A_Installation.Operation%20manual_3PRU701545-1C_Russian.pdf","installation_and_user_manual"),
 ("Bosch","AF_4CC_manual","https://daichi.ru/upload/iblock/c0f/0z4lvnkh1hkuv0x99wg2j4ta7nex092n/AF-4CC%20%D0%BA%D0%B0%D1%81%D1%81%D0%B5%D1%82%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%82%D0%B8%D0%BF%D0%B0%20%20600%D1%85600.pdf","installation_and_user_manual"),
 ("Midea","MIH_G_manual","https://air-midea.com/upload/iblock/5fa/w3uwwedt34zlvayeyypdf82w8bqe3b4d.pdf","installation_and_user_manual"),
 ("Midea","MIH_G_DP_manual","https://daichi.ru/upload/iblock/e3f/1r0uk23yt3xq50hbmhmd4ctbrsbow353/IOM_Wall-mounted_MIH_GHN18%28DP%29_11_07_25.pdf","installation_and_user_manual"),
 ("Midea","VRF_V8_2025_2026","https://www.c-o-k.ru/library/catalogs/midea/140017.pdf","full"),
 ("Midea","MIH_B_installation_manual","https://daichi.ru/upload/iblock/068/zdvzisq2aftnxqjjx296ou262ldcznn5/IOM%2BWall-mounted%20MIH_BHN18_250924.pdf","installation_and_user_manual"),
 ("Midea","MIH_B_technical","https://air-midea.com/upload/iblock/bc5/hv485zb0phwxgxczuo2lyb34669g2d21.pdf","technical_data"),
 ("IGC","VRF_legacy_DC_catalogue","https://www.c-o-k.ru/library/catalogs/igc/38195/140669.pdf","full"),
 ("IGC","VRF_official_technical","https://www.nsk.igc-aircon.com/upload/iblock/8e1/f2umkqwfiqx3p6b65iz03odbvjqw01vo.pdf","full"),
 ("Daikin","VRV_2026","https://www.daikin.at/content/dam/DACE-AT/document-library/catalogues/ac/vrv/Daikin_Katalog_VRV_2026.pdf","full"),

]
def norm(x): return re.sub(r"\s+","",str(x).upper())
def exact(model, text):
    # Preserve actual whitespace between PDF table cells and lines. Removing all
    # whitespace from the entire page merges adjacent model IDs and loses matches.
    m=norm(model)
    pattern=r"(?<![A-Z0-9])"+r"\s*".join(re.escape(c) for c in m)+r"(?![A-Z0-9])"
    if "(" not in m:
        pattern+=r"(?!\s*\()"  # do not confuse a base SKU with a suffixed variant
    return bool(re.search(pattern,str(text).upper()))

def download(url, maxmb=90):
    for trial in range(2):
        try:
            r=SESSION.get(url, timeout=(14,85),allow_redirects=True)
            r.raise_for_status()
            data=r.content
            if len(data)>maxmb*1024*1024: raise ValueError("oversize")
            if not data[:5]==b"%PDF-": raise ValueError("response not PDF")
            d=fitz.open(stream=data,filetype="pdf")
            if len(d)<1: raise ValueError("zero pages")
            return data,r.url,d
        except Exception as e:
            err=str(e)
            if trial==0:time.sleep(2)
    raise RuntimeError(err)
def safe_redact_pagenumbers(page):
    count=0
    bounds=page.rect
    for block in page.get_text("blocks"):
        x0,y0,x1,y1,text,*_=block
        t=text.strip()
        if not re.fullmatch(r"\d{1,3}",t):continue
        if not (y0>bounds.height*.90 or y1<bounds.height*.05):continue
        if not (x1<bounds.width*.2 or x0>bounds.width*.8 or abs((x0+x1)/2-bounds.width/2)<bounds.width*.09):continue
        page.add_redact_annot(fitz.Rect(x0-1,y0-1,x1+1,y1+1),fill=(1,1,1));count+=1
    if count: page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
    return count
def docsuffix(typ): return typ
def fileunique(dir,base,data):
    p=dir/base
    if p.exists():
        if hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(data).digest():return p,False
        i=2
        while (dir/(p.stem+"_"+str(i)+".pdf")).exists():i+=1
        p=dir/(p.stem+"_"+str(i)+".pdf")
    p.write_bytes(data);return p,True

with INVENTORY.open(encoding="utf-8-sig",newline="") as f:rows=list(csv.DictReader(f))
assert len(rows)==377 and len({(r["brand"],r["model"]) for r in rows})==377
assert all(r["scope"]=="UNFILLED_ONLY" for r in rows)
groups=defaultdict(list)
for row in rows:groups[(row["brand"],row["series_key"])].append(row)
assert len(groups)==53,len(groups)
OUT.mkdir(parents=True,exist_ok=True)
SHARED.mkdir(parents=True,exist_ok=True)
status={}
results=[]
catalogue_data=[]
for brand,tag,url,typ in SOURCES:
    try:
        raw,final_url,doc=download(url)
        sha=hashlib.sha256(raw).hexdigest()
        info={"brand":brand,"tag":tag,"type":typ,"url":url,"final_url":final_url,"sha256":sha,"bytes":len(raw),"pages":len(doc),"status":"DOWNLOADED"}
        if typ=="full":
            dest=SHARED/(brand+"_"+tag)
            dest.mkdir(parents=True,exist_ok=True)
            path=dest/"Полный каталог.pdf"
            path.write_bytes(raw)
            info["path"]=str(path.relative_to(OUT))
        else:
            info["path"]="document-to-match"
        catalogue_data.append((info,doc,raw))
        results.append(info.copy())
        print("FETCH_OK",tag,"PAGES",len(doc),"BYTES",len(raw),flush=True)
    except Exception as e:
        results.append({"brand":brand,"tag":tag,"url":url,"status":"FAILED","error":str(e)[:200]})
        print("FETCH_FAIL",tag,str(e)[:200],flush=True)
for (brand,key),modelrows in groups.items():
    models=[r["model"] for r in modelrows]
    path=OUT/brand/key
    path.mkdir(parents=True,exist_ok=True)
    grp={"brand":brand,"series":key,"models":models,"catalogue_pages":[],"documents":[],"status":"NOT_VERIFIED"}
    for src,doc,raw in catalogue_data:
        if src["brand"]!=brand:continue
        if src["type"]=="full":
            page_hits=[]
            for idx,page in enumerate(doc):
                if idx<3:continue
                t=page.get_text()
                # Only pages with exact SKU identity, not nearby-series family marketing.
                matches=[m for m in models if exact(m,t)]
                if matches:page_hits.append((idx,matches))
            # Pages listing 4+ DIFFERENT SKU families are probably a model overview.
            picked=[]
            for idx,matches in page_hits:
                pg=doc[idx]
                if len(pg.get_text())<150:continue
                picked.append(idx)
            if picked:
                part=fitz.open();cleaned=0
                for idx in picked:
                    part.insert_pdf(doc,from_page=idx,to_page=idx)
                for p in part: cleaned+=safe_redact_pagenumbers(p)
                b=part.tobytes(garbage=4,deflate=True)
                suffix="catalog" if not grp["catalogue_pages"] else "catalog_"+src["tag"].lower()
                f,_=fileunique(path,key+"_"+suffix+".pdf",b)
                grp["catalogue_pages"].append({"catalogue":src["tag"],"pdf":f.name,"pdf_pages":[x+1 for x in picked],"numbers_removed":cleaned,"models_seen":sorted(set(m for i,mm in page_hits for m in mm))})
        else:
            # Manuals are associated only if at least one exact model appears.
            text="\n".join(page.get_text() for page in doc)
            matching=[m for m in models if exact(m,text)]
            # A generic group title is insufficient to claim an exact variant.
            if matching:
                f,_=fileunique(path,key+"_"+docsuffix(src["type"])+".pdf",raw)
                grp["documents"].append({"document":f.name,"source":src["tag"],"verified_models":matching})
    grp["status"]="PARTIAL_VERIFIED" if grp["documents"] or grp["catalogue_pages"] else "NO_EXACT_MODEL_IN_DOWNLOADED_PDFS"
    status[key]=grp
    (path/"source_notes.txt").write_text("Brand: "+brand+"\nSeries grouping: "+key+"\nScope: only unfilled catalog rows\nModels:\n"+"\n".join(models)+"\nStatus: "+grp["status"]+"\n\nThis series grouping is preliminary until manufacturer series nomenclature is cross-checked.\n",encoding="utf-8")
    print("SERIES",brand,key,len(models),"CATALOGUES",len(grp["catalogue_pages"]),"MANUALS",len(grp["documents"]),flush=True)
report=ROOT/"series_documents_report.csv"
with report.open("w",encoding="utf-8-sig",newline="") as fh:
    w=csv.writer(fh);w.writerow(["brand","series","models","status","catalogue_excerpts","manuals","source_pdf_pages","models_list"])
    for (brand,key),g in groups.items():
        s=status[key]
        w.writerow([brand,key,len(g),s["status"],len(s["catalogue_pages"]),len(s["documents"]),"; ".join(x["catalogue"]+":"+",".join(map(str,x["pdf_pages"])) for x in s["catalogue_pages"])," | ".join(s["models"])])
(OUT/"report.txt").write_text("Scope: EXACT 377 models without fill in sheet КАТАЛОГ 744.\nGrouping: 53 preliminary series.\nDownloaded PDFs: "+str(sum(s["status"]=="DOWNLOADED" for s in results))+"/"+str(len(results))+".\n"+"Model series verified by exact matching text: "+str(sum(x["status"]=="PARTIAL_VERIFIED" for x in status.values()))+"/"+str(len(status))+".\nCatalogue snippets contain only pages with exact SKU strings. Original full catalogues are unchanged.\nExcerpts have standalone page numbers removed when detectable in margins. Unconfirmed series are explicitly not complete.\n"+"Sources:\n"+"\n".join(s["tag"]+" | "+s["status"]+" | "+s["url"] for s in results)+"\n",encoding="utf-8")
(OUT/"audit.json").write_text(json.dumps({"models":377,"series":53,"downloaded_sources":results,"series_report":list(status.values())},ensure_ascii=False,indent=2),encoding="utf-8")
target=ROOT/"MIXED_377_technical_docs_by_series_2026-11-14.zip"
with zipfile.ZipFile(target,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for f in OUT.rglob("*"):
        if f.is_file(): z.write(f,f.relative_to(OUT))
with zipfile.ZipFile(target) as z:
    bad=z.testzip()
    assert bad is None,bad
    entries=z.namelist()
    assert "report.txt" in entries and "audit.json" in entries
print("OUTPUT",str(target),"BYTES",target.stat().st_size,"SERIES_WITH_PDF",sum(x["status"]=="PARTIAL_VERIFIED" for x in status.values()),flush=True)
