import requests

response = requests.get("http://127.0.0.1:5000/api/news")

data = response.json()
print(data)

for item in data:
    print(item['title'])