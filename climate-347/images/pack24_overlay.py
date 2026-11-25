import csv, pathlib, zipfile, hashlib, io
from PIL import Image
root=pathlib.Path('climate-347/images')
rows=list(csv.DictReader((root/'audits/stage-21-approved-overlay.csv').open(encoding='utf-8'),delimiter=';'))
assert len(rows)==35
with zipfile.ZipFile('Climate347_approved_overlay_35.zip','w',zipfile.ZIP_DEFLATED) as z:
    for r in rows:
        b=(root/r['Approved JPG repository relative path']).read_bytes()
        assert hashlib.sha256(b).hexdigest()==r['SHA256']
        im=Image.open(io.BytesIO(b)); im.load(); assert im.size==(850,850) and im.format=='JPEG'
        z.writestr(r['Base archive target path'],b)
with zipfile.ZipFile('Climate347_approved_overlay_35.zip') as z:
    assert len(z.namelist())==35 and z.testzip() is None
print(hashlib.sha256(pathlib.Path('Climate347_approved_overlay_35.zip').read_bytes()).hexdigest())
