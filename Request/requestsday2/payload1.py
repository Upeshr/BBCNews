import requests

url = "https://httpbin.org/post"

payload = {
    "search": "laptop"
}

response = requests.post(url, json=payload)

data = response.json()

print(data["json"])