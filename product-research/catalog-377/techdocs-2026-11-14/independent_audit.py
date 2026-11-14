#!/usr/bin/env python3
"""Independent exact-SKU audit of the published MIXED 377 / 53-series PDF archive.
Does not trust previous PARTIAL_VERIFIED status or infer document-to-model coverage.
"""
import csv, hashlib, json, os, re, sys, zipfile
from collections import defaultdict, Counter
from pathlib import Path
import fitz

base=Path("product-research/catalog-377/techdocs-2026-11-14")
scope=list(csv.DictReader((base/"series_inventory.csv").open(encoding="utf-8-sig")))
assert len(scope)==377
assert len({(r["brand"],r["model"]) for r in scope})==377
assert all(r["scope"]=="UNFILLED_ONLY" for r in scope)
groups=defaultdict(list)
for r in scope: groups[(r["brand"],r["series_key"])].append(r)
assert len(groups)==53
zip_path=Path(sys.argv[1])
z=zipfile.ZipFile(zip_path)
names=z.namelist()
duplicates=defaultdict(list)
all_codes=[(r["brand"],r["model"],r["series_key"]) for r in scope]
def patt(s):
    compact=re.sub(r"\s+","",s.upper())
    pattern=r"(?<![A-Z0-9])"+r"\s*".join(re.escape(char) for char in compact)+r"(?![A-Z0-9])"
    if "(" not in compact:pattern+=r"(?!\s*\()"
    return re.compile(pattern,re.I)
regex={m:patt(m) for _,m,_ in all_codes}
doc_index=defaultdict(list)
failed=[]
stats={"pdf_total":0,"pages_read":0,"pdfs_without_matching_target":0}
for n in names:
    if not n.lower().endswith(".pdf"):continue
    sha=hashlib.sha256(z.read(n)).hexdigest()
    if n.startswith("Общие каталоги/"):continue
    parts=n.split("/")
    if len(parts)!=3:continue
    brand,key,filename=parts
    if (brand,key) not in groups:failed.append({"file":n,"issue":"FOLDER_NOT_IN_SCOPE"});continue
    raw=z.read(n)
    duplicates[sha].append(n)
    stats["pdf_total"]+=1
    try:
        pdf=fitz.open(stream=raw,filetype="pdf")
        texts=[p.get_text() for p in pdf]
        stats["pages_read"]+=len(texts)
        matches={}
        for mdlbrand,model,targetkey in all_codes:
            # Detect whether entire included PDF cites other scoped series.
            hits=[idx+1 for idx,t in enumerate(texts) if regex[model].search(t)]
            if hits:
                matches[(mdlbrand,model,targetkey)]=hits
        within={m:hits for (b,m,k),hits in matches.items() if b==brand and k==key}
        outside={f"{b}/{k}/{m}":hits for (b,m,k),hits in matches.items() if not (b==brand and k==key)}
        # Scan full text, not just filename or source-group label.
        if not within:stats["pdfs_without_matching_target"]+=1
        doc_index[(brand,key)].append({
            "path":n,"pages":len(pdf),"sha256":sha,
            "matched_sku_pages":within,"other_scoped_models_on_pages":outside,
            "type":"declaration" if "declaration" in filename.lower() else
                   "catalog_excerpt" if "catalog" in filename.lower() else "manual_or_other",
            "text_extraction_pages_without_text":sum(len(t.strip())==0 for t in texts)
        })
    except Exception as e: failed.append({"file":n,"issue":str(e)[:250]})
modelrows=[]
seriesrows=[]
for (brand,key),member in groups.items():
    docs=doc_index.get((brand,key),[])
    mdl_list=[r["model"] for r in member]
    group_specific=[x for x in docs if x["type"]!="declaration"]
    tech_exact=set().union(*(set(x["matched_sku_pages"]) for x in group_specific)) if group_specific else set()
    decl_exact=set().union(*(set(x["matched_sku_pages"]) for x in docs if x["type"]=="declaration")) if docs else set()
    family_only=set(mdl_list)-tech_exact-decl_exact
    crossdocs=[x for x in docs if x["other_scoped_models_on_pages"]]
    for r in member:
        m=r["model"]
        hits=[{"pdf":d["path"],"pages":d["matched_sku_pages"][m]} for d in docs if m in d["matched_sku_pages"]]
        technical=[x for x in hits if "declaration" not in x["pdf"].lower()]
        declarations=[x for x in hits if "declaration" in x["pdf"].lower()]
        proof="EXACT_MODEL_TECH_PDF" if technical else "EXACT_MODEL_DECLARATION_ONLY" if declarations else "SERIES_ONLY_OR_UNVERIFIED"
        if (brand,key)==("IGC","IMS_BH"):
            variant="NH_DC" if "NH(DC)" in re.sub(r"\s+","",m) else "NB_NO_DC"
        else:variant=""
        modelrows.append({
            **{k:r[k] for k in ["catalog_744_row","brand","model","series_key"]},
            "model_variant":variant,"proof":proof,
            "exact_technical_pdf_count":len(technical),
            "exact_declaration_count":len(declarations),
            "exact_pdf_names":" | ".join(x["pdf"] for x in hits)
        })
    seriesrows.append({
        "brand":brand,"series_key":key,"models":len(member),
        "exact_models_in_technical_pdfs":len(tech_exact),"exact_models_in_declaration_only":len(decl_exact-tech_exact),
        "without_model_specific_proof":len(family_only),
        "series_pdf_count":len(docs),"pdfs_with_out_of_group_models":len(crossdocs),
        "scope_note":"MIXED_SUFFIXES_IN_ONE_FAMILY; separate spec applicability NH(DC) vs NB" if (brand,key)==("IGC","IMS_BH") else
                     "DP_OPTION_SPLIT_IN_CURRENT_ARCHIVE; shared manufacturer MI2_GDHN18/MI2_GDHN18DP series source" if (brand,key) in [("Midea","MI2_G"),("Midea","MI2_G_DP")] else
                     "OPTIONAL_PUMP_SUFFIX_DIFFERENCE" if (brand,key) in [("Midea","MIH_G"),("Midea","MIH_G_DP")] else "",
        "models_without_exact_model_proof":" | ".join(sorted(family_only)),
        "pdfs_with_other_series":" | ".join(x["path"] for x in crossdocs)
    })
out=base/os.environ.get("AUDIT_OUTPUT_DIR","independent-audit-2026-11-14")
out.mkdir(exist_ok=True,parents=True)
for name,rows,cols in [
 ("model_exact_coverage.csv",modelrows,["catalog_744_row","brand","model","series_key","model_variant","proof","exact_technical_pdf_count","exact_declaration_count","exact_pdf_names"]),
 ("series_exact_coverage.csv",seriesrows,["brand","series_key","models","exact_models_in_technical_pdfs","exact_models_in_declaration_only","without_model_specific_proof","series_pdf_count","pdfs_with_out_of_group_models","scope_note","models_without_exact_model_proof","pdfs_with_other_series"])
]:
 with (out/name).open("w",encoding="utf-8-sig",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=cols);writer.writeheader();writer.writerows(rows)
repeated=[{"sha256":sha,"paths":paths} for sha,paths in duplicates.items() if len(paths)>1]
bad=[
 {"path":d["path"],"other_models":d["other_scoped_models_on_pages"]}
 for value in doc_index.values() for d in value if d["other_scoped_models_on_pages"]
]
status_counts=Counter(m["proof"] for m in modelrows)
summary={
 "sample":377,"preliminary_families":53,"archive":zip_path.name,
 "archive_sha256":hashlib.sha256(zip_path.read_bytes()).hexdigest(),
 "evidence_counts":dict(status_counts),
 "models_exact_technical":status_counts.get("EXACT_MODEL_TECH_PDF",0),
 "models_declaration_only":status_counts.get("EXACT_MODEL_DECLARATION_ONLY",0),
 "models_missing_exact":status_counts.get("SERIES_ONLY_OR_UNVERIFIED",0),
 "series_with_100pct_exact_model_coverage":sum(x["without_model_specific_proof"]==0 for x in seriesrows),
 "family_group_with_mixed_suffixes": ["IGC/IMS_BH: IMS-BH220NH(DC) & IMS-BH280NH(DC) vs IMS-BH450NB & IMS-BH560NB"],
 "candidate_over_split":["Midea MI2_G and MI2_G_DP share original manufacturer MI2_GDHN18(At)/MI2_GDHN18(At)DP specification family"],
 "duplicate_files_across_folders":repeated,
 "mixed_page_pdfs":bad,
 "failed_pdf_parsing":failed,
 "pdf_count":stats["pdf_total"],"pdf_pages_checked":stats["pages_read"],
 "warning":"An exact SKU string found in PDF is evidence of inclusion, not automatic full specification coverage. Group title alone never counts as model-exact proof."
}
(out/"audit_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
(out/"mixed_page_warnings.json").write_text(json.dumps(bad,ensure_ascii=False,indent=2),encoding="utf-8")
print("FINAL_AUDIT",json.dumps({
 k:v for k,v in summary.items()
 if k not in ("duplicate_files_across_folders","mixed_page_pdfs","failed_pdf_parsing")
},ensure_ascii=False),flush=True)
print("REPEATED_PDFS",len(repeated),"MIXED_PAGE_PDFS",len(bad),"PDF_ERRORS",len(failed),flush=True)
for row in seriesrows:
 if row["without_model_specific_proof"] or row["pdfs_with_out_of_group_models"]:
    print("FLAG",row["brand"],row["series_key"],"exact",row["exact_models_in_technical_pdfs"],
          "declaration",row["exact_models_in_declaration_only"],"without",row["without_model_specific_proof"],
          "cross_doc",row["pdfs_with_out_of_group_models"],flush=True)
