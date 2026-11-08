import requests
from bs4 import BeautifulSoup
urlpaths=[
"http://coolsochi.ru/product/midea-mih90ghn18-dp/",
"http://coolsochi.ru/product/kentatsu-ktkb18hzbn1/",
"http://vsekondicioneri.ru/product/midea-mih90ghn18/",
"http://ryazan.vsekondicioneri.ru/product/midea-mih90ghn18/",
"http://gorodskie-sistemy.ru/polupromyshlennoe-oborudovanie/vrf-sistemy-kondicionirovaniya/vnutrennij-blok-vrv/vnutrennij-blok-vrf-sistemy-midea-mih90ghn18",
"http://brand-climat.ru/midea-mih90ghn18-dp",
"http://brand-climat.ru/midea-mih90ghn18",
"http://air-midea.com/product/mih90ghn18/",
"https://kondicionerkin.ru/midea-mih90ghn18/",
]
for u in urlpaths:
    try:
        r=requests.get(u,timeout=12,headers={"User-Agent":"Mozilla/5.0"},allow_redirects=True)
        soup=BeautifulSoup(r.text,"html.parser")
        heads=[x.get_text(" ",strip=True) for x in soup.find_all("h1")][:2]
        text=soup.get_text(" ",strip=True).lower()
        print("PAGE",r.status_code,len(r.content),"MATCH",str("mih90ghn18" in text),"DESC",str("описание" in text),"SPEC",str("характеристики" in text),"IMG",len(soup.find_all("img")),"H1",heads,"URL",r.url,flush=True)
    except Exception as e:print("ERROR",u,str(e)[:150],flush=True)
