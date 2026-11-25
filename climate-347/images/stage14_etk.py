import pathlib,io,hashlib,json,csv,base64,re,zipfile,time
import requests
from bs4 import BeautifulSoup
from PIL import Image,ImageOps,ImageDraw
import numpy as np
from urllib.parse import urljoin
R=pathlib.Path('climate-347/images'); O=pathlib.Path('stage14-out');O.mkdir(exist_ok=True)
ids={'MDCI 8-1':'7739835416','MDCI 10-1':'7739835417','MDCI 12-1':'7739835418','MDCI 14-1':'7739835419','MDCI 16-1':'7739835420','MDCI 12-3':'7739835421','MDCI 14-3':'7739835422','MDCI 16-3':'7739835423','MDCI 18-3':'7739835424','MDCI 20-3':'7739835425','MDCI 22-3':'7739835426','MDCI 26-3':'7739835427','MDCI 40-3':'8733500853','MDCI 45-3':'8733500854'}
queue=[(m,'https://www.bosch-homecomfort.com/web-etk/de/bosch/de/de/product/'+ids[m]) for m in ['MDCI 22-3','MDCI 26-3','MDCI 40-3','MDCI 45-3','MDCI 20-3','MDCI 18-3']]
queue += [('IMBR-H440ANB','https://igc.com.ru/catalog/chillery/'),('MV8i-1010WV2GN1(ULTRA)','https://www.effect-nn.ru/cond_category_250_page-31.htm')]
def get(u,ref=None):
    with requests.get(u,headers={'User-Agent':'Mozilla/5.0 (compatible; product research)','Referer':ref or u},timeout=(8,18),stream=True) as r:
        r.raise_for_status();b=bytearray()
        for chunk in r.iter_content(65536):
            b.extend(chunk)
            if len(b)>20_000_000:raise ValueError('size limit')
        return bytes(b),r.url
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
def exact(s,m):return norm(m) in norm(s)
def save(m,u,page,mode):
    d,final=get(u,page);im=Image.open(io.BytesIO(d));im.load();im=im.convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);im=bg.convert('RGB')
    a=np.asarray(im);y,x=np.where((a<=242).any(axis=2))
    if not len(x):raise ValueError('blank')
    crop=im.crop((int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)));w,h=crop.size
    if max(w,h)<250:raise ValueError('thumbnail')
    ph=hashlib.sha256(f'{im.width}x{im.height}:'.encode()+im.tobytes()).hexdigest()
    f=O/'native'/(ph[:24]+'.png');f.parent.mkdir(exist_ok=True);im.save(f)
    fac=750/max(w,h);crop=crop.resize((round(w*fac),round(h*fac)),Image.Resampling.LANCZOS);out=Image.new('RGB',(850,850),'white');out.paste(crop,((850-crop.width)//2,(850-crop.height)//2))
    jf=O/'review'/(norm(m)+'-'+ph[:10]+'.jpg');jf.parent.mkdir(exist_ok=True);out.save(jf,quality=96,subsampling=0)
    return dict(model=m,page=page,url=final,status='CANDIDATE',detail=mode,source_width=im.width,source_height=im.height,object_width=w,object_height=h,upscale=round(fac,4),pixel_sha256=ph,review_sha256=hashlib.sha256(jf.read_bytes()).hexdigest(),file=str(jf.relative_to(O)))
rows=[];sources=[]
for m,url in queue:
    try:
        d,final=get(url);s=BeautifulSoup(d,'html.parser')
        title=' '.join(x.get_text(' ',strip=True) for x in s.find_all(['title','h1']))
        # ETK pages have exact model in title and/or main product heading.
        headings=' '.join(x.get_text(' ',strip=True) for x in s.find_all(['h1','h2','h3']))
        verified=exact(title+' '+headings,m)
        urls=[]
        for i in s.find_all('img'):
            alt=i.get('alt','')+' '+i.get('title','')
            src=i.get('data-src') or i.get('src') or ''
            if exact(alt,m) or (m.startswith('MDCI') and verified and ('documents/img' in src) and ('climate 5000' in alt.lower() or exact(alt,m))):
                urls.append(urljoin(final,src))
        if verified:
            og=s.find('meta',property='og:image')
            if og and og.get('content'):urls.append(urljoin(final,og['content']))
        # record all image attributes for review, but never assign unrelated image automatically
        sources.append(dict(model=m,page=final,title=title,verified=verified,images=[dict(alt=i.get('alt',''),src=i.get('src','')) for i in s.find_all('img')][:70]))
        if not urls:raise ValueError('no exact labelled image')
        for u in list(dict.fromkeys(urls))[:5]:
            try:rows.append(save(m,u,final,'EXACT_ETK_PAGE' if verified and m.startswith('MDCI') else 'EXACT_LABEL_REVIEW'))
            except Exception as e:rows.append(dict(model=m,page=final,url=u,status='FAILED',detail=str(e)[:200]))
    except Exception as e:rows.append(dict(model=m,page=url,url='',status='FAILED',detail=str(e)[:200]))
    time.sleep(.4)
fields=['model','page','url','status','detail','source_width','source_height','object_width','object_height','upscale','pixel_sha256','review_sha256','file']
with (R/'audits/stage-14-source-results.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
(R/'audits/stage-14-page-evidence.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
ok=[r for r in rows if r.get('file')]
for a in ok:
    f=O/a['file'];(R/'audits'/('stage-14-'+f.stem+'.b64.txt')).write_text(base64.b64encode(f.read_bytes()).decode())
summary=dict(targets=len(queue),candidate_models=len({r['model'] for r in ok}),files=len(ok),unique=len({r['pixel_sha256'] for r in ok}),approved=0)
(R/'audits/stage-14-summary.json').write_text(json.dumps(summary,indent=2))
with zipfile.ZipFile('Climate347_stage14_ETK_candidates.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
    for f in O.rglob('*'):
        if f.is_file():z.write(f,f.relative_to(O))
    for f in R.glob('audits/stage-14-*'):
        if not f.name.endswith('.b64.txt'):z.write(f,f.name)
with zipfile.ZipFile('Climate347_stage14_ETK_candidates.zip') as z:assert z.testzip() is None
print(json.dumps(summary))
