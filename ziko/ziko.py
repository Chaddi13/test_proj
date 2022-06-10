import json
import re

import requests
from bs4 import BeautifulSoup

# url = "https://www.ziko.pl/lokalizator/"
#
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",

}
# req = requests.get(url, headers=headers)
#
# src = req.text
#
# with open("ziko.html", "w", encoding="utf-8") as file:
#     file.write(src)

with open("ziko.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")

pharmacies = soup.find_all("div", class_="morepharmacy")
pharmacy_urls = []
for pharmacy in pharmacies:
    pharmacy_urls.append(f"https://www.ziko.pl{pharmacy.find('a').get('href')}")

pharmacies_data_list = []

for pharmacy_url in pharmacy_urls:
    req = requests.get(pharmacy_url, headers=headers)
    pharmacy_loc = pharmacy_url.split("/")[-2]

    with open(f"data/{pharmacy_loc}.html", "w", encoding="utf-8") as file:
        file.write(req.text)

    with open(f"data/{pharmacy_loc}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    try:
        pharmacy_address = soup.find("strong", text=re.compile("Adres")).find_next_sibling().text
    except Exception:
        pharmacy_address = "No address :("

    try:
        pharmacy_name = soup.find("strong", text=re.compile("Placówka")).find_next_sibling().text
    except Exception:
        pharmacy_name = "No name :("

    try:
        pharmacy_phones = []
        pharmacy_phone = soup.find("strong", text=re.compile("Telefon")).find_parent().find_all("a")
        for phone in pharmacy_phone:
            pharmacy_phones.append(phone.text)
    except Exception:
        pharmacy_phones = ["No phones :("]

    try:
        pharmacy_working_hours = []
        pharmacy_hours = soup.find("strong", text=re.compile("Godziny otwarcia")).find_next_sibling().find_all("span")
        for hour in pharmacy_hours:
            pharmacy_working_hours.append(f"{hour.text} {hour.next_element.next_element}")
    except Exception:
        pharmacy_working_hours = ["No working hours :("]

    try:
        pharmacy_latlon = []
        pharmacy_loc = soup.find("div", class_="coordinates").find_all("span")
        for loc in pharmacy_loc:
            pharmacy_latlon.append(float(loc.text.split(" ")[-2]))
    except Exception:
        pharmacy_latlon = ["No location available :("]

    pharmacies_data_list.append(
        {
            "address": pharmacy_address,
            "latlon": pharmacy_latlon,
            "name": pharmacy_name,
            "phones": pharmacy_phones,
            "working_hours": pharmacy_working_hours
        }
    )

with open("pharmacies_data.json", "a", encoding="utf-8") as file:
    json.dump(pharmacies_data_list, file, indent=4, ensure_ascii=False)
