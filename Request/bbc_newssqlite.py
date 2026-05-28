import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3

url = "https://www.bbc.com/news"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

bbc_news = soup.select("a", href=True)

headlines = []
seen = set()

for news in bbc_news:
    link = news.get("href")
    title = news.get_text(strip=True)

    if "news/article" in link and title and link not in seen:
        full_url = urljoin(url, link)
        news_headlines = {"title": title,
                          "link": full_url}
        seen.add(link)
        headlines.append(news_headlines)

for headline in headlines:
    pass

    # print(headline["title"])
    # print(headline["link"])
    # print("-" * 50)

conn = sqlite3.connect("news.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("""
                CREATE TABLE IF NOT EXISTS news(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT,
               link TEXT UNIQUE)""")
conn.commit()

for headline in headlines:  
    cursor.execute("INSERT INTO news (title, link) VALUES(?, ?)",
               (headline["title"],headline["link"]))
conn.commit()


cursor.execute("SELECT * FROM news")
rows = cursor.fetchall()

for row in rows:
    print(f"{row['title']}")
    print(f"{row['link']}")
    print("-" * 40)
# clean_rows = [dict(row) for row in rows]
# print(clean_rows)

conn.close()