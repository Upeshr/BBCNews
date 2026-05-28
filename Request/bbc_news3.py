import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.bbc.com/news"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

soup = BeautifulSoup(response.text, "html.parser")

titles = soup.select("a")

for h2 in titles:

    title = h2.get_text(strip=True)

    # go to parent <a>
    parent_a = h2.parent

    href = h2.get("href")
    print(href)

    full_url = urljoin(url, href)

    print(title)
    print(full_url)
    print("-" * 50)