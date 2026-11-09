#!/usr/bin/env python3
"""Retry exact original product pages for 40 PARTIAL SKUs, with Unicode SKU repair.
Source HTML and image bytes remain unmodified; source content must exist on vendor site.
"""
import importlib.util
import json
import re
from pathlib import Path
from PIL import Image

path = Path(__file__).with_name("capture_batch.py")
spec = importlib.util.spec_from_file_location("catalog377_core", path)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

CYR = str.maketrans({"А":"A","В":"B","С":"C","Е":"E","Н":"H","К":"K","М":"M","О":"O","Р":"P","Т":"T","Х":"X","У":"Y",
                     "а":"a","в":"b","с":"c","е":"e","н":"h","к":"k","м":"m","о":"o","р":"p","т":"t","х":"x","у":"y"})
def canon(s):
    return str(s).translate(CYR)

old_key=core.key
core.key=lambda x:old_key(canon(x))

def exact(model, text):
    sku=re.sub(r"\s+","",canon(model)).upper()
    hay=canon(text).upper()
    regex=r"(?<![A-Z0-9])"+re.escape(sku).replace(r"\(",r"\s*\(")+r"(?![A-Z0-9(])"
    return bool(re.search(regex,hay))
core.exact_model_in_text=exact

original_parse=core.parse_source
def parse_with_prose_gate(url,brand,model,response):
    page=original_parse(url,brand,model,response)
    if not page:
        return None
    host=(core.urlparse(page["url"]).hostname or "").lower()
    if host.endswith("effect-nn.ru"):
        soup=page["soup"]
        h1=" ".join(x.get_text(" ",strip=True) for x in soup.select("h1"))
        text=soup.get_text(" ",strip=True)
        i=text.find("Дополнительная информация")
        j=text.find("Вы можете купить кондиционер",i) if i>=0 else -1
        paragraph=text[i:(j if j>i else i+2200)] if i>=0 else ""
        matched=exact(model,h1)
        has_prose=(("Канальный" in paragraph or "внутренний" in paragraph.lower()
                    or "кондиционирован" in paragraph.lower()) and len(paragraph)>=120)
        page["has_description"]=bool(matched and has_prose)
        page["has_specs"]=bool(matched and page["has_specs"])
        print("EXACT_SOURCE_CHECK",json.dumps({"model":model,"url":page["url"],
              "h1_exact":matched,"description_length":len(paragraph),
              "description_valid":page["has_description"],
              "image_url_candidates":len(page["photos"])},ensure_ascii=False),flush=True)
    return page
core.parse_source=parse_with_prose_gate

original_capture=core.capture
def capture_with_image_gate(row, dirpath):
    result=original_capture(row,dirpath)
    if result.get("status")=="COMPLETE":
        folder=dirpath/(row["brand"]+"_"+core.safe(row["model"]))
        verified=[]
        for item in result.get("image_files",[]):
            file=folder/"page_files"/item["file"]
            try:
                with Image.open(file) as im: im.verify()
                with Image.open(file) as im: width,height=im.size
                if min(width,height)>=180:
                    verified.append({"file":item["file"],"width":width,"height":height})
            except Exception: pass
        result["verified_photo_dimensions"]=verified
        if not verified:
            result["status"]="PARTIAL"
            result["reason"]="No independently decoded image >=180x180 in new source"
        (folder/"manifest.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
        print("IMAGE_QA",row["model"],result["status"],len(verified),flush=True)
    return result
core.capture=capture_with_image_gate

if __name__=="__main__":
    core.main()
