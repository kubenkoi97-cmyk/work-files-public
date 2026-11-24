import concurrent.futures as cf, csv, hashlib, json, pathlib, re, zipfile, requests, fitz
from collections import defaultdict
ROOT=pathlib.Path("/tmp/climate347"); ROOT.mkdir(exist_ok=True)
def models(prefix, nums, suffix): return [prefix+str(n)+suffix for n in nums.split()]
a="250 290 340 400 450 500 560 615 670 730 785 850 900 950 1010"
b="252 280 335 400 450 500 560 615 670 730 785 850 900 950 1010 1060 1120 1170"
c="224 280 335 400 450 500 560 615 670 730 785 850"
d="250 290 340 400 450 500 560 615 680 730 800 850 900 950 1010"
e="220 330 440 550 660 770 880 990 1100 1210 1320"
f="022 026 035 043 061 087 105 122 156"
out="naruzhnye_bloki_VRF_sistem_"; inn="vnutrennie_bloki_VRF_sistem_"
vrf="multizonalnye_vrv_i_vrf_sistemy/"
groups=[]
def add(brand,group,kind,filename,urls,ms,folder,notes=""):
    groups.append(dict(brand=brand,group=group,kind=kind,filename=filename,urls=urls.split(" | "),models=ms,folder=folder,notes=notes))
add("Midea","MIH-T1","catalog","MIH_T1_catalog.pdf","https://oldachtrading.com/wp-content/uploads/PD__Midea_V8%20IDU_VRF_Catalog_2025-03-05_V12_compressed.pdf",models("MIH","112 125 140 160 200 224 252 280 335 400 450 560","T1HN18"),vrf+inn+"Midea","Regional applicability review required; original catalog only")
add("Midea","MIH-DL","manual","MIH_DL_installation_and_user_manual.pdf","https://www.c-o-k.ru/library/instructions/midea/kondicionery-promyshlennye/38667/142834.pdf?download= | https://www.c-o-k.ru/library/instructions/midea/kondicionery-promyshlennye/38667/142834.pdf",models("MIH","36 45 56 71 80 90 100 112 125 140","DLHN18"),vrf+inn+"Midea")
add("Midea","MIH-F3/F4/F5","technical","MIH_F3_F4_F5_technical_manual.pdf","https://www.c-o-k.ru/library/instructions/midea/kondicionery-promyshlennye/38666/142833.pdf?download= | https://www.c-o-k.ru/library/instructions/midea/kondicionery-promyshlennye/38666/142833.pdf",sum([models("MIH","22 28 36 45 56 71 80",s+"HN18") for s in ["F3","F4","F5"]],[]),vrf+inn+"Midea")
add("Midea","MIH-FS/FL","catalog","MIH_FS_FL_catalog.pdf","https://oldachtrading.com/wp-content/uploads/PD__Midea_V8%20IDU_VRF_Catalog_2025-03-05_V12_compressed.pdf",models("MIH","252 280 335 450 560","FSHN18")+models("MIH","252 280 335 450 560","FLHN18"),vrf+inn+"Midea","Regional applicability review required; original catalog only")
add("Daikin","VRV IV S winter","catalog","VRV_IV_S_winter_catalog.pdf","https://www.thermotrade.ru/wp-content/uploads/2024/04/daikin-vrv-2024.pdf",["RXYSQ"+s+"/-40" for s in "4T8V 5T8V 6T8V 4T8Y 5T8Y 6T8Y 8TY 10TY 12TY".split()],vrf+out+"Daikin","Winter option exact code required")
add("Daikin","VRV IV+ winter","catalog","VRV_IVplus_winter_catalog.pdf","https://www.thermotrade.ru/wp-content/uploads/2024/04/daikin-vrv-2024.pdf",models("RXYQ","8 10 12 14 16 18 20","U/-40"),vrf+out+"Daikin","Winter option exact code required")
add("Daikin","REMQ5U","wiring","REMQ5U_wiring_diagram.pdf","https://www.daikin.es/content/dam/MDM/TechnicalDrawings/VRV/REYQ-U%20%2B%20REMQ-U/EN/REMQ5U_REYQ8-12U_wir3_2D120651A-1_EN.pdf",["REMQ5U"],vrf+out+"Daikin")
add("Daikin","RYMQ-U","technical","RYMQ_U_technical_manual.pdf","https://leacond.com.ua/wp-content/uploads/2024/02/ryyq-u_eedru19_data-books_russian.pdf",models("RYMQ","8 10 12 14 16 18 20","U"),vrf+out+"Daikin")
add("Bosch","MDCI 8-18","installation","MDCI_8_18_installation_manual.pdf","https://www.bosch-homecomfort.com/web-etk/documents/doc?id=423339",["MDCI "+s for s in "12-1 14-1 16-1 12-3 14-3 16-3 18-3".split()],vrf+out+"Bosch")
add("Bosch","MDCI 22-26","installation","MDCI_20_22_26_3_installation_manual.pdf","https://www.manualslib.de/manual/1061636/Bosch-Mdci-Serie.html",["MDCI 22-3","MDCI 26-3"],vrf+out+"Bosch","HTML source; reject non-PDF response")
add("Bosch","MDCI 40-45","installation","MDCI-40_45-_-montazh.pdf","https://air-bosch.com/upload/iblock/27f/gdrfmtslc5togl6w48x7io8b2i28ioti/MDCI-40_45-_-montazh.pdf",["MDCI 40-3","MDCI 45-3"],vrf+out+"Bosch")
add("Kentatsu","DX PRO VII","catalog","DX_PRO_VII_catalog.pdf","https://www.c-o-k.ru/library/instructions/kentatsu/kondicionery-promyshlennye/37986/140011.pdf",models("KTRB",a,"HZAN3"),vrf+out+"Kentatsu")
add("Kentatsu","DX PRO VII Individual","catalog","DX_PRO_VII_Individual_catalog.pdf","https://www.c-o-k.ru/library/instructions/kentatsu/kondicionery-promyshlennye/37986/140011.pdf",models("KTRB",a,"HZAN3-i"),vrf+out+"Kentatsu")
add("Kentatsu","DX PRO Compact","manual","KYRA_A_installation_and_user_manual.pdf","https://daichi.business/documents/download.php?ID=16756",models("KYRA","80 100 120 140 160 180","HZAN1-A"),vrf+out+"Kentatsu")
add("Kentatsu","DX PRO A + mini","manual","DX_PRO_A_user_manual.pdf","https://kentatsuair.ru/library/kentatsu-kvag1010czan3-kvam80hzan1i-instruktsiya-ekspluatatsiya.pdf?v=284dc162eed6c9cab797614c77b4634fa2ee38e3c82ae7009d46fb8af72d2e5f | https://kentatsuair.ru/library/kentatsu-kvag1010czan3-kvam80hzan1i-instruktsiya-ekspluatatsiya.pdf",models("KVAM","80 100 120 140 160","HZAN1i")+models("KVAM","120 140 160 220 260","HZAN3i")+models("KVAH","250 340 730 800 900 950 1010","HZAN3")+models("KVAG",d,"HZAN3")+models("KVAG",d,"CZAN3"),vrf+out+"Kentatsu")
add("Midea","ATOM B","manual","ATOM_B_installation_and_user_manual.pdf","https://air-midea.com/upload/iblock/1f4/euymk0wyekscfn9tbt73pdjzeq12tfwu.pdf",models("MVUH","35 50 60 100 120","BT-VA1"),vrf+out+"Midea")
add("Midea","ATOM B 200","manual","ATOM_B_200_installation_and_user_manual.pdf","https://www.c-o-k.ru/library/instructions/midea/kondicionery-promyshlennye/37793/138737.pdf",["MVUH200BT-VA1"],vrf+out+"Midea")
add("Midea","V8Si","catalog","V8Si_catalog.pdf","https://onokom.ru/dok/midea/2024/catalog/2024-catalog-v8s.pdf",models("MV8Si-","252 280 335 400 450 500 560 615 670","WV2GN1"),vrf+out+"Midea")
add("Midea","VC MAX","manual","VC_MAX_installation_and_user_manual.pdf","https://24wvent.ru/documentation/3/MD23IU-046B-RU_27_11_23.pdf",models("MVC-M",c,"WV2GN1"),vrf+out+"Midea")
add("Midea","V8-i PRO","manual","V8_V8i_PRO_installation_and_user_manual.pdf","https://www.d-ks.ru/upload/iblock/77c/o82cqsoczelv5l85p17jgz0erk3s3df5.pdf",models("MV8i-","1060 1120 1170","WV2GN1(PRO)"),vrf+out+"Midea")
add("Midea","V8-i ULTRA","catalog","V8i_ULTRA_catalog.pdf","https://www.thermotrade.ru/wp-content/uploads/2024/08/midea_vrf_2024-2025.pdf",models("MV8i-",b,"WV2GN1(ULTRA)"),vrf+out+"Midea")
add("Midea","V4+W","catalog","V4plusW_catalog.pdf","https://www.c-o-k.ru/library/catalogs/midea/37988/140017.pdf",models("MVUW","252 280 335","A-VA3"),vrf+out+"Midea")
winter="https://www.thermotrade.ru/wp-content/uploads/2024/08/midea_vrf_2024-2025.pdf"
add("Midea","winter variants","catalog","Midea_winter_catalog.pdf",winter,models("MV8M-","80 100 120 140 160 170","WV2HN1/-40")+models("MV8M-","120 140 160 170","WV2GN1/-40")+models("MV8S-","252 280 335 400 450 500 560 615 670","WV2GN1/-40")+models("MV8Si-","252 280 335 400 450 500 560 615 670","WV2GN1/-40")+models("MVC-M",c,"WV2GN1/-40")+models("MV8-"," ".join(b.split()[:15]),"WV2GN1(PRO)/-40")+models("MV8i-",b,"WV2GN1(PRO)/-40"),vrf+out+"Midea","Exact winter suffix required; do not infer")
imbr=models("IMBR-C",e,"ANB")+models("IMBR-H",e,"ANB")+["IMBRG-C440ANB","IMBRG-H220ANB","IMBRG-H330ANB","IMBRG-H440ANB"]
add("IGC","IMBR/IMBRG","passport","IGC_IMBR_passport.pdf","https://iclim.ru/library/igc-imbr-r-pasport.pdf | https://igc.com.ru/library/igc-imbr-r-pasport.pdf | https://krasnodar.iclim.ru/library/igc-imbr-r-pasport.pdf",imbr,"chillery/IGC")
add("IGC","IMBR/IMBRG manufacturer candidate","technical","IGC_IMBR_manufacturer.pdf","https://igc-aircon.com/upload/iblock/007/codppkj23zxnh6ke3yzga38g8ogx782q.pdf",imbr,"chillery/IGC","Document type requires visual verification")
add("IGC","IRFT-Q","declaration","IGC_IRFT_Q_declaration.pdf","https://igc.com.ru/library/igc-eaes-n-ru-d-cn-ra01-v-90529-26-deklaratsiya.pdf | https://kzn.iclim.ru/library/igc-eaes-n-ru-d-cn-ra01-v-90529-26-deklaratsiya.pdf | https://spb.iclim.ru/library/igc-eaes-n-ru-d-cn-ra01-v-90529-26-deklaratsiya.pdf",models("IRFT-",f,"HA/NB-Q")+models("IRFT-",f,"CA/NB-Q"),"rooftopy/IGC","Declaration is not technical coverage")
# Original bytes only; no synthetic PDFs. Reject non-PDF or unreadable responses.
unique={tuple(g["urls"]) for g in groups}
def fetch(urls):
    errs=[]
    for u in urls:
        try:
            with requests.get(u,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf,*/*"},timeout=(12,30),stream=True) as r:
                r.raise_for_status()
                chunks=[]; size=0
                for ch in r.iter_content(1024*1024):
                    if ch: chunks.append(ch);size+=len(ch)
                    if size>160*1024*1024: raise ValueError("PDF over 160 MB limit")
                    if len(chunks)==1 and not chunks[0].lstrip().startswith(b"%PDF-"): raise ValueError("not PDF")
                raw=b"".join(chunks)
                if not raw.lstrip().startswith(b"%PDF-"): raise ValueError("not PDF")
            with fitz.open(stream=raw,filetype="pdf") as doc:
                if not len(doc): raise ValueError("empty PDF")
                pages=[p.get_text() for p in doc]
                doc[0].get_pixmap(matrix=fitz.Matrix(.3,.3))
            return (u,raw,pages,"")
        except Exception as exc: errs.append(u+": "+str(exc)[:250])
    return ("",None,[]," | ".join(errs))
def exact_pages(m,pages):
    # Preserve model punctuation, allow PDF whitespace, disallow suffix extensions.
    m=re.sub(r"\s+","",m)
    pat=r"(?<![A-Za-z0-9])"+r"\s*".join(re.escape(ch) if ch!="-" else r"[-‐‑–−]" for ch in m)+r"(?![A-Za-z0-9_/-])"
    return [i+1 for i,p in enumerate(pages) if re.search(pat,p,re.I)]
with cf.ThreadPoolExecutor(max_workers=12) as ex:
    results=dict(zip(unique,ex.map(fetch,unique)))
rows=[]; docs=[]; saved={}; cover=set(); declarations=set()
zipname=ROOT/"Climate_347_PDF_stage4_partial.zip"
with zipfile.ZipFile(zipname,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as z:
    for g in groups:
        u,raw,pages,error=results[tuple(g["urls"])]
        sha=hashlib.sha256(raw).hexdigest() if raw else ""
        path=""
        if raw:
            if sha not in saved:
                path="ORIGINAL_PDF/"+g["brand"]+"/"+g["filename"]
                if path in saved.values(): path=path[:-4]+"_"+sha[:8]+".pdf"
                z.writestr(path,raw);saved[sha]=path
            path=saved[sha]
        hits=0
        for m in g["models"]:
            pp=exact_pages(m,pages)
            status="EXACT_TEXT_MATCH_REVIEW_REQUIRED" if pp else ("DOWNLOADED_NO_EXACT_TEXT" if raw else "DOWNLOAD_FAILED")
            if pp:
                hits+=1
                (declarations if g["kind"]=="declaration" else cover).add((g["brand"],m))
            rows.append(dict(brand=g["brand"],series=g["group"],model=m,document_kind=g["kind"],source=u or g["urls"][0],archive_path=path,sha256=sha,pages=" ".join(map(str,pp)),status=status,notes=g["notes"],target_folder=g["folder"]+"/2026/",proposed_filename=g["filename"],error=error))
        docs.append(dict(brand=g["brand"],series=g["group"],source=u or g["urls"][0],archive_path=path,bytes=len(raw) if raw else 0,pages=len(pages),sha256=sha,exact_text_matches=hits,requested_models=len(g["models"]),error=error))
    for name,records in [("model_evidence.csv",rows),("document_manifest.csv",docs)]:
        p=ROOT/name
        with p.open("w",encoding="utf-8-sig",newline="") as fcsv:
            w=csv.DictWriter(fcsv,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
        z.write(p,"REPORTS/"+name)
    summary=dict(distinct_pdf_files=len(saved),downloaded_source_groups=sum(bool(x["archive_path"]) for x in docs),source_groups=len(docs),models_with_exact_technical_text=len(cover),models_with_exact_declaration_text=len(declarations),unique_models_attempted=len({(x["brand"],x["model"]) for x in rows}),catalog_total=347,ready_for_selectel=0,warning="PARTIAL original PDF package; text evidence only. Visual and regional verification and catalog excerpts pending. No Selectel upload or Excel edits.")
    z.writestr("REPORTS/summary.json",json.dumps(summary,ensure_ascii=False,indent=2))
with zipfile.ZipFile(zipname) as z: assert z.testzip() is None
summary["archive_sha256"]=hashlib.sha256(zipname.read_bytes()).hexdigest()
(ROOT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary),flush=True)
for x in docs: print(x["brand"],x["series"],x["bytes"],x["exact_text_matches"],x["error"][:180],flush=True)
assert len(saved)>0, "No valid PDFs fetched"
