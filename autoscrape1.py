import sqlite3
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def scrape_bbc():
    print("Scraping Started....")
    url = "https://www.bbc.com/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        conn = sqlite3.connect("news_bbc.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_bbc (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                link TEXT UNIQUE
            )
        """)

        # Fetch all anchor tags
        bbc_news = soup.find_all("a", href=True)
        
        counter = 0
        for tag in bbc_news:
            href = tag.get("href")
            text = tag.get_text(strip=True)

            if href and text:
                # FIX: Match the exact URL path patterns BBC is currently using live
                if "/news/articles/" in href or "/news/videos/" in href:
                    full_url = urljoin(url, href)

                    cursor.execute("""
                        INSERT OR IGNORE INTO news_bbc (title, link)
                        VALUES (?, ?)
                    """, (text, full_url))
                    counter += 1

        conn.commit()
        conn.close() 
        print(f"Scraping Finished Successfully! Added/Checked {counter} articles.")   
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
    
# Scheduler Setup
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_bbc, "interval", minutes=1)
scheduler.start()

scrape_bbc()

@app.route("/")
def home():
    query = request.args.get("q")
    
    # Run the scraper once on startup if the DB doesn't exist yet
    conn = sqlite3.connect("news_bbc.db")
    cursor = conn.cursor()
    
    if query:
        # FIX 2: Added trailing comma to force Python to recognize this as a tuple
        cursor.execute("SELECT * FROM news_bbc WHERE title LIKE ?", (f"%{query}%",))
        
    else:
        cursor.execute("SELECT * FROM news_bbc") # Newest articles first
        
    news = cursor.fetchall()
    conn.close()
    return render_template("bbc1.html", news=news)

if __name__ == "__main__":
    # FIX 3: use_reloader=False stops APScheduler from starting twice
    app.run(debug=True, use_reloader=False)