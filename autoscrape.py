import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request

app = Flask(__name__)

def scrape_bbc():
    print("Scraping Started....")
    url = "https://www.bbc.com/news"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    conn = sqlite3.connect("news_bbc.db")
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_bbc (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                   link TEXT UNIQUE)""")

    

    bbc_news = soup.select("a", href=True)
    for title in bbc_news:
        href = title.get("href")
        text = title.get_text(strip=True)

        if href and "news" in href and text:
            full_url = urljoin(url, href)

            cursor.execute("""
                            INSERT OR IGNORE INTO news_bbc (title, link)
                           VALUES (?, ?)""",
                           (text, full_url))

            
    conn.commit()
    conn.close() 
    print("Scraping Finished....")   
    
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_bbc,
                  "interval", minutes=1)
scheduler.start()

@app.route("/")

def home():
    query = request.args.get("q")
    conn = sqlite3.connect("news_bbc.db")
    cursor = conn.cursor()
    if query:
        cursor.execute("SELECT * FROM news_bbc WHERE title LIKE ?",
                        (f"%{query}%",))
    else:
        cursor.execute("SELECT * FROM news_bbc")
    news = cursor.fetchall()
    conn.close()
    return render_template("bbc1.html", news=news)

app.run(debug=True, use_reloader=False)