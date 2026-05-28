import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.bbc.com/news"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")
titles = soup.select("a h2")
# print(len(titles))
articles = []

for h2 in titles:
    text = h2.get_text(strip=True)
    parent_a = h2.parent
    href = parent_a.get("href")
    print(href)
    if not href and not text:
        continue
    #if "/news" in href:
    full_url = urljoin(url, href)
    article = {"title": text, "url": full_url}
    articles.append(article)


    # print(article)
    print(full_url)
    print("-" * 50)