from flask import Flask, render_template, request, redirect
import sqlite3
import os
print(os.getcwd())

app = Flask(__name__)



def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    print("Creting table...")

    c.execute(""" CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, done INTEGER)""")
    conn.commit()
    conn.close()
init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task = request.form.get("task")
        if task and task.strip():
            conn = sqlite3.connect("tasks.db")
            c = conn.cursor()
            c.execute("INSERT INTO tasks (text, done) VALUES (?, ?)",(task.strip(), 0))
            conn.commit()
            conn.close()
            
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template("todo.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/toggle/<int:id>")
def toggle(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT done FROM tasks WHERE id =?", (id,))
    result = c.fetchone()
    if result:
        current = result[0]
        new_value = 0 if current else 1

    c.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_value, id))

    conn.commit()
    conn.close()
    
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()

    if request.method == "POST":
        new_text = request.form.get("task")

        if new_text and new_text.strip():
            c.execute("UPDATE tasks SET text = ? WHERE id = ?", (new_text.strip(), id))
            conn.commit()
            conn.close()
            return redirect("/")
        else:
            conn.close()
            return "Invalid input"
        
    c.execute("SELECT text FROM tasks WHERE id = ?", (id,))
    task = c.fetchone()
    conn.close()
    if task:
        return render_template("edit.html", task=task[0], id=id)
    else:
        return "Task not found"

app.run(debug=True)