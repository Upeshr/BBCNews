import requests
from bs4 import BeautifulSoup

for page in range(1, 5):
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    print(f"\nScrapping Page: {page}")
    response = requests.get(url)
    print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.select(".product_pod")
    print(len(books))

    for book in books:
        title = book.h3.a["title"]
        print(title)