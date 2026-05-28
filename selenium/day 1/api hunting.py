import requests
import json

url = "https://www.daraz.com.np/catalog/?ajax=true&from=hp_categories&isFirstRequest=true&page=1&q=Electric%20Bikes&service=all_channel&spm=a2a0e.tm803317"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

data = response.json()

print(data.keys())
print(data["mods"].keys())

products = data["mods"]["listItems"]

print(len(products))

print(products[0])

for item in products:
    name = item.get("name")
    price = item.get("price")
    brand = item.get("brandName")
    rating = item.get("ratingScore")
    location = item.get("location")

    print(name)
    print(price)
    print(brand)
    print(rating)
    print(location)
    print("-" * 50)