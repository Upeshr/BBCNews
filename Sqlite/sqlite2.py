import sqlite3

conn = sqlite3.connect("news.db")
cursor = conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS news(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT, link TEXT
               )""")
conn.commit()

cursor.execute(
    "INSERT INTO news (title, link) VALUES (?, ?)",
      ("Breaking news",
        "https://www.example.com" ))

conn.commit()

cursor.execute("SELECT * FROM news")
rows = cursor.fetchall()
for row in rows:
    print(row)


conn.close()