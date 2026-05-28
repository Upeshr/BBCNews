from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)
@app.route("/")

def home():
    query = request.args.get("q")
    conn = sqlite3.connect("news_bbc.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if query:
        cursor.execute("SELECT * FROM news_bbc WHERE title LIKE ?",
                        (f"%{query}%",))
    else:
        cursor.execute("SELECT * FROM news_bbc")

    news = cursor.fetchall()
    conn.close()
    return render_template("bbc.html", news=news)

@app.route("/api/news")

def api_news():
    conn = sqlite3.connect("news_bbc.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news_bbc")
    rows = cursor.fetchall()
    conn.close()
    news = []
    for row in rows:
        news.append({"id": row["id"],
                     "title": row['title'],
                     "link": row['link']})
    return jsonify(news)

@app.route("/api/news/<int:id>")

def single_news(id):
    conn = sqlite3.connect("news_bbc.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news_bbc WHERE id=?", (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"id": row['id'],
                        "title": row['title'],
                        "link": row['link']})
    return {"error": "News not found"}

@app.route("/api/search")

def search_news():
    query = request.args.get("q")
    conn = sqlite3.connect("news_bbc.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news_bbc WHERE title LIKE ?",
                    (f"%{query}%",))
    
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({"id": row['id'],
                        "title": row['title'],
                        "link": row['link']})
    return jsonify(results)

app.run(debug=True)