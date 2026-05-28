import sqlite3

conn = sqlite3.connect("news.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS news (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                link TEXT)""")

conn.commit()
print("Table Created")