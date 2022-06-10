import json
import requests

# url = "https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true"
#
# headers = {
#     "Accept": "*/*",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
#
# }
# req = requests.get(url, headers=headers)
#
# q = req.text
#
# with open("kfc.json", "w", encoding="utf-8") as file:
#     file.write(q)

with open("kfc.json", encoding="utf-8") as file:
    src = file.read()

obj = json.loads(src)

kfc_data_list = []

for i in range(0, 1153):
    try:
        kfc_address = obj["searchResults"][i]["storePublic"]["contacts"]["streetAddress"]["ru"]
    except Exception:
        kfc_address = "Нет доступного адреса."

    try:
        kfc_latlon = [obj["searchResults"][i]["storePublic"]["contacts"]["coordinates"]["geometry"]["coordinates"][0], obj["searchResults"][0]["storePublic"]["contacts"]["coordinates"]["geometry"]["coordinates"][1]]
    except Exception:
        kfc_latlon = "Нет доступной геопозиции."

    try:
        kfc_name = obj["searchResults"][i]["storePublic"]["contacts"]["coordinates"]["properties"]["name"]["ru"]
    except Exception:
        kfc_name = "Нет доступного названия."

    try:
        if len(obj["searchResults"][i]["storePublic"]["contacts"]["phone"]["extensions"]) == 0:
            kfc_phones = [obj["searchResults"][i]["storePublic"]["contacts"]["phone"]["number"]]
        else:
            kfc_phones = [obj["searchResults"][i]["storePublic"]["contacts"]["phone"]["number"]]
            phone_extens = []
            for n in range(0,len(obj["searchResults"][i]["storePublic"]["contacts"]["phone"]["extensions"])):
                phone_extens.append(obj["searchResults"][i]["storePublic"]["contacts"]["phone"]["extensions"][n])
            for num in phone_extens:
                kfc_phones.append("Доб. "+num+". ")
    except Exception:
        kfc_phones = "Нет доступных номеров."

    try:
        kfc_working_hours = []
        for day in range(0, 7):
            kfc_day_name = obj["searchResults"][i]["storePublic"]["openingHours"]["regularDaily"][day]["weekDayName"]
            kfc_start_time = obj["searchResults"][i]["storePublic"]["openingHours"]["regularDaily"][day]["timeFrom"]
            kfc_end_time = obj["searchResults"][i]["storePublic"]["openingHours"]["regularDaily"][day]["timeTill"]
            kfc_working_hours.append(kfc_day_name+": "+kfc_start_time+" - "+kfc_end_time+"; ")
    except Exception:
        kfc_working_hours = "closed"

    kfc_data_list.append(
            {
                "address": kfc_address,
                "latlon": kfc_latlon,
                "name": kfc_name,
                "phones": kfc_phones,
                "working_hours": kfc_working_hours
            }
        )


with open("kfc_data.json", "a", encoding="utf-8") as file:
    json.dump(kfc_data_list, file, indent=4, ensure_ascii=False)
