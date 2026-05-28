import requests

url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(url)

data = response.json()
print(data[:2])

for post in data[:5]:
    print(post["title"])
    print()