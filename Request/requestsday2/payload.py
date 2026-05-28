import requests

url = "https://httpbin.org/post"

payload = {
    "username": "upesh",
    "password": "1234"
}

response = requests.post(url, data=payload)

data = response.json()

print(data["form"])