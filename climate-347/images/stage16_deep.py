import pathlib,io,hashlib,json,csv,base64,re,zipfile,time,concurrent.futures
import requests,fitz
from bs4 import BeautifulSoup
from PIL import Image,ImageOps,ImageDraw
import numpy as np
from urllib.parse import urljoin
R=pathlib.Path('climate-347/images');O=pathlib.Path('stage16-out');O.mkdir(exist_ok=True)
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

from urllib.parse import urlparse
queue=[]
targets=list(csv.DictReader((R/'audits/stage-15-remaining-56.csv').open(encoding='utf-8'),delimiter=';'))
for t in targets:
    m=t['Exact model']; brand=t['Brand'];base=m.replace('/-40','');slug=base.lower();us=slug.replace('-','_').replace('(','_').replace(')','')
    if brand=='Kentatsu':
        queue.extend([(m,base,'https://iclim.ru/catalog/promyshlennye_konditsionery/multizonalnye_sistemy/naruzhnye_bloki_vrf/kentatsu_'+slug+'/'),(m,base,'https://pro-komfort.com/product/naruzhnyy-blok-multizonalnoy-sistemy-vrf-kentatsu-'+slug+'/')])
    elif brand=='Midea' and 'ULTRA' in m:
        queue.append((m,base,'https://mir-komforta.ru/catalog/konditsionirovanie/multizonalnye-vrf-sistemy/naruzhnye-bloki-vrf/midea-v8-ultra-v8i-ultra-'+norm(base)+'/'))
        queue.append((m,base,'https://iclim.ru/catalog/promyshlennye_konditsionery/multizonalnye_sistemy/naruzhnye_bloki_vrf/midea_'+us+'/'))
    elif brand=='Midea' and '/-40' in m:
        series='vc-max' if base.startswith('MVC') else 'v8si' if base.startswith('MV8Si') else 'v8s'
        queue.extend([(m,base,'https://frigus-systems.ru/product/vrf-sistemy/naruzhnye-bloki/midea-'+slug+'/'),(m,base,'https://coldcontrol.ru/catalog/detail/naruzhnyy-blok-vrf-midea-'+series+'-'+slug+'/'),(m,base,'https://www.klimat-master.ru/goods/midea-'+slug+'/'),(m,base,'https://iclim.ru/catalog/promyshlennye_konditsionery/multizonalnye_sistemy/naruzhnye_bloki_vrf/midea_'+us+'/')])
    elif brand=='Midea' and m.startswith('MIH'):
        queue.extend([(m,base,'https://iclim.ru/catalog/promyshlennye_konditsionery/multizonalnye_sistemy/vnutrennie_bloki_vrf/midea_'+slug+'/'),(m,base,'https://www.klimat-master.ru/goods/midea-'+slug+'/')])
    elif m=='IMBR-H440ANB':
        queue.append((m,base,'https://iclim.ru/catalog/promyshlennye_konditsionery/chillery/igc_imbr_h440anb/'))
    elif m=='IWF-Q1700CAQ4T22':
        queue.append((m,base,'https://www.klimat-master.ru/goods/igc-'+slug+'/'))
    elif brand=='Bosch':
        queue.extend([(m,base,'https://iclim.ru/catalog/promyshlennye_konditsionery/multizonalnye_sistemy/naruzhnye_bloki_vrf/bosch_'+us.replace(' ','_')+'/'),(m,base,'https://www.klimat-master.ru/goods/bosch-'+slug.replace(' ','-')+'/')])
# Per-host worker: stop after 429; no access-control bypass. Only exact product page candidates.
def work(t):
    m,base,u=t;out=[]
    try:
        data,final=get(u,12_000_000);s=BeautifulSoup(data,'html.parser')
        h=' '.join(x.get_text(' ',strip=True) for x in s.find_all('h1'))
        if norm(base) not in norm(h):raise ValueError('exact/base H1 missing: '+h[:120])
        tx=s.get_text(' ',strip=True)
        winter=bool(re.search(r'(?:низкотемпературн\w+|зимн\w+)\s+комплект',tx,re.I))
        status='EXACT_CARD' if norm(m) in norm(h) else 'BASE_CARD_WINTER_OPTION' if winter else 'BASE_CARD_ONLY'
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
        if og and og.get('content'):urls.append(og['content'])
        urls=list(dict.fromkeys(urljoin(final,v) for v in urls if v and not any(x in v.lower() for x in ['loading.svg','placeholder','no_photo','no-photo','logo'])))[:7]
        if not urls:raise ValueError('no labelled gallery')
        for v in urls:
            try:
                d,f=get(v,20_000_000,final);im=Image.open(io.BytesIO(d));im.load()
                out.append(dict(model=m,page=final,url=f,status='CANDIDATE',detail=status,**save(im)))
            except Exception as e:out.append(dict(model=m,page=final,url=v,status='FAILED',detail=str(e)[:180]))
    except Exception as e:out.append(dict(model=m,page=u,url='',status='FAILED',detail=str(e)[:180]))
    return out
by={}
for t in queue:by.setdefault(urlparse(t[2]).netloc,[]).append(t)
def runhost(q):
    rs=[]
    for t in q:
        a=work(t);rs.extend(a)
        if any('429' in x.get('detail','') for x in a):break
        time.sleep(.35)
    return rs
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:web=[r for a in ex.map(runhost,by.values()) for r in a]
pdfrows=[];logs=[]
sources=[('Midea_V8S_2025','https://www.midea.com/content/dam/midea-aem/id/PD-Midea-V8S-VRF-Catalogue-2025-06-30-V6.pdf'),('Midea_V8_all','https://www.savame.com/wp-content/uploads/2025/04/Midea-VRF-V8-All-Catalogue-EN.pdf'),('Midea_Daichi_2026','https://www.c-o-k.ru/library/catalogs/daichi/38190/140641.pdf'),('Midea_V8S_RU','https://onokom.ru/dok/midea/2024/catalog/2024-catalog-v8s.pdf')]
def pdfwork(item):
    name,u=item;rs=[];log={}
    try:
        d,final=get(u,90_000_000);doc=fitz.open(stream=d,filetype='pdf');sha=hashlib.sha256(d).hexdigest()
        sel=set(range(min(8,len(doc))))
        for i,p in enumerate(doc):
            tx=p.get_text()
            if re.search(r'MV8S[i]?\s*[-_]?\s*(450|500|560|615|670)|MVC\s*[-_]?\s*M(615|670|730|785|850)|MIH\s*[-_]?\s*(252|280|335|450|560)\s*F[LS]HN',tx,re.I):sel.update(j for j in [i-1,i,i+1] if 0<=j<len(doc))
        sel=sorted(sel)[:50];log=dict(name=name,url=final,status='PDF_ACQUIRED',pages=len(doc),selected=len(sel),sha256=sha)
        for i in sel:
            p=doc[i];founds=0
            for z in p.get_image_info(xrefs=True):
                x=z['xref'];w=z['width'];h=z['height']
                if not x or max(w,h)<400 or min(w,h)<160:continue
                try:
                    pix=fitz.Pixmap(doc,x)
                    masks=[v[1] for v in p.get_images(full=True) if v[0]==x and v[1]]
                    if masks:
                        try:pix=fitz.Pixmap(pix,fitz.Pixmap(doc,masks[0]))
                        except Exception:pass
                    if pix.colorspace is None:continue
                    if pix.colorspace.n>3:pix=fitz.Pixmap(fitz.csRGB,pix)
                    a=save(Image.open(io.BytesIO(pix.tobytes('png'))))
                    rs.append(dict(model=name,page=i+1,url=final,status='PDF_CANDIDATE',detail=f'xref {x}; rect {z["bbox"]}',**a));founds+=1
                except Exception:pass
            if founds:
                f=O/'pages'/f'{name}-p{i+1:03}.jpg';f.parent.mkdir(exist_ok=True)
                pix=p.get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False);f.write_bytes(pix.tobytes('jpeg',jpg_quality=85))
        doc.close()
    except Exception as e:log=dict(name=name,url=u,status='FAILED',detail=str(e)[:200])
    return rs,log
# Sequential PDFs avoid excessive memory.
for item in sources:
    rs,log=pdfwork(item);pdfrows.extend(rs);logs.append(log)
fields=['model','page','url','status','detail','source_width','source_height','object_width','object_height','upscale','pixel_sha256','review_sha256','file']
writecsv(R/'audits/stage-16-web-results.csv',web,fields);writecsv(R/'audits/stage-16-pdf-results.csv',pdfrows,fields)
(R/'audits/stage-16-pdf-log.json').write_text(json.dumps(logs,indent=2))
writecsv(R/'audits/stage-16-queue.csv',[dict(model=m,base=base,url=u) for m,base,u in queue],['model','base','url'])
unique={}
for a in web+pdfrows:
    if a.get('file'):unique.setdefault(a['pixel_sha256'],a)
u=list(unique.values())
for k in range(0,len(u),16):
    group=u[k:k+16];sheet=Image.new('RGB',(1120,((len(group)+3)//4)*245),'white');draw=ImageDraw.Draw(sheet)
    for i,a in enumerate(group):
        x=i%4*280;y=i//4*245;im=ImageOps.contain(Image.open(O/a['file']),(270,200));sheet.paste(im,(x+(280-im.width)//2,y))
        draw.text((x+3,y+202),f"{a['model']} {str(a['page'])[:8] if a['status']=='PDF_CANDIDATE' else ''}"[:38],fill='black')
        draw.text((x+3,y+217),f"{a['object_width']}x{a['object_height']} {a['pixel_sha256'][:10]}",fill='black')
    f=O/f'contact-{k//16+1:02}.jpg';sheet.save(f,quality=82)
    if k<256:(R/'audits'/f'stage-16-contact-{k//16+1:02}.b64.txt').write_text(base64.b64encode(f.read_bytes()).decode())
for a in u:
    if a['status']!='PDF_CANDIDATE' and max(a['object_width'],a['object_height'])>=500:
        f=O/a['file'];(R/'audits'/f'stage-16-full-{a["pixel_sha256"][:10]}.b64.txt').write_text(base64.b64encode(f.read_bytes()).decode())
summary=dict(target_models=len(targets),queued_pages=len(queue),attempted_pages=len({(r['model'],r['page']) for r in web}),web_models_with_images=len({r['model'] for r in web if r.get('file')}),web_files=sum(bool(r.get('file')) for r in web),pdf_occurrences=len(pdfrows),pdf_unique=len({r['pixel_sha256'] for r in pdfrows}),unique_all=len(u),sheets=(len(u)+15)//16,approved=0)
(R/'audits/stage-16-summary.json').write_text(json.dumps(summary,indent=2))
with zipfile.ZipFile('Climate347_stage16_candidates.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
    for f in O.rglob('*'):
        if f.is_file():z.write(f,f.relative_to(O))
    for f in R.glob('audits/stage-16-*'):
        if not f.name.endswith('.b64.txt'):z.write(f,f.name)
with zipfile.ZipFile('Climate347_stage16_candidates.zip') as z:assert z.testzip() is None
print(json.dumps(summary))
