#!/usr/bin/env python3
"""Independent v3 review of five recovery ZIPs, and safe reconciliation.
Only original exact-SKU HTML with genuine vendor narrative/specs and real photos
can be promoted. This script downloads the released ZIP anew; no guessed statuses.
"""
import csv, io, importlib.util, json, re, subprocess, tempfile
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
from bs4 import BeautifulSoup

ROOT=Path("product-research/catalog-377")
OUT=ROOT/"audit-v3"
OUT.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location("audit_gh_cli",ROOT/"audit_gh_cli.py")
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
CYR=str.maketrans({"А":"A","В":"B","С":"C","Е":"E","Н":"H","К":"K","М":"M","О":"O","Р":"P","Т":"T","Х":"X","У":"Y",
                   "а":"a","в":"b","с":"c","е":"e","н":"h","к":"k","м":"m","о":"o","р":"p","т":"t","х":"x","у":"y"})
def normalized(x):
    return re.sub(r"\s+","",str(x).translate(CYR).upper())
audit.norm=normalized

BATCHES=["169-180","181-196","197-206","341-341","350-350"]
FIELDS=["brand","model","master_status","release_tag","zip_integrity",
        "file_presence","exact_heading","photo_images_verified",
        "has_description_in_manifest","has_specs_in_manifest","source_url","reason"]
records=[]
for label in BATCHES:
    path=ROOT/"status"/("partial-effect-"+label+".csv")
    if not path.exists():
        raise RuntimeError("Missing published candidate status: "+str(path))
    with path.open(encoding="utf-8-sig",newline="") as f:
        candidates=list(csv.DictReader(f))
    tag="catalog377-partial-effect-"+label
    filename="catalog377-"+label+".zip"
    print("INDEPENDENT_DOWNLOAD",tag,len(candidates),flush=True)
    with tempfile.TemporaryDirectory() as temporary:
        zpath,error=audit.fetch(tag,filename,Path(temporary))
        if error:
            raise RuntimeError("Cannot independently download "+tag+": "+error)
        with ZipFile(zpath) as z:
            bad=z.testzip()
            if bad:raise RuntimeError("Bad ZIP entry "+tag+": "+bad)
            names=set(z.namelist())
            for c in candidates:
                rec=audit.check_one(z,c,tag)
                # Validate exact original publisher prose, not generic navigation or own text.
                if rec["reason"]=="OK" and c["status"]=="COMPLETE":
                    prefix="products/"+c["brand"]+"_"+audit.safe(c["model"])+"/"
                    soup=BeautifulSoup(z.read(prefix+"original.html").decode("utf-8","replace"),"html.parser")
                    h1=" ".join(h.get_text(" ",strip=True) for h in soup.select("h1"))
                    txt=soup.get_text(" ",strip=True)
                    i=txt.find("Дополнительная информация")
                    j=txt.find("Вы можете купить кондиционер",i) if i>=0 else -1
                    prose=txt[i:(j if j>i else i+2200)] if i>=0 else ""
                    if ("effect-nn.ru" not in c.get("source_url","")
                         or normalized(c["model"]) not in normalized(h1)
                         or len(prose)<120
                         or ("внутренний" not in prose.lower() and "Канальный" not in prose
                             and "кондиционирован" not in prose.lower())):
                        rec["reason"]="INVALID_PUBLISHER_PROSE_OR_SKU"
                    if prefix+"server-source-original.html" not in names:
                        rec["reason"]="MISSING_UNMODIFIED_HTTP_BYTES"
                records.append(rec)
                print("REVIEW",c["model"],c["status"],rec["reason"],rec["photo_images_verified"],flush=True)
assert len(records)==40 and len({(x["brand"],x["model"]) for x in records})==40

with (OUT/"partial-effect-qa.csv").open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(records)
approved={(x["brand"],x["model"]) for x in records if x["master_status"]=="COMPLETE" and x["reason"]=="OK"}
summary={"total_reaudited":len(records),"promoted_original_html":len(approved),
         "still_partial":len(records)-len(approved),
         "by_status":dict(Counter("VERIFIED" if x["reason"]=="OK" else x["reason"] for x in records)),
         "method":"Independent gh release download; CRC, exact homoglyph-safe SKU H1, raw original + offline HTML, original publisher prose, specs, locally decoded product images"}
(OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print("V3_RESULT",json.dumps(summary,ensure_ascii=False),flush=True)

# The authoritative reconciler only accepts v3-approved new COMPLETE rows.
subprocess.run(["python",str(ROOT/"reconcile_status.py")],check=True)
master_path=ROOT/"status"/"master_status.csv"
with master_path.open(encoding="utf-8-sig",newline="") as f:
    master=list(csv.DictReader(f))
master_by={(r["brand"],r["model"]):r for r in master}

# Synchronize the separate original-HTML evidence matrix, preserving unapproved rows.
matrix_path=ROOT/"status"/"html_capture_matrix.csv"
with matrix_path.open(encoding="utf-8-sig",newline="") as f:
    reader=csv.DictReader(f);fields=reader.fieldnames;matrix=list(reader)
for x in matrix:
    k=(x["brand"],x["model"])
    if k not in approved:continue
    m=master_by[k]
    if m["status"]!="COMPLETE" or m["zip_verified"]!="YES":
        raise RuntimeError("Audit/reconciler conflict for "+str(k))
    x.update(exact_original_html_captured="YES",original_html_description="YES",
        exact_gallery_photo_files="YES",zip_integrity_verified="YES",
        source_url=m["source_url"],zip_archive_url=m["archive_download_url"],
        content_gate="COMPLETE",quarantined_wrong_model_url="",
        outstanding_action="NONE: authentic source and independent archive QA verified")
with matrix_path.open("w",encoding="utf-8-sig",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(matrix)
counts=Counter(m["status"] for m in master)
matrix_status={
    "total_exact_skus":len(master),
    "verified_original_html_and_photos":sum(x["exact_original_html_captured"]=="YES" and x["exact_gallery_photo_files"]=="YES" for x in matrix),
    "original_page_also_has_product_description":sum(x["original_html_description"]=="YES" for x in matrix),
    "verified_original_html_but_no_independent_description":sum(x["content_gate"]=="PARTIAL" for x in matrix),
    "wrong_model_suffix_quarantined":counts["WRONG_MODEL"],
    "exact_individual_page_unavailable":counts["NOT_FOUND"],
    "statuses":dict(counts),
    "important":"Exact original HTML, description and archive integrity are separately checked; old supplier originals preserved."
}
(ROOT/"status"/"html_capture_summary.json").write_text(json.dumps(matrix_status,ensure_ascii=False,indent=2),encoding="utf-8")
(OUT/"RESULTS.md").write_text(
    "# PARTIAL exact HTML recovery - independent audit v3\n\n"
    +f"Audited: {len(records)}. New independently VERIFIED COMPLETE: {len(approved)}. "
    +f"Remaining PARTIAL among them: {40-len(approved)}.\n\n"
    +"Historical source ZIPs and authored description companions are preserved. "
    +"Original shop HTML was never rewritten to insert our text.\n",
    encoding="utf-8")
print("RECONCILED",json.dumps(matrix_status,ensure_ascii=False),flush=True)
