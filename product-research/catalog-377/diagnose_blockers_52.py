#!/usr/bin/env python3
"""Root-cause matrix for exactly 52 unfinished original HTML product archives."""
import csv, json
from collections import Counter
from pathlib import Path
root=Path("product-research/catalog-377")
out=root/"diagnostics"
out.mkdir(parents=True,exist_ok=True)
def load(p):
    with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
items=load(root/"status/master_status.csv")
sources=load(root/"supporting-evidence/sku_source_map.csv")
factory={(x["brand"],x["model"]):x for x in sources}
assert len(items)==377
pending=[x for x in items if x.get("status")!="COMPLETE"]
assert len(pending)==52,len(pending)
records=[]
for x in pending:
    brand,model,status=x["brand"],x["model"],x["status"]
    has_url=bool(x.get("source_url"))
    imgs=int(x.get("image_count") or 0)
    has_specs=x.get("has_specs")=="True"
    has_desc=x.get("has_description")=="True"
    factory_exact=factory.get((brand,model),{}).get("exact_sku_confirmed_in_pdf")=="True"
    if brand=="Kentatsu":
        assert status=="PARTIAL" and has_url and imgs>0 and has_specs and not has_desc
        code="PUBLISHED_WITHOUT_PRODUCT_DESCRIPTION"
        action="Keep exact original HTML+photos; find another exact original page with narrative, or attach a separately identified manufacturer series description."
    elif brand=="Midea":
        assert status=="PARTIAL" and has_url and imgs>0 and has_specs and not has_desc
        code="ORIGINAL_PAGE_ONLY_SPECS_AND_IMAGES"
        action="Check tabs, JSON-LD, and another exact SKU source. Keep factory manual as separately identified appendix, not part of original HTML."
    else:
        assert brand=="IGC" and status=="NOT_FOUND"
        code="EXACT_SKU_NOT_CONFIRMED" if not factory_exact else "HISTORICAL_SKU_NO_ORIGINAL_INDIVIDUAL_PAGE"
        action="Search documented historical URLs or authorized distributor exports, keeping exact DC suffix; do not replace by DC5 or DC7."
    records.append(dict(brand=brand,model=model,excel_row=x["excel_row"],
        legacy_status=status,original_html_exists=has_url,
        html_source=x.get("source_url",""),archive=x.get("archive_download_url",""),
        local_product_photos=imgs,specifications_identified=has_specs,
        original_product_description_identified=has_desc,
        manufacturer_document_exact_sku=factory_exact,root_cause=code,
        action=action,archive_integrity="NOT_REVERIFIED_IN_THIS_REPORT"))
with (out/"blockers_52.csv").open("w",encoding="utf-8-sig",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
cnt=dict(Counter(x["root_cause"] for x in records))
summary=dict(catalog_total=377,complete_claimed_in_master=325,unresolved=len(records),
    distribution=cnt,original_page_plus_photos_exists=sum(x["original_html_exists"] for x in records),
    no_individual_original_html=sum(not x["original_html_exists"] for x in records),
    warning="Registry COMPLETE is not independent ZIP verification. Existing standalone audit suffered GitHub HTTP 504.")
(out/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
md=["# Диагностика незакрытых оригинальных HTML по 52 моделям",
"",
"Основание — актуальный реестр 377 SKU и карта заводской документации. Никакие описания или исходные HTML не создаются из предположений.",
"",
f"Реестр: 325 COMPLETE и {len(records)} незакрытых. Это не означает, что все 325 ZIP повторно подтверждены.",
"",
"## Почему не закрыто",
""]
for k,v in sorted(cnt.items()):md.append(f"- {k}: {v} моделей.")
md+=["",
"40 PARTIAL: сохранены исходный HTML точного товара, технические характеристики и изображения, но отдельное опубликованное описание не подтверждено.",
"12 IGC NOT_FOUND: точная оригинальная товарная страница исторической версии не подтверждена, несмотря на упоминание ряда моделей в заводских каталогах.",
"",
"## Исправления метода",
"",
"1. Не искать описание по словам во всём HTML: меню магазина и карточки связанных товаров дают ложные совпадения. Проверять именно контейнер товара, с разметкой и доказательством текста.",
"2. Разделить причины неудач: HTTP 404, HTTP 429/Retry-After, HTTP 503, антибот, таймаут, нет точного заголовка, нет картинок, нет отдельного описания.",
"3. Для JS-страниц: настоящий браузерный DOM и локальные ресурсы через Playwright или архивирование WACZ. Это не создаёт информацию, отсутствующую у продавца.",
"4. Для GitHub проверять ZIP посредством authenticated gh release download, unzip -t, декодирования фотографий и SHA-256; успешная публикация сама по себе не равна проверке.",
"5. Для старых IGC: исторические точные URLs/прошлые архивные снимки/прямые запросы к производителю. Модели с DC, DC5, DC7 не подменять.",
"",
"Отдельно вести SOURCE_HTML_CAPTURED, SOURCE_HAS_DESCRIPTION, DATA_PACK_COMPLETE, RELEASE_ZIP_VERIFIED. Исходный HTML не дополнять сторонними материалами, иначе он перестанет быть оригинальным.",
"",
"[Точный поартикульный CSV](./blockers_52.csv) • [Основной реестр](../status/master_status.csv)"]
(out/"README.md").write_text("\n".join(md)+"\n",encoding="utf-8")
print("DIAGNOSED",json.dumps(summary,ensure_ascii=False),flush=True)
