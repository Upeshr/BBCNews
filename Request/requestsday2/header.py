import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.com/news"
headers = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) " "AppleWebKit/537.36 (KHTML, like Gecko) " "Chrome/136.0.0.0 Safari/537.36"), "Accept-Language": "en-US,en;q=0.9"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

titles = soup.select("h2")

for title in titles[:10]:
    print(title.text.strip())