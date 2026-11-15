#!/usr/bin/env python3
"""Build an auditable Selectel upload pack from immutable MIXED377 v7 release.
Only model-exact technical PDFs get public links; family-only files stay REVIEW_ONLY.
"""
import collections, csv, hashlib, io, json, os, pathlib, re, sys, zipfile
import requests
import fitz

REPO=pathlib.Path("product-research/catalog-377/techdocs-2026-11-14")
MODEL_CSV=REPO/"independent-audit-v7-2026-11-14/model_exact_coverage.csv"
OLD=pathlib.Path(sys.argv[1])
DEST=pathlib.Path(sys.argv[2])
DEST.parent.mkdir(parents=True,exist_ok=True)
BASE="https://docs.proclimate5.ru/multizonalnye_vrv_i_vrf_sistemy"
FOLDERS={b:f"multizonalnye_vrv_i_vrf_sistemy/vnutrennie_bloki_VRF_sistem_{b}/2026" for b in ("IGC","Bosch","Daikin","Kentatsu","Midea")}
REMOTE={b:f"{BASE}/vnutrennie_bloki_VRF_sistem_{b}/2026/" for b in FOLDERS}
EXTRA_1T="https://docs.proclimate5.ru/multizonalnye_vrv_i_vrf_sistemy/vnutrennie_bloki_VRF_sistem_IGC/2026/IMS_1T_catalog.pdf"
AUDIT=["catalog_744_row","brand","model","series_key","proof","new_proof","document_count","doc_filenames","target_urls","html","source_evidence","action"]
BLOCK='<p>\n <a href="{url}" target="_blank"><img src="/images/icons/pdf-icon2.jpg" alt="" style="height:41px; width:40px"></a> <a href="{url}" target="_blank">{label}</a>\n</p>'

def clean(s):
    return re.sub(r"[^a-z0-9]","",s.casefold())
def label(name):
    if "_catalog" in name:return "Страница каталога"
    if "_declaration" in name:return "Декларация соответствия"
    if "_certificate" in name:return "Сертификат соответствия"
    if "installation_and_user_manual" in name:return "Инструкция к товару"
    if "installation_manual" in name:return "Инструкция по монтажу"
    if "_user_manual" in name or "_manual" in name:return "Инструкция к товару"
    if "_technical_data" in name or "_datasheet" in name:return "Технические данные"
    if "_specification" in name:return "Технические характеристики"
    return "Техническое руководство"
def writecsv(rows,fields):
    ioobj=io.StringIO()
    writer=csv.DictWriter(ioobj,fieldnames=fields,extrasaction="ignore",lineterminator="\n")
    writer.writeheader();writer.writerows(rows)
    return ioobj.getvalue().encode("utf-8-sig")
def proofexact(pdf,models):
    try:
        with fitz.open(stream=pdf,filetype="pdf") as doc:
            lines=[p.get_text("text") for p in doc]
        res={}
        for model in models:
            needle=clean(model)
            # PDF page separately: never stitch neighboring table columns/pages.
            res[model]=any(needle in clean(page) for page in lines)
        return res
    except Exception as e:
        return {x:False for x in models}

with open(MODEL_CSV,encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))
assert len(rows)==377 and len({(r["brand"],r["model"]) for r in rows})==377, "377 inventory gate"
assert OLD.is_file() and OLD.stat().st_size>100_000_000, "v7 original ZIP not downloaded"
sha=hashlib.file_digest(open(OLD,"rb"),"sha256").hexdigest()
assert sha=="cffc616df0c39c728ebfb16f0b04910bd415b14ea955e4d1b85e14ef29591bfe", "Immutable v7 archive SHA mismatch"
with zipfile.ZipFile(OLD) as z:
    assert z.testzip() is None
    oldpdf={n:z.read(n) for n in z.namelist() if n.lower().endswith(".pdf")}
assert len(oldpdf)>=60, "unexpected v7 PDF inventory"
assert not any("Midea_ATOM_2024" in name for name in oldpdf), "unsafe regional ATOM PDF still present"
# A directly supplied, region-relevant PDF may close 2 false negatives from textual audit.
extra_pdf=None
try:
    resp=requests.get(EXTRA_1T,timeout=35,headers={"User-Agent":"Mozilla/5.0"})
    if resp.ok and resp.content.startswith(b"%PDF-"):
        tmodels=[r["model"] for r in rows if r["brand"]=="IGC" and r["series_key"]=="IMS_1T"]
        results=proofexact(resp.content,tmodels)
        if len(tmodels)==6 and all(results.values()):
            extra_pdf=resp.content
            print("IGC_IMS1T direct PDF: exact match all 6",flush=True)
        else:
            print("IGC_IMS1T direct PDF incomplete:",results,flush=True)
    else:print("IGC_IMS1T request invalid:",resp.status_code,flush=True)
except Exception as exc:
    print("IGC_IMS1T direct fetch failed:",str(exc)[:250],flush=True)

# New regional-library originals: accept a manual ONLY for models spelled out in its PDF.
KENTATSU_CANDIDATES={
    "KTZV":"https://www.iclim.ru/library/kentatsu-ktzv-hzbn1-instruktsiya.pdf",
    "KTLV":"https://www.iclim.ru/library/kentatsu-ktlv-hzbn1-instruktsiya.pdf",
    "KTKV":"https://www.iclim.ru/library/kentatsu-ktkv-hzbn1-instruktsiya.pdf",
    "KTGB":"https://www.iclim.ru/library/kentatsu-dx-pro-vii-ktgb-hzbn1-instruktsiya.pdf",
}
new_kentatsu={}
for group,url in KENTATSU_CANDIDATES.items():
    models=[r["model"] for r in rows if r["brand"]=="Kentatsu" and r["series_key"]==group]
    try:
        reply=requests.get(url,timeout=80,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf"})
        if not(reply.ok and reply.content.startswith(b"%PDF-")):raise ValueError(f"bad HTTP/PDF {reply.status_code}")
        verified=proofexact(reply.content,models)
        correct=[m for m,ok in verified.items() if ok]
        print("KENTATSU_NEW_MANUAL",group,"checked",len(models),"exact",len(correct),"models",correct,flush=True)
        if correct:
            name=f"Kentatsu/{group}/{group}_installation_and_user_manual_2026.pdf"
            if name in oldpdf:raise AssertionError("new documentation path already in release")
            oldpdf[name]=reply.content
            new_kentatsu[group]=(name,set(correct),url)
    except Exception as e:
        print("KENTATSU_NEW_MANUAL_ERROR",group,str(e)[:280],flush=True)

# Current Russian-language Midea manuals located after v7. Exact suffix must occur in PDF.
MIDEA_CANDIDATES={
    "MI2_Q4C":"https://www.iclim.ru/library/midea-mi2-q4c-instruktsiya.pdf",
    "MI2_Q1":"https://www.iclim.ru/library/midea-mi2-q1dhn18-at-instruktsiya.pdf",
    "MI2_T3":"https://www.iclim.ru/library/midea-mi2-t3dhn18-at-instruktsiya.pdf",
    "MI2_Q4":"https://midea-pro.ru/library/midea-mi2-q4dhn18-at-instruktsiya.pdf",
    "MI2_G_DP":"https://www.iclim.ru/library/midea-mi2-gdhn18-at-dp-instruktsiya.pdf",
    "MI2_DL":"https://www.iclim.ru/library/midea-mi2-dldhn18-at-instruktsiya.pdf",
}
new_midea={}
for group,url in MIDEA_CANDIDATES.items():
    models=[r["model"] for r in rows if r["brand"]=="Midea" and r["series_key"]==group]
    try:
        reply=requests.get(url,timeout=80,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf"})
        if not(reply.ok and reply.content.startswith(b"%PDF-")):raise ValueError(f"bad HTTP/PDF {reply.status_code}")
        checked=proofexact(reply.content,models)
        correct=[m for m,ok in checked.items() if ok]
        print("MIDEA_NEW_MANUAL",group,"checked",len(models),"exact",len(correct),"models",correct,flush=True)
        if correct:
            name=f"Midea/{group}/{group}_installation_and_user_manual_2026.pdf"
            if name in oldpdf:raise AssertionError("new documentation path already in release")
            oldpdf[name]=reply.content
            new_midea[group]=(name,set(correct),url)
    except Exception as e:
        print("MIDEA_NEW_MANUAL_ERROR",group,str(e)[:280],flush=True)

# Original IGC IMS DC5 installation/operation manual; SSL chain may be incomplete on source host.
new_igc_4tm=None
url_4tm="https://igc-aircon.com/upload/iblock/2fd/g7gqb0wx6uqkoxuz7qf9lnhfzsxzpmks.pdf"
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    reply=requests.get(url_4tm,timeout=90,verify=False,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf"})
    if not(reply.ok and reply.content.startswith(b"%PDF-")):raise ValueError(f"not valid PDF HTTP {reply.status_code}")
    models_4tm=[r["model"] for r in rows if r["brand"]=="IGC" and r["series_key"]=="IMS_4TM"]
    checked=proofexact(reply.content,models_4tm)
    matching=[m for m,v in checked.items() if v]
    print("IGC_4TM_DC5_INSTALL_MANUAL",len(matching),"of",len(models_4tm),"models",matching,flush=True)
    if matching:
        new_igc_4tm=("IGC/IMS_4TM/IMS_4TM_installation_and_user_manual_2026.pdf",set(matching),url_4tm)
        oldpdf[new_igc_4tm[0]]=reply.content
except Exception as e:
    print("IGC_4TM_DC5_FAILED",str(e)[:280],flush=True)

# Confirmed IGC IMS 5 original installation manual, exact full SKU on page 4.
IGC_IMS5="https://iclim.ru/library/igc-ims-5-vnutrennie-bloki-instruktsiya.pdf"
new_igc_ims5=None
try:
    resp=requests.get(IGC_IMS5,timeout=90,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf"})
    if not(resp.ok and resp.content.startswith(b"%PDF-")):raise ValueError(f"non-PDF source: {resp.status_code}")
    models_ims5=[r["model"] for r in rows if r["brand"]=="IGC" and r["series_key"] in ("IMS_4TM","IMS_QV")]
    found=proofexact(resp.content,models_ims5)
    # Exact model + matching same generation; can serve more than one of the 53 code groups.
    verified={m for m,ok in found.items() if ok}
    print("IGC_IMS5_EXACT_MODELS",len(verified),sorted(verified),flush=True)
    expected={"IMS-4TM28NH (DC5)","IMS-4TM36NH(DC5)","IMS-4TM45NH(DC5)","IMS-4TM56NH(DC5)","IMS-QV100NH(DC)"}
    if not expected <= verified:raise ValueError(f"key IGC models absent: {expected-verified}")
    p="IGC/IMS_5/IMS_5_installation_and_user_manual_2026.pdf"
    oldpdf[p]=resp.content
    new_igc_ims5=(p,verified,IGC_IMS5)
except Exception as exc:
    print("IGC_IMS5_NOT_CONFIRMED",str(exc)[:300],flush=True)

# Reconcile per-model proof names, never infer from folder membership.
source_paths=collections.defaultdict(list)
for r in rows:
    names=[x.strip() for x in (r.get("exact_pdf_names") or "").split(" | ") if x.strip()]
    if r["proof"] not in ("EXACT_MODEL_TECH_PDF","EXACT_MODEL_DECLARATION_ONLY"):names=[]
    for n in names:
        if n not in oldpdf:
            raise AssertionError(f"Audit references absent PDF: {n}")
        if n.split("/")[0]!=r["brand"]:
            raise AssertionError(f"Wrong-brand PDF: {n} for {r['model']}")
    if r["brand"]=="Kentatsu" and r["series_key"] in new_kentatsu and r["model"] in new_kentatsu[r["series_key"]][1]:
        name,verified,url=new_kentatsu[r["series_key"]]
        names=[name]+names
        r["new_proof"]="DIRECT_2026_KENTATSU_MANUAL_EXACT"
    elif r["brand"]=="IGC" and new_igc_ims5 is not None and r["model"] in new_igc_ims5[1] and r["proof"]!="EXACT_MODEL_TECH_PDF":
        names=[new_igc_ims5[0]]+names
        r["new_proof"]="DIRECT_IGC_IMS5_TECH_MANUAL_EXACT"
    elif r["brand"]=="IGC" and r["series_key"]=="IMS_4TM" and new_igc_4tm is not None and r["model"] in new_igc_4tm[1]:
        names=[new_igc_4tm[0]]+names
        r["new_proof"]="DIRECT_IGC_DC5_INSTALL_MANUAL_EXACT"
    elif r["brand"]=="Midea" and r["series_key"] in new_midea and r["model"] in new_midea[r["series_key"]][1]:
        name,verified,url=new_midea[r["series_key"]]
        names=[name]+names
        r["new_proof"]="DIRECT_2026_MIDEA_MANUAL_EXACT"
    elif extra_pdf is not None and r["brand"]=="IGC" and r["series_key"]=="IMS_1T":
        # Replace the superseded excerpt with the clean original exact-model catalog.
        names=[n for n in names if "IMS_1T_catalog.pdf" not in n]
        names=["IGC/IMS_1T/IMS_1T_catalog.pdf"]+names
        r["new_proof"]="DIRECT_MANUFACTURER_CATALOG_2026_EXACT"
    elif r["proof"]=="EXACT_MODEL_TECH_PDF":
        r["new_proof"]="ARCHIVE_V7_EXACT"
    elif r["proof"]=="EXACT_MODEL_DECLARATION_ONLY":
        r["new_proof"]="DECLARATION_ONLY"
    else:
        r["new_proof"]="NOT_MODEL_VERIFIED"
    r["_names"]=sorted(set(names),key=lambda v:(0 if "catalog" in v else 1,v))

if extra_pdf is not None:
    oldpdf["IGC/IMS_1T/IMS_1T_catalog.pdf"]=extra_pdf

# The exact same uploaded filename must not refer to two different PDFs.
upload={}
url_by_src={}
sha_rows=[]
for r in rows:
    for n in r["_names"]:
        b=n.split("/")[0]
        basename=n.rsplit("/",1)[-1]
        zpath=f"UPLOAD_TO_SELECTEL/{FOLDERS[b]}/{basename}"
        payload=oldpdf[n]
        digest=hashlib.sha256(payload).hexdigest()
        if zpath in upload and hashlib.sha256(upload[zpath]).hexdigest()!=digest:
            raise AssertionError(f"filename collision: {zpath}")
        upload[zpath]=payload
        url_by_src[n]=REMOTE[b]+basename

# Build entire 377-SKU manifest; do not fabricate PDFs for remaining products.
document_index=[]
missing=[]
for r in rows:
    names=r["_names"]
    urls=[url_by_src[n] for n in names]
    html="\n".join(BLOCK.format(url=url_by_src[n],label=label(n)) for n in names)
    status=r["new_proof"]
    if status=="NOT_MODEL_VERIFIED":
        if r["brand"]=="Midea" and r["series_key"] in ("MI2_Q1","MI2_Q4C","MI2_Q4","MI2_T3"):
            action="NO_PDF_IN_V7_GROUP__FIND_REGION_SPECIFIC_TECHNICAL_PDF"
        else:action="FAMILY_PDF_ONLY__FIND_EXACT_MODEL_OR_MANUAL"
    elif status=="DECLARATION_ONLY":action="FIND_TECHNICAL_PDF__DECLARATION_NOT_TECHNICAL_DATA"
    else:action="UPLOAD_PDFS_AND_VERIFY_HTTP_200__LINKS_NOT_YET_LIVE"
    entry={
        "catalog_744_row":r["catalog_744_row"],"brand":r["brand"],"model":r["model"],
        "series_key":r["series_key"],"proof":r["proof"],"new_proof":status,
        "document_count":len(names),"doc_filenames":" | ".join(n.split("/")[-1] for n in names),
        "target_urls":" | ".join(urls),"html":html,
        "source_evidence":" | ".join(names) if names else "",
        "action":action}
    document_index.append(entry)
    if status in ("NOT_MODEL_VERIFIED","DECLARATION_ONLY"):missing.append(entry)
    for n in names:
        document_index[-1].setdefault("_private",[])

# Keep all original full catalogs and never silently promote unverified PDF to upload.
review={}
full={}
for n,payload in oldpdf.items():
    if n.startswith("Общие каталоги/"):full["ORIGINAL_FULL_CATALOGS/"+n]=payload
    elif "/" in n and n.split("/")[0] in FOLDERS and n not in url_by_src:
        review["REVIEW_ONLY_NOT_FOR_UPLOAD/"+n]=payload

readme=f"""MIXED 377 — пакет подготовки загрузки Selectel, 2026-11-15
All 377 unfilled catalog products appear in REPORTS/ALL_377.csv.
Immutable source archive v7 SHA256: {sha}
READY: {sum(x['new_proof'] in ('ARCHIVE_V7_EXACT','DIRECT_MANUFACTURER_CATALOG_2026_EXACT','DIRECT_2026_KENTATSU_MANUAL_EXACT','DIRECT_2026_MIDEA_MANUAL_EXACT','DIRECT_IGC_DC5_INSTALL_MANUAL_EXACT','DIRECT_IGC_IMS5_TECH_MANUAL_EXACT') for x in document_index)} exact technical models.
DECLARATION ONLY: {sum(x['new_proof']=='DECLARATION_ONLY' for x in document_index)} models, technical manuals still missing.
NOT MODEL VERIFIED: {sum(x['new_proof']=='NOT_MODEL_VERIFIED' for x in document_index)} models.
UPLOAD_TO_SELECTEL: {len(upload)} distinct PDF payloads under explicit destination folder paths.
REVIEW_ONLY_NOT_FOR_UPLOAD: {len(review)} series candidate PDFs; they are NOT approved model links.
ORIGINAL_FULL_CATALOGS: {len(full)} unchanged source originals.

Deployment:
1. Upload only the CONTENTS of UPLOAD_TO_SELECTEL/ to the document root, keeping folders and case unchanged.
2. Set PDF objects publicly readable, Content-Type application/pdf.
3. Check each URL in REPORTS/ALL_377.csv with HTTP HEAD/GET and verify bytes / file type.
4. Only then publish HTML links in product Excel. URLs here are intended paths, not proof of upload.
5. REVIEW_ONLY documents must NOT be put into public product cards without exact applicability check.

CRITICAL: 2024 overseas Midea ATOM file is quarantined from v7 due 4.5 vs 1.5 kW regional inconsistency on MI2-15Q4CDHN18(At).
Pending models cannot be called complete.
IGC direct source: {EXTRA_1T}
NEW KENTATSU direct sources: {len(new_kentatsu)} verified PDFs; see REPORTS/NEW_KENTATSU_PDF_SOURCES.csv
NEW MIDEA direct sources: {len(new_midea)} verified PDFs; see REPORTS/NEW_MIDEA_PDF_SOURCES.csv
IGC DC5 manual: {url_4tm if new_igc_4tm is not None else "not verified"}; SSL chain was not verified on origin.
IGC IMS 5 confirmed: {IGC_IMS5 if new_igc_ims5 is not None else "not found"}; see REPORTS/IGC_IMS5_MODELS.csv
2026 EAEU model listing (not a substitute for technical PDF): https://xn----7sbajahheyaepn1ca0aveqcb0fxl.xn--p1acf/document/eaes-n-ru-d-cnra08v0854326/
"""
with zipfile.ZipFile(DEST,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=5,allowZip64=True) as z:
    for coll in (upload,review,full):
        for n,b in sorted(coll.items()):z.writestr(n,b)
    z.writestr("REPORTS/ALL_377.csv",writecsv(document_index,AUDIT))
    z.writestr("REPORTS/NEED_MORE_PROOF.csv",writecsv(missing,AUDIT))
    z.writestr("REPORTS/SERVER_FILE_MANIFEST.csv",writecsv(
        [{"zip_path":n,"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),"target_url":"https://docs.proclimate5.ru/"+n.split("UPLOAD_TO_SELECTEL/",1)[1]}
         for n,b in sorted(upload.items())],
        ["zip_path","sha256","bytes","target_url"]))
    z.writestr("REPORTS/NEW_KENTATSU_PDF_SOURCES.csv",writecsv(
        [{"series":g,"source_url":t[2],"new_pdf_filename":t[0].split("/")[-1],"models_confirmed":" | ".join(sorted(t[1]))} for g,t in sorted(new_kentatsu.items())],
        ["series","source_url","new_pdf_filename","models_confirmed"]))
    z.writestr("REPORTS/NEW_MIDEA_PDF_SOURCES.csv",writecsv(
        [{"series":g,"source_url":t[2],"new_pdf_filename":t[0].split("/")[-1],"models_confirmed":" | ".join(sorted(t[1]))} for g,t in sorted(new_midea.items())],
        ["series","source_url","new_pdf_filename","models_confirmed"]))
    z.writestr("REPORTS/IGC_IMS5_MODELS.csv",writecsv(
        [{"source_url":new_igc_ims5[2],"pdf_name":new_igc_ims5[0],"model":m} for m in sorted(new_igc_ims5[1])] if new_igc_ims5 else [],
        ["source_url","pdf_name","model"]))
    z.writestr("README_SELECTEL.txt",readme.encode("utf-8"))
with zipfile.ZipFile(DEST) as z:
    assert z.testzip() is None
    assert sum(r["new_proof"]=="NOT_MODEL_VERIFIED" for r in document_index)+sum(r["new_proof"]=="DECLARATION_ONLY" for r in document_index)+sum(r["new_proof"] in ("ARCHIVE_V7_EXACT","DIRECT_MANUFACTURER_CATALOG_2026_EXACT","DIRECT_2026_KENTATSU_MANUAL_EXACT","DIRECT_2026_MIDEA_MANUAL_EXACT","DIRECT_IGC_DC5_INSTALL_MANUAL_EXACT","DIRECT_IGC_IMS5_TECH_MANUAL_EXACT") for r in document_index)==377
    assert len(document_index)==377
report={
    "source_zip_sha256":sha,"archive":str(DEST),"archive_bytes":DEST.stat().st_size,
    "products":377,"exact_technical":sum(r["new_proof"] in ("ARCHIVE_V7_EXACT","DIRECT_MANUFACTURER_CATALOG_2026_EXACT","DIRECT_2026_KENTATSU_MANUAL_EXACT","DIRECT_2026_MIDEA_MANUAL_EXACT","DIRECT_IGC_DC5_INSTALL_MANUAL_EXACT","DIRECT_IGC_IMS5_TECH_MANUAL_EXACT") for r in document_index),
    "declaration_only":sum(r["new_proof"]=="DECLARATION_ONLY" for r in document_index),
    "unverified":sum(r["new_proof"]=="NOT_MODEL_VERIFIED" for r in document_index),
    "upload_pdf_files":len(upload),"review_pdf_files":len(review),"full_original_catalogs":len(full),
    "new_igc_pdf_downloaded":extra_pdf is not None,
    "new_kentatsu":{g:{"models_confirmed":len(t[1]),"source_url":t[2]} for g,t in new_kentatsu.items()},
    "new_midea":{g:{"models_confirmed":len(t[1]),"source_url":t[2]} for g,t in new_midea.items()},
    "new_igc_4tm":({"models_confirmed":len(new_igc_4tm[1]),"source_url":new_igc_4tm[2],"tls_verified":False} if new_igc_4tm else None),
    "new_igc_ims5":({"models_confirmed":len(new_igc_ims5[1]),"source_url":new_igc_ims5[2]} if new_igc_ims5 else None),
    "not_uploaded_to_selectel":True}
print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
pathlib.Path(str(DEST)+".summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
