import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


def open_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    soup = bs(
        response.text, 
        "html.parser"
    )

    return soup


# Main website
url = "http://books.toscrape.com/"

soup = open_page(url)

# Find all books
books = soup.find_all(
    "article",
    class_="product_pod"
)

for book in books:

    # Get relative link
    relative_link = book.h3.a["href"]

    # Convert to full URL
    book_url = urljoin(url, relative_link)

    print(f"\nOpening: {book_url}")

    # Open book detail page
    book_soup = open_page(book_url)

    # Book title
    title = book_soup.find("h1").get_text(strip=True)

    # Price
    price = book_soup.find(
        "p",
        class_="price_color"
    ).get_text(strip=True)

    # Stock
    availability = book_soup.find(
        "p",
        class_="instock availability"
    ).get_text(strip=True)

    # Product description
    description_tag = book_soup.find(
        "meta",
        attrs={"name": "description"}
    )

    description = description_tag["content"].strip()

    # Product information table
    table = book_soup.find("table")

    rows = table.find_all("tr")

    product_info = {}

    for row in rows:
        key = row.th.get_text(strip=True)
        value = row.td.get_text(strip=True)

        product_info[key] = value

    # Print scraped data
    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"Availability: {availability}")
    print(f"Description: {description}")

    print("\nProduct Information:")

    for key, value in product_info.items():
        print(f"{key}: {value}")

    print("-" * 60)