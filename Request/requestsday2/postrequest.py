import requests

url = "https://httpbin.org/post"

data = {"username": "upesh",
        "password": "1234"
        }

response = requests.post(url, data=data)

print(response.text)