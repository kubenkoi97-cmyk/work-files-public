# Термотрейд и IGC — MIXED / этап 2 (2026-10-13)

**Состояние:** промежуточный результат; 17/744 моделей с подтверждёнными источниками, 727 ожидают исследования. Не считать готовым каталогом.

## Формат входного Excel
- Исходный лист `Лист1` — 744 товарные строки и 15 столбцов A:O; исходный столбец C пуст и не содержит модель.
- Для защиты исходных данных модель выделена из оригинального столбца B в новый лист `MIXED — обработка`: A=описание, B=характеристики, C=точная модель, D=исходное название, E:I=бренд, источник, статус, QA, номер исходной строки.
- Количество моделей по брендам: IGC 121; Kentatsu 296; Midea 283; Daikin 32; Bosch 12.
- Перепроверено, что оригинальный лист полностью сохранён и 744 модели соответствуют исходным строкам.

## Подтверждённые источники
- IGC IMS-K22NH(DC), IMS-K28NH(DC), IMS-K36NH(DC), IMS-K45NH(DC), IMS-K56NH(DC), IMS-K71NH(DC): https://www.c-o-k.ru/library/instructions/igc/kondicionery-promyshlennye/38333/141247.pdf
- Kentatsu KTGV18HZBN1: https://mircli.ru/Kentatsu-KTGV18HZBN1/
- Kentatsu KTGV24HZBN1: https://mircli.ru/Kentatsu-KTGV24HZBN1/
- Kentatsu KTGV30HZBN1: https://mircli.ru/Kentatsu-KTGV30HZBN1/
- Kentatsu KTGV40HZBN1: https://mircli.ru/Kentatsu-KTGV40HZBN1/
- Midea MI2-15GDHN18(At): https://mircli.ru/Midea-MI2-15GDHN18-At-/
- Midea MI2-22GDHN18(At): https://mircli.ru/Midea-MI2-22GDHN18-At-/
- Midea MI2-28GDHN18(At): https://mircli.ru/Midea-MI2-28GDHN18-At-/
- Midea MI2-36GDHN18(At): https://mircli.ru/Midea-MI2-36GDHN18-At-/
- Daikin FXKQ20A: https://mircli.ru/Daikin-FXKQ20A/
- Daikin FXKQ25A: https://mircli.ru/Daikin-FXKQ25A/
- Bosch MDCI 12-1 (identity): https://www.bosch-homecomfort.com/web-etk/de/bosch/de/de/product/7739835418
- Bosch MDCI 12-1 (specifications): https://bosch.generadordeprecios.info/rehabilitacion/calculaprecio.asp?Valor=2%7C0_0_0_0_0_0%7C2%7CIBB010%7Cicn_ibb010%3Ac16_0

## Контроль качества / ограничения
- Не переносить параметры между суффиксами `DC`, `DC5`, а также между внутренними и наружными блоками.
- IGC: технические таблицы проверены, но описания неполные.
- Daikin FXKQ20A / FXKQ25A: значение R32 из карточек продавца требует подтверждения региональной технической документацией.
- На заданных приоритетных сайтах выполнены **пробные точные поисковые запросы**. Поштучная проверка всех 744 моделей на каждом домене не выполнена.
- Excel содержит все 744 позиции и 17 заполненных строк; исходные данные не менялись.
- Данный коммит фиксирует статус и источники. Бинарный XLSX доступен в текущем чате, так как коннектор GitHub в этой операции предоставляет запись UTF-8 файлов, но не загрузку локального XLSX.
