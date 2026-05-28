import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.bbc.com/news"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

soup = BeautifulSoup(response.text, "html.parser")

articles = []

# find all links
links = soup.find_all("a")

for link in links:
    href = link.get("href")
    text = link.get_text(strip=True)

    # skip empty text or empty href
    if not href or not text:
        continue

    # only keep news article links
    if "/news/" in href:

        full_url = urljoin(url, href)

        article = {
            "title": text,
            "url": full_url
        }

        articles.append(article)

# remove duplicates
unique_articles = []

seen = set()

for article in articles:
    if article["url"] not in seen:
        seen.add(article["url"])
        unique_articles.append(article)

# print results
for article in unique_articles[:10]:
    print(article)