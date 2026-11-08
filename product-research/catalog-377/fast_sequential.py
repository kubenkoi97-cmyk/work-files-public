#!/usr/bin/env python3
"""Catalog377 fast sequential exact-model archival.

One SKU at a time: quick source discovery -> exact match -> archive resources
-> validate ZIP/images -> publish release -> commit per-SKU checkpoint.
Never modify old immutable source snapshots or use a sibling SKU's page.
"""
import argparse,csv,hashlib,io,json,os,re,subprocess,sys,tempfile,time,zipfile
from pathlib import Path
from urllib.parse import urlencode,urlparse,urljoin
from bs4 import BeautifulSoup
from PIL import Image

sys.path.insert(0,str(Path(__file__).parent))
import capture_batch as c

ROOT=Path("product-research/catalog-377")
STATUS=ROOT/"status"
TRACK=STATUS/"fast-sequential"
TRACK.mkdir(exist_ok=True,parents=True)
REPO="kubenkoi97-cmyk/work-files-public"

def run(cmd,timeout=90):
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
    if p.returncode:raise RuntimeError("CMD failed: "+" ".join(cmd)+" "+(p.stderr or p.stdout)[-280:])
    return p.stdout.strip()

def git_checkpoint(paths,message):
    paths=[str(p) for p in paths]
    run(["git","config","user.name","github-actions[bot]"])
    run(["git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com"])
    run(["git","add",*paths])
    if not subprocess.run(["git","diff","--cached","--quiet"]).returncode:
        run(["git","commit","-m",message])
    else:return
    for attempt in range(10):
        try:
            run(["git","pull","--rebase","origin","main"],timeout=35)
            run(["git","push","origin","HEAD:main"],timeout=45)
            return
        except Exception as exc:
            print("GIT_PUSH_RETRY",attempt+1,str(exc)[:170],flush=True)
            time.sleep(2+attempt*2)
    raise RuntimeError("Cannot commit SKU checkpoint; local file remains, do not claim publication")

def source_urls_from_rss(brand,model):
    qlist=[f'"{model}" "{brand}" описание характеристики',f'"{model}" купить']
    result=[]
    for q in qlist:
        url="https://www.bing.com/search?format=rss&"+urlencode({"q":q})
        r=c.get(url,timeout=7)
        if not r:continue
        soup=BeautifulSoup(r.text,"xml")
        for item in soup.find_all("item"):
            href=item.find("link").get_text(" ",strip=True) if item.find("link") else ""
            title=item.find("title").get_text(" ",strip=True) if item.find("title") else ""
            if href and c.key(model) in c.key(title+" "+href):
                if urlparse(href).hostname and not any(h in urlparse(href).hostname for h in ("bing.com","google.com","youtube.com","yandex.ru")):
                    result.append(href)
    return list(dict.fromkeys(result))

def exact_links(brand,model,old):
    candidates=[]
    # MirCli remains the first priority; only two distinct likely direct
    # patterns because previous 377-SKU audits already exhausted broad search.
    candidates.extend(c.slug_candidates(brand,model)[:2])
    if brand=="IGC":
        candidates.extend(c.igc_http_candidates(model))
    # Confirmed direct seller sources are useful only when not already the
    # known incomplete original HTML for the same SKU.
    if brand=="Kentatsu":
        suffix=model.lower()
        candidates.extend([
          f"https://climatehnik.com/search/?q={model}",
          f"https://coolsochi.ru/product/kentatsu-{suffix}/",
          f"https://ryazan.vsekondicioneri.ru/product/kentatsu-{suffix}/",
        ])
    if brand=="Midea":
        suffix=model.lower().replace("(","-").replace(")","")
        candidates.extend([
          f"https://coolsochi.ru/product/midea-{suffix}/",
          f"https://russia-midea.ru/midea-{suffix}/",
        ])
    candidates.extend(source_urls_from_rss(brand,model))
    cleaned=[]
    for u in candidates:
        parsed=urlparse(u)
        if parsed.scheme not in ("http","https") or not parsed.netloc:continue
        if any(x in parsed.netloc for x in ("youtube.com","google.com","bing.com")):continue
        if u.rstrip("/")==old.get("source_url","").rstrip("/"):continue
        if u not in cleaned:cleaned.append(u)
    return cleaned[:9]

def real_narrative(page,model):
    """Find actual *product* descriptive content, not navigation 'Описание'."""
    soup=page["soup"]
    evidence=[]
    for node in soup.find_all("script",type="application/ld+json"):
        try: obj=json.loads(node.get_text())
        except (ValueError,TypeError):continue
        queue=(obj if isinstance(obj,list) else [obj])
        while queue:
            item=queue.pop()
            if not isinstance(item,dict):continue
            if isinstance(item.get("@graph"),list):queue.extend(item["@graph"])
            if "Product" in str(item.get("@type","")) and c.exact_model_in_text(model,item.get("name","")):
                val=BeautifulSoup(str(item.get("description","")),"html.parser").get_text(" ",strip=True)
                if len(val)>100:evidence.append(val)
    selectors=["[itemprop='description']","#description",".product-description",
               ".product__description",".product_detail_description",".detail_text",
               ".product-detail__description",".description-text","#tab-description",
               "[data-tab='description']",".description"]
    for selector in selectors:
        for node in soup.select(selector)[:3]:
            if node.find_parent(["nav","footer","header"]):continue
            txt=node.get_text(" ",strip=True)
            if 110<=len(txt)<12000:
                if re.search(r"внутренн|кондицион|охлажден|обогрев|воздух|вентиляц|блок",txt,re.I):
                    evidence.append(txt)
    return max((len(text) for text in evidence),default=0),bool(evidence)

def discover(brand,model,old):
    attempted=[]
    best=None;best_site=None
    for url in exact_links(brand,model,old):
        attempted.append(url)
        response=c.get(url,timeout=8)
        page=c.parse_source(url,brand,model,response)
        if not page:continue
        length,has_narrative=real_narrative(page,model)
        page["has_description"]=has_narrative
        if not page["has_specs"] or not page["photos"]:
            continue
        site=urlparse(page["url"]).hostname
        if has_narrative:
            print("FOUND_FULL_SOURCE",brand,model,page["url"],"NARRATIVE_CHARS",length,flush=True)
            return page,attempted,site
        if best is None or len(page["photos"])>len(best["photos"]):
            best,best_site=page,site
    return best,attempted,best_site

def validate_archive(path,manifest,brand,model):
    with zipfile.ZipFile(path) as z:
        bad=z.testzip()
        if bad:raise RuntimeError("CRC failed for "+bad)
        modeldir="products/"+brand+"_"+c.safe(model)+"/"
        for item in ("original.html","server-source-original.html","offline.html","manifest.json"):
            if modeldir+item not in z.namelist():
                raise RuntimeError("Missing source file "+item)
        photos=manifest.get("image_files",[])
        if not photos:raise RuntimeError("No downloaded product images")
        valid=0
        for photo in photos:
            p=modeldir+"page_files/"+photo["file"]
            if p not in z.namelist():raise RuntimeError("Missing product photo "+p)
            with Image.open(io.BytesIO(z.read(p))) as im:
                im.verify()
                if im.width>=150 and im.height>=150:valid+=1
        if not valid:raise RuntimeError("No decodable product photo >=150px")
        with z.open(modeldir+"original.html") as f:
            soup=BeautifulSoup(f.read().decode("utf-8","replace"),"html.parser")
        head=" ".join(h.get_text(" ",strip=True) for h in soup.find_all("h1"))
        title=soup.title.get_text(" ",strip=True) if soup.title else ""
        if not c.exact_model_in_text(model,head+" "+title):
            raise RuntimeError("Wrong model in HTML heading, rejecting ZIP")
        return valid

def archive_and_publish(row,page,attempts,site,prior_status):
    model,brand,idx=row["model"],row["brand"],int(row["row"])
    key=f"{idx:03d}"
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);target=root/"products"
        previous=c.choose_source
        c.choose_source=lambda b,m:(page,attempts,site)
        # Prioritize model photos, then a bounded selection of CSS/JS/images;
        # preserve the entire server HTML separately as raw original bytes.
        old_assets=c.choose_download_urls
        c.choose_download_urls=lambda p:dict(list(old_assets(p).items())[:65])
        try:
            manifest=c.capture(row,target)
        finally:
            c.choose_source=previous
            c.choose_download_urls=old_assets
        if manifest["status"]=="ERROR":raise RuntimeError(manifest.get("error","capture failed"))
        zipname=f"catalog377-fast-{key}-{c.safe(brand)}-{c.safe(model)}.zip"
        zpath=root/zipname
        statfile=root/"status.csv"
        fields=["excel_row","brand","model","status","site","source_url","has_description",
             "has_specs","photo_links_found","downloaded_product_photos","downloaded_page_assets","reason"]
        with statfile.open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fields,extrasaction="ignore");w.writeheader();w.writerow(manifest)
        with zipfile.ZipFile(zpath,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=4) as z:
            for p in target.rglob("*"):
                if p.is_file():z.write(p,p.relative_to(root))
            z.write(statfile,"status.csv")
        valid=validate_archive(zpath,manifest,brand,model)
        tag=f"catalog377-fast-{key}"
        args=["gh","release","view",tag,"--repo",REPO]
        exists=subprocess.run(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
        if exists:
            run(["gh","release","upload",tag,str(zpath),str(statfile),"--repo",REPO,"--clobber"],timeout=130)
        else:
            run(["gh","release","create",tag,str(zpath),str(statfile),"--repo",REPO,
                 "--title",f"Catalog377 {key}: {brand} {model} original product HTML",
                 "--notes",f"Authentic exact SKU HTML, offline HTML, local gallery. Archive status {manifest['status']}. Older PARTIAL sources retained; exact model verified."],timeout=130)
        assets=json.loads(run(["gh","release","view",tag,"--repo",REPO,"--json","assets"],timeout=40))
        if not any(a.get("name")==zipname and a.get("size",0)>1000 for a in assets.get("assets",[])):
            raise RuntimeError("Release did not confirm uploaded ZIP")
        manifest["release_url"]=f"https://github.com/{REPO}/releases/tag/{tag}"
        manifest["zip_url"]=f"https://github.com/{REPO}/releases/download/{tag}/{zipname}"
        manifest["local_zip_sha256"]=hashlib.sha256(zpath.read_bytes()).hexdigest()
        manifest["verified_local_product_images"]=valid
        manifest["zip_size"]=zpath.stat().st_size
        # This per-model status is reconciled into master_status.csv. Only
        # publish for a genuinely archived individual exact-model product.
        per=STATUS/f"fast-{key}.csv"
        enriched=dict(manifest)
        enriched.update(archive_release_url=manifest["release_url"],
                        archive_download_url=manifest["zip_url"],
                        archive_sha256=manifest["local_zip_sha256"])
        with per.open("w",encoding="utf-8-sig",newline="") as fd:
            writer=csv.DictWriter(fd,fieldnames=fields+
                ["archive_release_url","archive_download_url","archive_sha256"],
                extrasaction="ignore")
            writer.writeheader();writer.writerow(enriched)
        return manifest,per

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--max-models",type=int,default=62)
    ap.add_argument("--start-row",type=int,default=1)
    ap.add_argument("--end-row",type=int,default=377)
    args=ap.parse_args()
    inventory=c.inventory()
    with (STATUS/"master_status.csv").open(encoding="utf-8-sig",newline="") as f:
        master={(r["brand"],r["model"]):r for r in csv.DictReader(f)}
    pending=[row for row in inventory
             if args.start_row<=int(row["row"])<=args.end_row
             and master[(row["brand"],row["model"])]["status"]!="COMPLETE"]
    pending.sort(key=lambda row:int(row["row"]))
    print("SEQUENTIAL_START",len(pending),"MAX",args.max_models,flush=True)
    for pos,row in enumerate(pending[:args.max_models],start=1):
        brand,model,idx=row["brand"],row["model"],int(row["row"])
        key=f"{idx:03d}"
        old=master[(brand,model)]
        checkpoint=TRACK/f"{key}.json"
        if checkpoint.exists():
            try:
                prior=json.loads(checkpoint.read_text())
                if prior.get("result")=="COMPLETE" and prior.get("release_verified"):
                    print("SKIP_COMPLETED",key,brand,model,flush=True)
                    continue
            except (ValueError,OSError):pass
        print("MODEL_BEGIN",pos,"of",min(len(pending),args.max_models),key,brand,model,flush=True)
        started=time.time()
        outcome={"excel_row":idx,"brand":brand,"model":model,
                 "previous_status":old["status"],"original_source":old.get("source_url",""),
                 "started_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())}
        paths=[checkpoint]
        try:
            c.HTTP_ATTEMPT_LOG.clear()
            page,attempted,site=discover(brand,model,old)
            outcome["attempted_urls"]=attempted
            outcome["http_attempts"]=c.HTTP_ATTEMPT_LOG[-60:]
            if page is None:
                outcome.update(result="NO_NEW_SOURCE",reason="No exact additional vendor HTML with specifications and product photos")
            elif page["url"].rstrip("/")==old.get("source_url","").rstrip("/") and old["status"]=="PARTIAL":
                outcome.update(result="NO_IMPROVEMENT",reason="Page is same as existing partial HTML")
            elif not page["has_description"] and old["status"]=="PARTIAL":
                outcome.update(result="PARTIAL_ALTERNATIVE_FOUND",alternative_source=page["url"],
                       reason="New exact source still has no product narrative; existing archive unchanged")
            else:
                result,per=archive_and_publish(row,page,attempted,site,old["status"])
                paths.append(per)
                outcome.update(result=result["status"],release_verified=True,
                    release_url=result["release_url"],archive_url=result["zip_url"],
                    source_url=result["source_url"],
                    saved_product_photos=result["verified_local_product_images"],
                    zip_sha256=result["local_zip_sha256"])
        except Exception as exc:
            outcome.update(result="ERROR",reason=str(exc)[:450])
            print("MODEL_ERROR",key,brand,model,str(exc)[:250],flush=True)
        outcome["finished_utc"]=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
        outcome["elapsed_seconds"]=round(time.time()-started,1)
        checkpoint.write_text(json.dumps(outcome,ensure_ascii=False,indent=2),encoding="utf-8")
        try:
            git_checkpoint(paths,f"Catalog377 SKU {key}: {brand} {model} {outcome['result']}")
        except Exception as exc:
            print("CHECKPOINT_FAILED",key,str(exc)[:350],flush=True)
            raise
        print("MODEL_SAVED",key,brand,model,outcome["result"],
              outcome.get("archive_url",""),"SECONDS",outcome["elapsed_seconds"],flush=True)
    print("SEQUENTIAL_DONE",min(len(pending),args.max_models),flush=True)
if __name__=="__main__":
    main()
