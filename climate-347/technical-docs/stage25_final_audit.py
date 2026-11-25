import csv, hashlib, io, json, pathlib, re, subprocess, zipfile, collections
root=pathlib.Path('/tmp/climate347final');root.mkdir(exist_ok=True)
tag='climate-347-pdf-stage17-45511680707'
subprocess.run(['gh','release','download',tag,'--pattern','Climate_347_stage17_partial_Selectel.zip','--dir',str(root)],check=True)
zpath=root/'Climate_347_stage17_partial_Selectel.zip'
assert hashlib.file_digest(zpath.open('rb'),'sha256').hexdigest()=='bc853ccdeff05f353f1171be34a5872bbe5346b555a5c420b71280fdc1a7cd68'
def rows(z,name):return list(csv.DictReader(io.StringIO(z.read('REPORTS/'+name).decode('utf-8-sig'))))
with zipfile.ZipFile(zpath) as z:
    assert z.testzip() is None
    m=rows(z,'partial_selectel_manifest.csv');c=rows(z,'coverage_347.csv')
    allowed={'catalog','manual','combined_manual_passport','installation','technical','wiring','passport','service','engineering','drawing'}
    bad=re.compile(r'certificate|declaration|сертификат|деклараци|warranty|гарантийн',re.I)
    assert len(m)==407 and len(c)==347
    groups=collections.defaultdict(list)
    files={}
    for r in m:
        assert r['document_kind'] in allowed and not bad.search(r['filename']+' '+r['label_ru'])
        p=r['archive_path']
        assert p.startswith('UPLOAD_TO_SELECTEL/') and r['full_url']=='https://docs.proclimate5.ru/'+p.split('/',1)[1]
        if p not in files:files[p]=hashlib.sha256(z.read(p)).hexdigest()
        assert files[p]==r['sha256']
        groups[(r['brand'],r['model'])].append((r['full_url'],r['label_ru'],r['html']))
    assert len(groups)==327 and len(files)==41
    assert set(files)=={n for n in z.namelist() if n.startswith('UPLOAD_TO_SELECTEL/') and n.lower().endswith('.pdf')}
    ids={}; docs=[]; mapping=collections.defaultdict(list)
    for k,entries in groups.items():
        idx=[]
        for e in entries:
            if e not in ids:ids[e]=len(docs);docs.append(e)
            idx.append(ids[e])
        mapping[(k[0],tuple(idx))].append(k[1])
    payload={'documents':docs,'groups':[[b,list(ix),models] for (b,ix),models in mapping.items()],'missing':[[r['brand'],r['model']] for r in c if (r['brand'],r['model']) not in groups]}
    out=pathlib.Path('climate-347/technical-docs/final_mapping_stage25.json');out.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n')
    print('PASS',len(groups),len(files),len(m),len(payload['missing']),flush=True)
