#!/usr/bin/env python3
"""Supplement verified-v4 archive with newly discovered exact/model-family documentation.
All 377 source SKU scope is unchanged. Group-family-only sources remain explicitly qualified.
"""
from pathlib import Path
from collections import defaultdict
from io import BytesIO
import csv, fitz, hashlib, json, re, requests, sys, zipfile

inp_path=Path(sys.argv[1]);out_path=Path(sys.argv[2])
session=requests.Session();session.headers.update({"User-Agent":"Mozilla/5.0"})
with zipfile.ZipFile(inp_path) as zin:
    raw={n:zin.read(n) for n in zin.namelist() if not n.endswith("/")}
assert "audit.json" in raw and "deduplication_manifest.json" in raw
audit=json.loads(raw["audit.json"])
existing={x["series"]:x for x in audit["series_report"]}
supplemental=[]
def norm(s):
    return re.sub(r"\s+","",str(s).upper())
def exact(model,t):
    m=norm(model)
    pattern=r"(?<![A-Z0-9])"+r"\s*".join(map(re.escape,m))+r"(?![A-Z0-9])"
    if "(" not in m:pattern+=r"(?!\s*\()"
    return bool(re.search(pattern,t.upper()))
def download_pdf(url,label):
    try:
        r=session.get(url,timeout=(15,65));r.raise_for_status()
        if not r.content.startswith(b"%PDF-"):raise ValueError("Not a PDF")
        doc=fitz.open(stream=r.content,filetype="pdf")
        print("FETCH_OK",label,len(doc),"PAGES",len(r.content),"BYTES",flush=True)
        return r.content,doc
    except Exception as exc:
        print("FETCH_FAIL",label,str(exc)[:180],flush=True)
        return None,None
def remove_page_numbers(page):
    bounds=page.rect;count=0
    for b in page.get_text("blocks"):
        x0,y0,x1,y1,txt,*_=b
        t=txt.strip()
        if re.fullmatch(r"\d{1,3}",t) and (y0>bounds.height*.9 or y1<bounds.height*.05) and (x1<bounds.width*.2 or x0>bounds.width*.8 or abs((x0+x1)/2-bounds.width/2)<bounds.width*.09):
            page.add_redact_annot(fitz.Rect(x0-1,y0-1,x1+1,y1+1),fill=(1,1,1));count+=1
    if count:page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
    return count
def excerpt(doc,indices):
    result=fitz.open()
    for i in sorted(set(indices)):result.insert_pdf(doc,from_page=i,to_page=i)
    removed=sum(remove_page_numbers(p) for p in result)
    return result.tobytes(garbage=4,deflate=True),removed

# 1. Manufacturer manual explicitly names compact cassette DC5 variants.
igc_url="https://igc-aircon.com/upload/iblock/2fd/g7gqb0wx6uqkoxuz7qf9lnhfzsxzpmks.pdf"
b,d=download_pdf(igc_url,"IGC_IMS6_original_user_install")
if b:
    model_list=existing["IMS_4TM"]["models"]
    hit={m:[i+1 for i,p in enumerate(d) if exact(m,p.get_text())] for m in model_list}
    matched={k:v for k,v in hit.items() if v}
    if matched:
        path="IGC/IMS_4TM/IMS_4TM_installation_and_user_manual.pdf"
        raw[path]=b
        supplemental.append({"series":"IMS_4TM","path":path,"proof":"EXACT_SKU_IN_MANUFACTURER_PDF","exact_models":matched,"unmatched_models":sorted(set(model_list)-set(matched)),"source_url":igc_url,"original_unchanged":True})
        print("IGC_EXACT_MODELS",json.dumps(matched,ensure_ascii=False),flush=True)

# 2. Family-level DP variant explicitly described in Midea original full catalogue.
for cat in ("Общие каталоги/Midea_VRF_V8_2025_2026/Полный каталог.pdf",
            "Общие каталоги/Midea_ATOM_2024/Полный каталог.pdf"):
    if cat not in raw:continue
    d=fitz.open(stream=raw[cat],filetype="pdf")
    matched=[i for i,p in enumerate(d) if ("MI2_GDHN18" in norm(p.get_text()) and "DP" in p.get_text().upper()) or "MI2_GDHN18(AT)DP" in norm(p.get_text())]
    if matched:
        clip,removed=excerpt(d,matched[:7])
        path="Midea/MI2_G_DP/MI2_G_DP_catalog.pdf"
        raw[path]=clip
        supplemental.append({"series":"MI2_G_DP","path":path,"proof":"SERIES_LEVEL_ONLY_DP_FAMILY_HEADING","exact_models":{},"source_catalog":cat,"catalog_pdf_pages":[i+1 for i in matched[:7]],"page_numbers_removed":removed,"warning":"MI2_GDHN18(At)DP family documented; individual full DP SKU strings not confirmed in PDF table."})
        print("MIDEA_DP_FAMILY_PAGES",[i+1 for i in matched[:7]],flush=True)
        break

# 3. See whether a true MI2-DL family page occurs in existing manufacturer sources.
for cat in ("Общие каталоги/Midea_VRF_V8_2025_2026/Полный каталог.pdf",
            "Общие каталоги/Midea_VRF_2024_2025/Полный каталог.pdf",
            "Общие каталоги/Midea_ATOM_2024/Полный каталог.pdf"):
    if cat not in raw:continue
    d=fitz.open(stream=raw[cat],filetype="pdf")
    matched=[]
    for i,p in enumerate(d):
        t=p.get_text()
        # Model series nomenclature alone is permissible for partial series evidence,
        # but not for attributing numeric exact SKU specifications.
        if re.search(r"MI2[\-_\s]*DL\b|MI2[\-_\s]*DLDHN18",t,re.I):matched.append(i)
    if matched:
        clip,removed=excerpt(d,matched[:7])
        path="Midea/MI2_DL/MI2_DL_catalog.pdf"
        raw[path]=clip
        supplemental.append({"series":"MI2_DL","path":path,"proof":"SERIES_LEVEL_ONLY_MODEL_SPECIFICATIONS_NOT_CONFIRMED","exact_models":{},"source_catalog":cat,"catalog_pdf_pages":[i+1 for i in matched[:7]],"page_numbers_removed":removed})
        print("MIDEA_DL_FAMILY_PAGES",[i+1 for i in matched[:7]],flush=True)
        break

# 4. Additional original Kentatsu overview, use ONLY series-only scope status for families
# not present in other PDFs. Keep original whole catalogue as-is.
kent_url="https://www.c-o-k.ru/library/catalogs/kentatsu/38188/140639.pdf"
b,d=download_pdf(kent_url,"Kentatsu_2026_nomenclature")
if b:
    full="Общие каталоги/Kentatsu_2026_Nomenclature/Полный каталог.pdf"
    raw[full]=b
    for series in ("KTZV","KTLV","KTKV","KTHV","KTGB"):
        hits=[]
        for i,p in enumerate(d):
            text=p.get_text()
            if re.search(r"(?<![A-Z0-9])"+series+r"(?![A-Z0-9])",text.upper()):hits.append(i)
        if hits:
            # Prefer only a few directly related overview pages; other series can
            # share the source page, so these cannot be described as technical datasheets.
            clip,removed=excerpt(d,hits[:3])
            path="Kentatsu/"+series+"/"+series+"_catalog.pdf"
            raw[path]=clip
            supplemental.append({"series":series,"path":path,"proof":"SERIES_LEVEL_ONLY_OVERVIEW","exact_models":{},"source_catalog":full,"catalog_pdf_pages":[i+1 for i in hits[:3]],"page_numbers_removed":removed,"warning":"Series family identified in official source. Individual numerical SKU and technical parameters remain unverified."})
            print("KENTATSU_SERIES_OVERVIEW",series,[i+1 for i in hits[:3]],flush=True)

# Dedup once again by file content within each brand/series.
kept={};final={}
removed=[]
def priority(name):
    if "_installation_and_user_manual.pdf" in name:return (0,name)
    if "_catalog.pdf" in name:return (1,name)
    return (2,name)
for path,data in sorted(raw.items(),key=lambda kv:priority(kv[0])):
    sha=hashlib.sha256(data).hexdigest()
    if path.lower().endswith(".pdf"):
        folder=path.rsplit("/",1)[0]
        scope=(path.split("/")[1].split("_")[0]+"_full_catalog") if path.startswith("Общие каталоги/") else folder
        key=(scope,sha)
        if key in kept:
            removed.append({"skipped":path,"kept":kept[key]})
            continue
        kept[key]=path
    final[path]=data

notes={
 "scope":"ONLY 377 unfilled models in Каталог 744; 53 preliminary groups; original Excel unchanged",
 "version":"v5 supplementary sources layered on verified de-duplicated v4",
 "supplemental_evidence":supplemental,
 "additional_duplicates_removed":removed,
 "status_semantics":"EXACT_SKU_IN_MANUFACTURER_PDF means only listed SKUs verified. SERIES_LEVEL_ONLY means generic family proof, not exact SKU technical verification.",
 "caveats":"Manual and overview PDFs may cover multiple HVAC series. Original full catalogues preserved. Group page excerpts are subsets containing relevant models/family and may include adjacent content on mixed pages.",
}
final["supplemental_v5_evidence.json"]=json.dumps(notes,ensure_ascii=False,indent=2).encode("utf-8")
with zipfile.ZipFile(out_path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as zout:
    for p,data in final.items():zout.writestr(p,data)
with zipfile.ZipFile(out_path) as z:
    assert z.testzip() is None
    pdfs=[n for n in z.namelist() if n.lower().endswith(".pdf")]
    full=[n for n in pdfs if n.startswith("Общие каталоги/")]
    print("V5_FINAL",json.dumps({"size":out_path.stat().st_size,"original_catalogs":len(full),"series_pdf_files":len(pdfs)-len(full),"supplemental":[{"series":s["series"],"proof":s["proof"]} for s in supplemental],"removed_dup":removed},ensure_ascii=False),flush=True)
