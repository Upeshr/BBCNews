import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0: Win64; x64) " "AppleWebKit/537.36 (KHTML like Gecko) " "Chrome/136.0.0.0 Safari/537.36"), "Accept-Language": "en-US,en;q=0.9"}
session = requests.Session()
response = session.get("https://www.bbc.com/news")
soup = BeautifulSoup(response.text, "html.parser")

titles = soup.select("h2")
for title in titles[:10]:
    print(title.text.strip())
    print()
