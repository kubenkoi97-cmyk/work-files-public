#!/usr/bin/env python3
"""Repackage checked 377-SKU series archive, eliminating identical PDF bytes within a series.
Never alter original source PDFs; preserving provenance via sha256 duplicate manifest.
"""
import hashlib, json, os, sys, zipfile
from collections import defaultdict
from pathlib import Path

base = Path(sys.argv[1])
out = Path(sys.argv[2])
dupes=[]
seen={}
pages=0
kept=0
with zipfile.ZipFile(base) as inp, zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as dest:
    names = inp.namelist()
    # For identical content, keep the more precise manual name when available.
    def rank(n):
        lower=n.lower()
        return (
            0 if "_installation_and_user_manual.pdf" in lower else
            1 if "_installation_manual.pdf" in lower else
            2 if "_user_manual.pdf" in lower else
            3 if "_technical_data.pdf" in lower else
            4,
            n
        )
    # Sort for dup grouping preferences; regular non-PDF files remain.
    files=sorted((n for n in names if not n.endswith("/")),key=rank)
    for n in files:
        data=inp.read(n)
        folder=n.rsplit("/",1)[0] if "/" in n else ""
        sha=hashlib.sha256(data).hexdigest()
        if n.lower().endswith(".pdf"):
            # Within a series or globally across copies of full catalogs with same brand.
            if n.startswith("Общие каталоги/"):
                scope=n.split("/")[1].split("_")[0].lower()+"_original_full_catalog"
            else:
                scope=folder
            key=(scope,sha)
            if key in seen:
                dupes.append({"skipped_path":n,"kept_path":seen[key],"sha256":sha,"bytes":len(data)})
                continue
            seen[key]=n
        dest.writestr(n,data)
        kept+=1
    manifest={
        "scope":"377 originally unfilled models only; 53 preliminary series",
        "input_asset":str(base.name),
        "input_sha256":hashlib.sha256(base.read_bytes()).hexdigest(),
        "originals_untouched":True,
        "duplicate_definition":"exact SHA-256 identical bytes within a series or identical full catalogs of same manufacturer",
        "duplicates_removed":len(dupes),
        "removed":dupes,
        "warning":"Do not interpret partial series documentation as verification for every model or field. See original audit.json and series_documents_report.csv.",
    }
    dest.writestr("deduplication_manifest.json",json.dumps(manifest,ensure_ascii=False,indent=2).encode("utf-8"))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert "deduplication_manifest.json" in z.namelist()
    pdfs=[n for n in z.namelist() if n.endswith(".pdf")]
    originals=[n for n in pdfs if n.startswith("Общие каталоги/")]
    excerpts=[n for n in pdfs if not n.startswith("Общие каталоги/") and "_catalog" in n]
    manuals=[n for n in pdfs if not n.startswith("Общие каталоги/") and "_catalog" not in n]
print(json.dumps({"output":str(out),"bytes":out.stat().st_size,
"unique_full_catalogs":len(originals),"unique_series_excerpts":len(excerpts),
"unique_series_other_pdfs":len(manuals),"duplicates_removed":len(dupes),
"removed":dupes},ensure_ascii=False,indent=2),flush=True)
