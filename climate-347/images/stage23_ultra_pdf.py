import pathlib,io,hashlib,json,csv,base64,re,zipfile,time,concurrent.futures
import requests,fitz
from bs4 import BeautifulSoup
from PIL import Image,ImageOps,ImageDraw
import numpy as np
from urllib.parse import urljoin
R=pathlib.Path('climate-347/images');O=pathlib.Path('stage23-out');O.mkdir(exist_ok=True)
def get(u,limit=65_000_000,ref=None):
    with requests.get(u,headers={'User-Agent':'Mozilla/5.0 (compatible; product research)','Referer':ref or u},timeout=(4,6),stream=True) as r:
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
    if max(w,h)<120 or min(w,h)<60:raise ValueError('thumbnail')
    ph=hashlib.sha256(f'{im.width}x{im.height}:'.encode()+im.tobytes()).hexdigest()
    f=O/'native'/(ph[:24]+'.png');f.parent.mkdir(exist_ok=True)
    if not f.exists():im.save(f)
    fac=750/max(w,h);crop=crop.resize((round(w*fac),round(h*fac)),Image.Resampling.LANCZOS);out=Image.new('RGB',(850,850),'white');out.paste(crop,((850-crop.width)//2,(850-crop.height)//2))
    jf=O/'review'/(ph[:24]+'.jpg');jf.parent.mkdir(exist_ok=True);out.save(jf,quality=96,subsampling=0)
    return dict(source_width=im.width,source_height=im.height,object_width=w,object_height=h,upscale=round(fac,4),pixel_sha256=ph,review_sha256=hashlib.sha256(jf.read_bytes()).hexdigest(),file=str(jf.relative_to(O)))
def writecsv(path,rows,fields):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)


from urllib.parse import urlparse
queue=[]
direct=[]
def originals():return []
# All URLs are template probes derived from actual indexed examples; verify H1 before selecting.
def work(t):
    m,base,u=t;out=[]
    try:
        data,final=get(u,12_000_000);s=BeautifulSoup(data,'html.parser')
        h=' '.join(x.get_text(' ',strip=True) for x in s.find_all('h1'))
        if norm(base) not in norm(h) and not (m.startswith(('IWF','IMBR')) and any(norm(base) in norm(i.get('alt','')+' '+i.get('title','')) for i in s.find_all('img'))):raise ValueError('exact/base H1 or labelled listing raster missing: '+h[:120])
        tx=s.get_text(' ',strip=True)
        winter=bool(re.search(r'(?:низкотемпературн\w+|зимн\w+)\s+комплект',tx,re.I))
        status='ALIAS_REQUIRES_CROSS_REFERENCE' if base!=m else 'EXACT_CARD' if norm(m) in norm(h) else 'BASE_CARD_WINTER_OPTION' if winter else 'BASE_CARD_ONLY'
        urls=[]
        for i in s.find_all('img'):
            if norm(base) not in norm(i.get('alt','')+' '+i.get('title','')):continue
            for k in ['data-src','data-original','data-lazy','data-lazy-src','src']:
                a=i.get(k,'')
                if a and not a.startswith('data:'):urls.append(a)
            for k in ['srcset','data-srcset']:
                for a in i.get(k,'').split(','):
                    if a.strip():urls.append(a.strip().split()[0])
            for a in list(i.parents)[:3]:
                if a.name=='a' and a.get('href') and re.search(r'\.(jpg|jpeg|webp|png)(\?|$)',a['href'],re.I):urls.append(a['href'])
                for k in ['data-src','data-zoom-image','data-large','data-full']:
                    if a.get(k):urls.append(a[k])
        og=s.find('meta',property='og:image')
        if og and og.get('content') and norm(base) in norm(h):urls.append(og['content'])
        urls=list(dict.fromkeys(urljoin(final,re.sub(r'^https?://[^/]+(?=https?://)','',v)) for v in urls if v and not any(x in v.lower() for x in ['loading.svg','placeholder','no_photo','no-photo','logo'])))[:7]
        if not urls:raise ValueError('no labelled gallery')
        for v in urls:
            try:
                d,f=get(v,20_000_000,final);im=Image.open(io.BytesIO(d));im.load()
                out.append(dict(model=m,page=final,url=f,status='CANDIDATE',detail=status,**save(im)))
            except Exception as e:out.append(dict(model=m,page=final,url=v,status='FAILED',detail=str(e)[:180]))
    except Exception as e:out.append(dict(model=m,page=u,url='',status='FAILED',detail=str(e)[:180]))
    return out

# Exact model tokens must be in H1; original script captures only labelled gallery images.
by={}
for t in queue:by.setdefault(urlparse(t[2]).netloc,[]).append(t)
def runhost(q):
    rs=[]
    for t in q:
        a=work(t);rs.extend(a)
        if any('429' in x.get('detail','') for x in a):break
        time.sleep(.35)
    return rs
def evidence():
    log=[];rows=[]
    docs=[('Midea ULTRA thermotrade','https://www.thermotrade.ru/wp-content/uploads/2024/08/midea_vrf_2024-2025.pdf',[108,109,110]),('Midea ULTRA Daichi','https://daichi.business/upload/iblock/32c/M2_2024_DM24_02.01.02_Small_260824.pdf',[108,109,110]),('Midea ULTRA COK','https://www.c-o-k.ru/library/catalogs/midea/37988/140017.pdf',None)]
    for label,url,pages in docs:
        try:
            d,final=get(url,100_000_000);doc=fitz.open(stream=d,filetype='pdf')
            selected=pages if pages is not None else [i for i,p in enumerate(doc) if re.search(r'ULTRA',p.get_text(),re.I) and re.search(r'78[,.]5|785',p.get_text(),re.I)][:10]
            log.append(dict(label=label,url=final,status='PDF_ACQUIRED',pages=len(doc),selected=[i+1 for i in selected],sha256=hashlib.sha256(d).hexdigest()))
            for i in selected:
                p=doc[i]
                preview=p.get_pixmap(matrix=fitz.Matrix(.85,.85),alpha=False).tobytes('jpeg',jpg_quality=80)
                (R/'audits'/f'stage-23-page-{norm(label)}-{i+1}.b64.txt').write_text(base64.b64encode(preview).decode())
                log.append(dict(label=label,page=i+1,text=p.get_text()[:9000]))
                log.append(dict(label=label,page=i+1,images=[dict(xref=z[0],smask=z[1],width=z[2],height=z[3],rects=[list(r) for r in p.get_image_rects(z[0])]) for z in p.get_images(full=True)]))
                for x in p.get_images(full=True):
                    try:
                        if max(x[2],x[3])<120 or min(x[2],x[3])<60:continue
                        pix=fitz.Pixmap(doc,x[0])
                        if pix.colorspace and pix.colorspace.n>3:pix=fitz.Pixmap(fitz.csRGB,pix)
                        if x[1]:
                            pix=fitz.Pixmap(pix,fitz.Pixmap(doc,x[1]))
                        im=Image.open(io.BytesIO(pix.tobytes('png')));im.load()
                        a=dict(model=label,page=f'{final}#page={i+1}',url=final,status='CANDIDATE',detail=f'PDF_NATIVE_XREF_{x[0]}_REVIEW_REQUIRED',**save(im));rows.append(a)
                    except Exception as e:log.append(dict(label=label,page=i+1,xref=x[0],status='RASTER_ERROR',detail=str(e)[:180]))
            doc.close()
        except Exception as e:log.append(dict(label=label,url=url,status='FAILED',detail=str(e)[:200]))
    (R/'audits/stage-23-evidence.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
    return rows
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    ev=ex.submit(evidence)
    orig=ex.submit(originals)
    web=[r for a in ex.map(runhost,by.values()) for r in a]
    web.extend(ev.result())
    web.extend(orig.result())
fields=['model','page','url','status','detail','source_width','source_height','object_width','object_height','upscale','pixel_sha256','review_sha256','file']
writecsv(R/'audits/stage-23-web-results.csv',web,fields)
unique={}
for a in web:
    if a.get('file'):unique.setdefault(a['pixel_sha256'],a)
u=list(unique.values())
for k in range(0,len(u),16):
    group=u[k:k+16];sheet=Image.new('RGB',(1120,((len(group)+3)//4)*245),'white');draw=ImageDraw.Draw(sheet)
    for i,a in enumerate(group):
        x=i%4*280;y=i//4*245;im=ImageOps.contain(Image.open(O/a['file']),(270,200));sheet.paste(im,(x+(280-im.width)//2,y))
        draw.text((x+3,y+202),a['model'][:38],fill='black')
        draw.text((x+3,y+217),f"{a['object_width']}x{a['object_height']} {a['pixel_sha256'][:10]}",fill='black')
    f=O/f'contact-{k//16+1:02}.jpg';sheet.save(f,quality=82)
    (R/'audits'/f'stage-23-contact-{k//16+1:02}.b64.txt').write_text(base64.b64encode(f.read_bytes()).decode())
for a in u:
    if max(a['object_width'],a['object_height'])>=120 and (a['model'].startswith('Bosch MDCI') or a['detail'].startswith(('EXACT_CARD','SAVED_HTML','PDF_','ALIAS_')) or a['model'].startswith(('IWF','IMBR'))):
        f=O/a['file'];(R/'audits'/f'stage-23-full-{a["pixel_sha256"][:10]}.b64.txt').write_text(base64.b64encode(f.read_bytes()).decode())
summary=dict(queued_pages=len(queue)+len(direct),attempted_pages=len({(r['model'],r['page']) for r in web}),web_models_with_images=len({r['model'] for r in web if r.get('file') and not r['detail'].startswith('PDF_')}),web_files=sum(bool(r.get('file')) for r in web),unique_all=len(u),sheets=(len(u)+15)//16,approved=0)
(R/'audits/stage-23-summary.json').write_text(json.dumps(summary,indent=2))
with zipfile.ZipFile('Climate347_stage23_candidates.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
    for f in O.rglob('*'):
        if f.is_file():z.write(f,f.relative_to(O))
    for f in R.glob('audits/stage-23-*'):
        if not f.name.endswith('.b64.txt'):z.write(f,f.name)
with zipfile.ZipFile('Climate347_stage23_candidates.zip') as z:assert z.testzip() is None
print(json.dumps(summary))
