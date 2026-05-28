from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")

def home():
    conn = sqlite3.connect("news.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news")
    news = cursor.fetchall()
    conn.close()

    html = "<h1>{BBC News}</h1>"

    for item in news:
        html += f"""
        <h3>{item['title']}</h3>
        <a href="{item['link']}">
        {item['link']}</a>
        <hr>
        """
    return html 
app.run(debug=True)