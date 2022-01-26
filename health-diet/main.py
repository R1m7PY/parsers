import requests
from bs4 import BeautifulSoup
import json
import csv

url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"
}

req = requests.get(url, headers=headers)
src = req.text

with open("index.html", "w") as file:
   file.write(src)

with open("index.html") as file:
   src = file.read()

soup = BeautifulSoup(src, "lxml")
all_product_hrefs = soup.find_all(class_="mzr-tc-group-item-href")

all_catigories_dict = dict()
for item in all_product_hrefs:
   item_text = item.text
   item_href = "https://health-diet.ru" + item.get("href")
    
   all_catigories_dict[item_text] = item_href

with open("all_catigories_dict.json", "w") as file:
   json.dump(all_catigories_dict, file, indent=4, ensure_ascii=False)

with open("all_catigories_dict.json") as file:
    all_catigories = json.load(file)

iteration_count = int(len(all_catigories)) - 1
count = 0
print(f"Всего итераций {iteration_count}")
for category_name, category_href in all_catigories.items():
    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")

    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", "w") as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    
    # проверяем наличие таблицы на странице
    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue

    # собираем заголовки таблицы
    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    # собираем данные продуктов
    products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    product_info = list()
    for item in products_data:
        product_tds = item.find_all("td")

        title = product_tds[0].find("a").text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text
        
        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }
        )

        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

    with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"{count} итерация выполнена. {category_name} заполнен...")

