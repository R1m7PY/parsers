import requests
from bs4 import BeautifulSoup
import lxml
import json


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"
}


count = 9256
k = 0
results_list = []
for i in range(1, count+1):
    print(f"looking on the {i} page...")

    url = f"https://www.liveinternet.ru/rating/ru/#period=month;page={i};"
    req = requests.get(url, headers=headers)

    with open(f"data/{i}page.html", "w") as file:
        file.write(req.text)
    
    with open(f"data/{i}page.html") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")

    # поиск нужных элементов
    all_results = soup.find_all("div", class_="result")
    for result in all_results:
        result_num = result.find("div", class_="result-num")
        if 15000 < int(result_num) < 60000:
            result_text = result.find("div", class_="text").find("a")
            result_url = result_text.get("href")
            result_title = result_text.text
            k += 1
            results_list.append(
                {
                    "URL": result_url,
                    "Title": result_title,
                    "трафик": result_num
                }
            )
            print(f"found the {k} link")
            print(result_url)
            print("#"*20)

with open("result_list.json", "a", encoding="utf-8") as file:
    json.dump(results_list, file, indent=4, ensure_ascii=False)
