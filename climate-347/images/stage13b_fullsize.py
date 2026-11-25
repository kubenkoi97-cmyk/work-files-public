import pathlib,zipfile,io,hashlib,json,base64,subprocess,csv,re
import requests,fitz
from PIL import Image
import numpy as np
R=pathlib.Path('climate-347/images');O=pathlib.Path('stage13b-out');O.mkdir(exist_ok=True)
tag='climate347-images-stage13-45524141720';name='Climate347_stage13_cabinet_evidence.zip'
subprocess.run(['gh','release','download',tag,'-p',name,'-D',str(O)],check=True)
p=O/name
assert hashlib.sha256(p.read_bytes()).hexdigest()=='17a2c2fe12c9a62df63b97551485c170af3e84c5e5daf56171abf3646864ee48'
def rgb(im):
    im=im.convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);return bg.convert('RGB')
def bbox(im):
    a=np.asarray(im);y,x=np.where((a<=242).any(axis=2));return (int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1))
def normalize(im):
    im=rgb(im);b=bbox(im);obj=im.crop(b);w,h=obj.size;f=750/max(w,h);obj=obj.resize((round(w*f),round(h*f)),Image.Resampling.LANCZOS)
    out=Image.new('RGB',(850,850),'white');out.paste(obj,((850-obj.width)//2,(850-obj.height)//2));return out,(w,h)
rows=[]
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    for label,ph in [('Bosch_MDCI_16-1','2cb6a4feeec5d75df5671eb3'),('Kentatsu_KVAG560CZAN3_angle1','48365e913c0cd010f6422a93'),('Kentatsu_KVAG560CZAN3_angle2','264c4be798c817c6f5529217'),('Kentatsu_KVAG560CZAN3_front','bbe7346679234f2b613776d6')]:
        im=Image.open(io.BytesIO(z.read('native/'+ph+'.png')));out,wh=normalize(im)
        f=O/(label+'.jpg');out.save(f,quality=96,subsampling=0)
        assert Image.open(f).size==(850,850)
        (R/'audits'/('stage-13b-'+label+'.b64.txt')).write_text(base64.b64encode(f.read_bytes()).decode())
        rows.append(dict(candidate=label,source_object=str(wh),upscale=750/max(wh),file=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),status='FULL_SIZE_REVIEW'))
# Read the actual catalogue page, then render only the designated product picture and report actual embedded image metadata.
url='https://www.thermotrade.ru/wp-content/uploads/2024/08/midea_vrf_2024-2025.pdf'
data=requests.get(url,timeout=(10,60)).content
assert hashlib.sha256(data).hexdigest()=='3e8e60b86bafaee04361a6f9f18a52461516eed2a0baf67c91900ec07461481b'
d=fitz.open(stream=data,filetype='pdf')
meta=[]
for idx,label in [(105,'ULTRA'),(109,'VC_MAX')]:
    pg=d[idx]
    # Capture the whole page with its labels for independent review.
    p=pg.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
    b=p.tobytes('jpeg',jpg_quality=90)
    (O/(label+'_page.jpg')).write_bytes(b)
    (R/'audits'/('stage-13b-'+label+'_page.b64.txt')).write_text(base64.b64encode(b).decode())
    for x in pg.get_image_info(xrefs=True):
        meta.append(dict(label=label,pdf_page=idx+1,xref=x['xref'],bbox=list(x['bbox']),width=x['width'],height=x['height']))
    # Page 110 has visually verified VC MAX wide front at x625..719,y445..569 on 893x1263 preview.
    # Extract that specific region at high DPI ONLY as a candidate; effective raster resolution is recorded separately.
    if label=='VC_MAX':
        r=fitz.Rect(pg.rect.width*620/893,pg.rect.height*439/1263,pg.rect.width*724/893,pg.rect.height*574/1263)
        pix=pg.get_pixmap(matrix=fitz.Matrix(9,9),clip=r,alpha=False)
        im=Image.open(io.BytesIO(pix.tobytes('png')))
        out,wh=normalize(im);f=O/'VC_MAX_wide_render_review.jpg';out.save(f,quality=96,subsampling=0)
        (R/'audits'/'stage-13b-VC_MAX_wide_render_review.b64.txt').write_text(base64.b64encode(f.read_bytes()).decode())
        rows.append(dict(candidate='VC_MAX_wide_render',source_object=str(wh),upscale=750/max(wh),file=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),status='RENDER_NOT_NATIVE_QUALITY_UNPROVEN'))
d.close()
(R/'audits'/'stage-13b-page-image-metadata.json').write_text(json.dumps(meta,indent=2))
with (R/'audits'/'stage-13b-fullsize.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with zipfile.ZipFile('Climate347_stage13b_fullsize_review.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
    for f in O.glob('*.jpg'):z.write(f,f.name)
    for n in ['stage-13b-page-image-metadata.json','stage-13b-fullsize.csv']:z.write(R/'audits'/n,n)
with zipfile.ZipFile('Climate347_stage13b_fullsize_review.zip') as z:assert z.testzip() is None
print(json.dumps(rows))
