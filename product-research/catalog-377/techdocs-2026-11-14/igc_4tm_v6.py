#!/usr/bin/env python3
"""Append authentic SKU-matching IGC PDF documentation to verified v5 ZIP.
Recover only if PDF bytes valid, and some exact requested 4TM(DC5) matches are present.
"""
import hashlib,json,re,requests,sys,zipfile
from pathlib import Path
import fitz
src=Path(sys.argv[1]);output=Path(sys.argv[2])
with zipfile.ZipFile(src) as z: files={n:z.read(n) for n in z.namelist() if not n.endswith("/")}
models=["IMS-4TM15NH(DC5)","IMS-4TM28NH (DC5)","IMS-4TM36NH(DC5)","IMS-4TM45NH(DC5)","IMS-4TM56NH(DC5)"]
sources=[
 ("installation_and_user_manual","https://igc-aircon.com/upload/iblock/2fd/g7gqb0wx6uqkoxuz7qf9lnhfzsxzpmks.pdf",False),
 ("installation_and_user_manual","https://igc-aircon.com/upload/iblock/2fd/g7gqb0wx6uqkoxuz7qf9lnhfzsxzpmks.pdf",True),
 ("declaration","https://docs.proclimate5.ru/kompressorno_kondensatornye_bloki/IGC/IMS_deklaracsia.pdf",False),
]
def exact(model,txt):
    m=re.sub(r"\s+","",model.upper())
    patt=r"(?<![A-Z0-9])"+r"\s*".join(map(re.escape,m))+r"(?![A-Z0-9])"
    return bool(re.search(patt,txt.upper()))
results=[];found_types=set()
for dtype,url,insecure in sources:
    if dtype in found_types:continue
    try:
        resp=requests.get(url,timeout=(15,65),verify=not insecure,headers={"User-Agent":"Mozilla/5.0"})
        resp.raise_for_status();payload=resp.content
        if not payload.startswith(b"%PDF-"):raise ValueError("not a PDF")
        doc=fitz.open(stream=payload,filetype="pdf")
        matches={m:[i+1 for i,p in enumerate(doc) if exact(m,p.get_text())] for m in models}
        matches={m:pages for m,pages in matches.items() if pages}
        if not matches:raise ValueError("requested exact DC5 SKUs not present")
        dest="IGC/IMS_4TM/IMS_4TM_"+dtype+".pdf"
        files[dest]=payload
        results.append({"status":"accepted","type":dtype,"source_url":url,"verification":"SHA256+PDF magic+exact SKU strings","transport_cert_verified":not insecure,"pages":len(doc),"bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest(),"target_path":dest,"exact_matches":matches,"unmatched":sorted(set(models)-set(matches))})
        found_types.add(dtype)
        print("VERIFIED",dtype,"SKU",len(matches),"PAGES",len(doc),"BYTES",len(payload),flush=True)
    except Exception as e:
        results.append({"status":"not_recovered","type":dtype,"url":url,"insecure_transport":insecure,"error":str(e)[:190]})
        print("NOT_RECOVERED",dtype,str(e)[:190],flush=True)
files["igc_4tm_v6_status.json"]=json.dumps({"scope":"Only preselected 377 unfilled model scope","series":"IMS_4TM","models":models,"results":results,"warning":"A declaration is evidence of listing, not a technical datasheet; a family manual covers only explicitly listed models. Do not transfer specs from DC4/DC7 to DC5."},ensure_ascii=False,indent=2).encode("utf-8")
with zipfile.ZipFile(output,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for n,data in files.items():z.writestr(n,data)
with zipfile.ZipFile(output) as z:
    assert z.testzip() is None
print("V6_FINAL",json.dumps({"size":output.stat().st_size,"IGC_4TM_PDFs":[r for r in results if r["status"]=="accepted"],"scope_unmodified":True},ensure_ascii=False),flush=True)
