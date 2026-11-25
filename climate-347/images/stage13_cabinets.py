import pathlib,io,hashlib,csv,json,re,zipfile,base64,concurrent.futures
import requests,fitz
from bs4 import BeautifulSoup
from PIL import Image,ImageOps,ImageDraw
import numpy as np
R=pathlib.Path('climate-347/images'); O=pathlib.Path('stage13-out');O.mkdir(exist_ok=True)
sources=[('Midea_catalog','https://www.thermotrade.ru/wp-content/uploads/2024/08/midea_vrf_2024-2025.pdf',[108,109,110,111,112,113,114,115,116]),('Bosch_catalog','https://www.bosch-homecomfort.com/ke/media/country_pool/pdfs/catalogues/vrf_2021_en.pdf',[]),('Kentatsu_catalog','https://www.c-o-k.ru/library/catalogs/kentatsu/37986/140011.pdf',[80,81,82,83,84,85])]
def get(url,limit=100_000_000,ref=None):
    with requests.get(url,headers={'User-Agent':'Mozilla/5.0 (compatible; product research)','Referer':ref or url},timeout=(10,35),stream=True) as r:
        r.raise_for_status();d=bytearray()
        for b in r.iter_content(65536):
            d.extend(b)
            if len(d)>limit:raise ValueError('size cap')
        return bytes(d),r.url
def writecsv(path,rs,fields):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rs)
def saveim(im,name):
    im=im.convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);im=bg.convert('RGB')
    arr=np.asarray(im);ys,xs=np.where((arr<=242).any(axis=2))
    if not len(xs):return None
    bw,bh=int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)
    h=hashlib.sha256(f'{im.width}x{im.height}:'.encode()+im.tobytes()).hexdigest()
    f=O/'native'/(h[:24]+'.png');f.parent.mkdir(exist_ok=True)
    if not f.exists():im.save(f)
    return dict(file=str(f.relative_to(O)),pixel_sha256=h,width=im.width,height=im.height,object_width=bw,object_height=bh)
rows=[];logs=[];pages=[]
for name,url,nums in sources:
    try:
        data,final=get(url);d=fitz.open(stream=data,filetype='pdf');sha=hashlib.sha256(data).hexdigest()
        # identify all relevant product overview pages rather than exact table alone
        sel=set(i-1 for i in nums if 1<=i<=len(d))
        for i,p in enumerate(d):
            t=p.get_text()
            if name=='Midea_catalog' and (('ULTRA' in t and ('78,5-117' in t or '78,5–117' in t or '78,5—117' in t or '78,5 - 117' in t)) or ('VC MAX' in t and ('61,5-85' in t or '61,5–85' in t))):sel.add(i)
            if name=='Bosch_catalog' and ('MDCI' in t and re.search(r'MDCI\s*(40|45|26|22|16)[-– ]',t)):sel.update(j for j in [i-1,i,i+1] if 0<=j<len(d))
            if name=='Kentatsu_catalog' and ('DX PRO A' in t and ('KVAG' in t or 'KVAH' in t)):sel.update(j for j in [i-1,i,i+1] if 0<=j<len(d))
        sel=sorted(sel)[:35]
        logs.append(dict(source=name,url=final,status='PDF_ACQUIRED',detail=f'{len(d)} pages; selected {len(sel)}; SHA256 {sha}'))
        for i in sel:
            pg=d[i]; key=f'{name}-p{i+1:03d}'
            pm=pg.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
            im=Image.open(io.BytesIO(pm.tobytes('png'))).convert('RGB');im.thumbnail((1400,1600))
            f=O/'pages'/(key+'.jpg');f.parent.mkdir(exist_ok=True);im.save(f,quality=90)
            pages.append(dict(source=name,page=i+1,file=str(f.relative_to(O)),text=pg.get_text()[:800].replace('\n',' ')))
            # get_image_info includes inline and clipped objects; xref extraction preserves native pixels
            for z in pg.get_image_info(xrefs=True):
                x=z['xref'];w=z['width'];h=z['height'];rect=fitz.Rect(z['bbox'])
                if not x or min(w,h)<65 or max(w,h)<150 or rect.is_empty:continue
                try:
                    pix=fitz.Pixmap(d,x)
                    masks=[j[1] for j in pg.get_images(full=True) if j[0]==x and j[1]]
                    if masks:
                        try:pix=fitz.Pixmap(pix,fitz.Pixmap(d,masks[0]))
                        except:pass
                    if pix.colorspace is None:continue
                    if pix.colorspace.n>3:pix=fitz.Pixmap(fitz.csRGB,pix)
                    a=saveim(Image.open(io.BytesIO(pix.tobytes('png'))),key)
                    if a:rows.append(dict(source=name,page=i+1,xref=x,rect=str(rect),pdf_sha256=sha,**a))
                except Exception:pass
        d.close()
    except Exception as e:logs.append(dict(source=name,url=url,status='FAILED',detail=str(e)[:250]))
# Direct exact-card originals for Bosch and Midea FSHN/FLHN. Reuse actual labelled image links, avoid multiple identical listing requests.
queue=[]
for m in ['MDCI 16-1','MDCI 22-3','MDCI 26-3','MDCI 40-3','MDCI 45-3']:
    queue.append((m,'https://vsekondicioneri.ru/product/naruzhnyy-blok-vrf-sistemy-bosch-'+m.lower().replace(' ','-')+'/'))
queue.append(('MDCI 16-1','https://www.bosch-homecomfort.com/web-etk/de/bosch/de/de/product/7739835420'))
for n in [252,280,335,450,560]:
    for suf in ['FLHN','FSHN']:
        m=f'MIH{n}{suf}18';queue.append((m,'https://simferopol.vsekondicioneri.ru/product/midea-'+m.lower()+'/'))
queue.append(('MV8i-1010WV2GN1(ULTRA)','https://tdkomfort.ru/shop/product/naruzhnyy_blok_vrf_sistemy_midea_mv8i_1010wv2gn1_ultra/'))
queue.append(('KVAG560CZAN3','https://pro-komfort.com/product/naruzhnyy-blok-multizonalnoy-sistemy-vrf-kentatsu-kvag560czan3/'))
queue.append(('IMBR-H440ANB','https://igc-aircon.com/product/modulnye_chillery_30_kw_2080_kw/'))
from urllib.parse import urljoin
web=[]
def card(item):
    m,url=item;out=[]
    try:
        d,final=get(url,10_000_000);s=BeautifulSoup(d,'html.parser')
        h=' '.join(x.get_text(' ',strip=True) for x in s.find_all('h1'))
        exact=lambda t:re.search(r'(?<![A-Za-z0-9])'+re.escape(m)+r'(?![A-Za-z0-9])',t,re.I) is not None
        verified=exact(h) or (m=='MDCI 16-1' and exact(s.title.get_text(' ',strip=True) if s.title else ''))
        urls=[]
        if verified:
            og=s.find('meta',property='og:image')
            if og and og.get('content'):urls.append(og['content'])
        for i in s.find_all('img'):
            if exact(i.get('alt','')+' '+i.get('title','')) or (verified and 'bosch-homecomfort.com' in final and i.get('alt')=='Climate 5000 VRF'):
                for k in ['data-src','data-original','src']:
                    if i.get(k):urls.append(i[k])
                a=i.find_parent('a',href=True)
                if a and re.search(r'\.(jpg|jpeg|png|webp)(\?|$)',a['href'],re.I):urls.append(a['href'])
        if m=='MDCI 26-3':urls.append('https://vsekondicioneri.ru/wa-data/public/shop/products/70/06/30670/images/55384/55384.659@2x.jpg')
        urls=list(dict.fromkeys(urljoin(final,u) for u in urls if u and not u.startswith('data:')))[:8]
        if not urls:raise ValueError('No exact H1/labelled image')
        for u in urls:
            try:
                b,f=get(u,20_000_000,final);im=Image.open(io.BytesIO(b));im.load()
                if max(im.size)<250:continue
                rec=saveim(im,m)
                if rec:out.append(dict(model=m,page=final,url=f,status='CANDIDATE',detail='exact page' if verified else 'exact image label only',**rec))
            except Exception as e:out.append(dict(model=m,page=final,url=u,status='FAILED',detail=str(e)[:200]))
        if not out:raise ValueError('no qualifying raster')
    except Exception as e:out.append(dict(model=m,page=url,url='',status='FAILED',detail=str(e)[:200]))
    return out
# Sequential by host, modest request rate; do not retry HTTP429.
import time
for it in queue:
    web.extend(card(it));time.sleep(0.4)
fields=['file','pixel_sha256','width','height','object_width','object_height']
writecsv(R/'audits/stage-13-pdf-images.csv',rows,['source','page','xref','rect','pdf_sha256']+fields)
writecsv(R/'audits/stage-13-web-images.csv',web,['model','page','url','status','detail']+fields)
writecsv(R/'audits/stage-13-source-log.csv',logs,['source','url','status','detail'])
writecsv(O/'page-index.csv',pages,['source','page','file','text'])
# Evidence sheets for relevant page overview and all unique images.
for p in pages:
    if p['source']=='Midea_catalog' and p['page'] in range(108,116):
        raw=(O/p['file']).read_bytes()
        (R/'audits'/('stage-13-'+pathlib.Path(p['file']).stem+'.b64.txt')).write_text(base64.b64encode(raw).decode())
unique={}
for a in rows+[r for r in web if r.get('file')]:unique.setdefault(a['pixel_sha256'],a)
u=list(unique.values())
for k in range(0,len(u),16):
    group=u[k:k+16];sheet=Image.new('RGB',(1120,((len(group)+3)//4)*220),'white');draw=ImageDraw.Draw(sheet)
    for i,a in enumerate(group):
        x=i%4*280;y=i//4*220;im=ImageOps.contain(Image.open(O/a['file']),(270,175));sheet.paste(im,(x+(280-im.width)//2,y))
        draw.text((x+3,y+175),f"{a.get('source',a.get('model'))} p{a.get('page','') if 'source' in a else ''}",fill='black')
        draw.text((x+3,y+190),f"{a['object_width']}x{a['object_height']} {a['pixel_sha256'][:10]}",fill='black')
    f=O/f'contact-{k//16+1:02}.jpg';sheet.save(f,quality=82)
    if k<160:(R/'audits'/f'stage-13-contact-{k//16+1:02}.b64.txt').write_text(base64.b64encode(f.read_bytes()).decode())
summary=dict(pdf_pages=len(pages),pdf_occurrences=len(rows),pdf_unique=len({r['pixel_sha256'] for r in rows}),web_models=len({r['model'] for r in web if r.get('file')}),web_files=sum(bool(r.get('file')) for r in web),unique_all=len(u),sheets=(len(u)+15)//16,approved=0)
(R/'audits/stage-13-summary.json').write_text(json.dumps(summary,indent=2))
with zipfile.ZipFile('Climate347_stage13_cabinet_evidence.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
    for f in O.rglob('*'):
        if f.is_file():z.write(f,f.relative_to(O))
    for f in R.glob('audits/stage-13-*.csv'):z.write(f,f.name)
    z.write(R/'audits/stage-13-summary.json','summary.json')
with zipfile.ZipFile('Climate347_stage13_cabinet_evidence.zip') as z:assert z.testzip() is None
print(json.dumps(summary))
