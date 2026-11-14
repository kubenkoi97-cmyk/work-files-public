#!/usr/bin/env python3
"""Correct source-identity error in v6, without altering or deleting historic releases.
Indonesian ATOM 2024 Midea PDF uses model-capacity mapping not safe for the Russian
catalog 744 (MI2-15Q4CDHN18(At): 4.5 kW vs RU product card 1.5 kW).
Archive the prior original in v6 unchanged; remove from the current active pack.
"""
from pathlib import Path
import csv,hashlib,json,sys,zipfile
source=Path(sys.argv[1])
target=Path(sys.argv[2])
with zipfile.ZipFile(source) as zin:
    raw={name:zin.read(name) for name in zin.namelist() if not name.endswith("/")}
audit=json.loads(raw["audit.json"])
ban_source="ATOM_2024"
untrusted_refs=set()
accepted_refs=set()
for group in audit["series_report"]:
    brand=group["brand"];key=group["series"]
    for obj in group.get("catalogue_pages",[]):
        p=f'{brand}/{key}/{obj["pdf"]}'
        if obj["catalogue"]==ban_source:untrusted_refs.add(p)
        else:accepted_refs.add(p)
removed=[]
for name in sorted(untrusted_refs-accepted_refs):
    if name in raw:
        removed.append({"path":name,"bytes":len(raw.pop(name)),"reason":"PROVENANCE_OVERSEAS_CAPACITY_CONFLICT"})
catalogue="Общие каталоги/Midea_ATOM_2024/Полный каталог.pdf"
assert catalogue in raw, "Original source not in input: fail closed"
removed.append({"path":catalogue,"bytes":len(raw.pop(catalogue)),"reason":"OVERSEAS_MI2_MODEL_CAPACITY_CONFLICT"})
reason={
    "archive_version":"v7",
    "scope":"ONLY 377 originally unfilled models of Каталог 744",
    "change":"Quarantine source incompatible with Russian-market SKU meaning; previous v6 historical release preserved",
    "observed_specific_discrepancy":{
        "SKU":"MI2-15Q4CDHN18(At)",
        "overseas_atom_2024_catalog_cooling_kw":4.5,
        "russian_mircli_listing_cooling_kw":1.5,
        "manufacturer_document":"https://www.midea.com/content/dam/midea-aem/id/PD-Midea-Atom-Catalogue-2024-12-25-V7-1.pdf",
        "russian_listing":"https://mircli.ru/Midea-MI2-15Q4CDHN18-At-T-MBQ4-03F/",
        "risk":"Same apparent model marking is not sufficient to transfer numeric specifications between markets"
    },
    "quarantined_paths":removed,
    "retained_source_history":"https://github.com/kubenkoi97-cmyk/work-files-public/releases/tag/mixed-377-technical-docs-2026-11-14-v6",
    "claim_limits":"Family prefixes remain preliminary, and exact models need independently validated manufacturer-market documentation. Do not infer numeric data from a model prefix."
}
raw["READ_FIRST_SOURCE_VALIDATION_V7.json"]=json.dumps(reason,ensure_ascii=False,indent=2).encode("utf-8")
raw["SOURCE_STATUS.txt"]=("MIXED 377, V7. ONLY UNFILLED SHEET MODELS.\n"
 "Model-to-series classification audited in separate repo CSV.\n"
 "Midea overseas ATOM_2024 PDF quarantined: identical-looking code has different capacity scale.\n"
 "This ZIP is not a claim that all 377 technical dossiers are complete.\n"
 "See READ_FIRST_SOURCE_VALIDATION_V7.json and independent-audit-v7-2026-11-14.\n").encode("utf-8")
with zipfile.ZipFile(target,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for name,data in raw.items():z.writestr(name,data)
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
    assert catalogue not in z.namelist()
    assert "READ_FIRST_SOURCE_VALIDATION_V7.json" in z.namelist()
print(json.dumps({"input_bytes":source.stat().st_size,"output_bytes":target.stat().st_size,"removed_count":len(removed),"removed":removed,"pdfs_remaining":sum(n.endswith(".pdf") for n in raw)},ensure_ascii=False,indent=2),flush=True)
