import pathlib,io,hashlib,json,csv,base64,re,zipfile,time,concurrent.futures
import requests,fitz
from bs4 import BeautifulSoup
from PIL import Image,ImageOps,ImageDraw
import numpy as np
from urllib.parse import urljoin
R=pathlib.Path('climate-347/images');O=pathlib.Path('stage15b-out');O.mkdir(exist_ok=True)
def get(u,limit=65_000_000,ref=None):
    with requests.get(u,headers={'User-Agent':'Mozilla/5.0 (compatible; product research)','Referer':ref or u},timeout=(7,20),stream=True) as r:
        r.raise_for_status();d=bytearray()
        for chunk in r.iter_content(65536):
            d.extend(chunk)
            if len(d)>limit:raise ValueError('size limit')
        return bytes(d),r.url
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
def save(im):
    im=im.convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);im=bg.convert('RGB')
    a=np.asarray(im);y,x=np.where((a<=242).any(axis=2))
    if not len(x):raise ValueError('blank')
    crop=im.crop((int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)));w,h=crop.size
    if max(w,h)<250 or min(w,h)<100:raise ValueError('thumbnail')
    ph=hashlib.sha256(f'{im.width}x{im.height}:'.encode()+im.tobytes()).hexdigest()
    f=O/'native'/(ph[:24]+'.png');f.parent.mkdir(exist_ok=True)
    if not f.exists():im.save(f)
    fac=750/max(w,h);crop=crop.resize((round(w*fac),round(h*fac)),Image.Resampling.LANCZOS);out=Image.new('RGB',(850,850),'white');out.paste(crop,((850-crop.width)//2,(850-crop.height)//2))
    jf=O/'review'/(ph[:24]+'.jpg');jf.parent.mkdir(exist_ok=True);out.save(jf,quality=96,subsampling=0)
    return dict(source_width=im.width,source_height=im.height,object_width=w,object_height=h,upscale=round(fac,4),pixel_sha256=ph,review_sha256=hashlib.sha256(jf.read_bytes()).hexdigest(),file=str(jf.relative_to(O)))
def writecsv(path,rows,fields):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

rows=[]
for model,host,filename in [('RYMQ14-20U','www.daikin.eu','RYMQ14-20U.tif'),('RXYQ14-20U','www.daikin.co.uk','RXYQ14-20U.tif')]:
    base='https://'+host+'/content/dam/MDM/Pictures/VRV/OutdoorUnits/Packshots/'+filename
    # Actual public asset path from official labelled thumbnail; try original first, then standard public rendition paths.
    for u in [base,base+'/_jcr_content/renditions/original',base+'/_jcr_content/renditions/cq5dam.web.1280.1280.jpeg',base+'/_jcr_content/renditions/cq5dam.web.600.600.jpeg',base+'/_jcr_content/renditions/cq5dam.thumbnail.319.319.png']:
        try:
            data,final=get(u,30_000_000);im=Image.open(io.BytesIO(data));im.load()
            a=save(im);rows.append(dict(model=model,url=final,status='CANDIDATE',detail=im.format or '',**a))
            if max(a['object_width'],a['object_height'])>=750:break
        except Exception as e:rows.append(dict(model=model,url=u,status='FAILED',detail=str(e)[:180]))
fields=['model','url','status','detail','source_width','source_height','object_width','object_height','upscale','pixel_sha256','review_sha256','file']
writecsv(R/'audits/stage-15b-daikin-factory.csv',rows,fields)
for a in rows:
    if a.get('file') and max(a['object_width'],a['object_height'])>=500:
        f=O/a['file'];(R/'audits'/f'stage-15b-{a["pixel_sha256"][:10]}.b64.txt').write_text(base64.b64encode(f.read_bytes()).decode())
with zipfile.ZipFile('Climate347_stage15b_Daikin_factory.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
    for f in O.rglob('*'):
        if f.is_file():z.write(f,f.relative_to(O))
    z.write(R/'audits/stage-15b-daikin-factory.csv','manifest.csv')
with zipfile.ZipFile('Climate347_stage15b_Daikin_factory.zip') as z:assert z.testzip() is None
print(json.dumps(rows))
