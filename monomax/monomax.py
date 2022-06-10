import json
import re

import requests
from bs4 import BeautifulSoup

# url = "https://monomax.by/map"
#
# headers = {
#     "Accept": "*/*",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
#
# }
# req = requests.get(url, headers=headers)
#
# src = req.text
#
# with open("monomax.html", "w", encoding="utf-8") as file:
#     file.write(src)

with open("monomax.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
shops = soup.find_all("div", class_="shop")
shops_data_list = []

pattern = re.compile("53.(.*?)]")
loc = re.findall(pattern, soup.find_all("script", type="text/javascript")[-1].text)

for shop in shops:
    shop_name = "Мономах"

    shop_address = shop.find("p", class_="name").text

    shop_phone = shop.find("p", class_="phone").find("a").text

    loc.pop(0)
    lat = "53." + loc[0].split(", ")[0]
    lon = loc[0].split(", ")[1]
    latlon = [lat, lon]

    shops_data_list.append(
            {
                "address": shop_address,
                "latlon": latlon,
                "name": shop_name,
                "phones": shop_phone
            }
        )

with open("monomax_data.json", "a", encoding="utf-8") as file:
    json.dump(shops_data_list, file, indent=4, ensure_ascii=False)
