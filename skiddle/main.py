from itertools import count
import json
import string
import requests
from bs4 import BeautifulSoup
import lxml


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"
}

fests_urls_list = list()
for i in range(0, 216, 24):
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=26%20Jan%202022&to_date=&maxprice=500&o={i}&bannertitle=April"
    
    req = requests.get(url, headers=headers)
    json_data = json.loads(req.text)
    html_respons = json_data["html"]

    with open(f"data/index_{i}.html", "w") as file:
        file.write(html_respons)
    
    with open(f"data/index_{i}.html") as file:
        src = file.read()
    
    soup = BeautifulSoup(src, "lxml")
    cards = soup.find_all("a", class_="card-details-link")

    for item in cards:
        fest_url = "https://www.skiddle.com" + item.get("href")
        fests_urls_list.append(fest_url)

count = 0
fest_list_result = list()
for url in fests_urls_list:
    count += 1
    print(count)
    print(url)
    print("#"*count)

    req = requests.get(url, headers=headers)

    try:
        soup = BeautifulSoup(req.text, "lxml")
        fest_info_block = soup.find("div", class_="top-info-cont")

        fest_name = fest_info_block.find("h1").text.strip()
        fest_date = fest_info_block.find("h3").text.strip()
        fest_location_url = "https://www.skiddle.com" + fest_info_block.find("a", class_="tc-white").get("href")

        # get contact details and info
        req = requests.get(fest_location_url, headers=headers)
        soup = BeautifulSoup(req.text, "lxml")

        contact_details = soup.find("h2", string="Venue contact details and info").find_next()
        items = [item.text for item in contact_details.find_all("p")]

        contact_details_dict = dict()
        for contact_detail in items:
            contact_detail_list = contact_detail.split(": ")
            contact_details_dict[contact_detail_list[0]] = contact_detail_list[1]
        
        fest_list_result.append(
            {
                "Fest name": fest_name,
                "Fest date": fest_date,
                "Contacts data": contact_details_dict
            }
        )

    except Exception as ex:
        print(ex)
        print("Oops...")

with open("fest_list_result.json", "a", encoding="utf-8") as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)
