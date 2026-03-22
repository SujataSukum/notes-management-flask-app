from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------------- DB INIT ----------------
def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            content TEXT,
            time TEXT,
            pinned INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ADD NOTE
@app.route('/add', methods=['POST'])
def add_note():
    data = request.json
    title = data['title']
    content = data['content']
    time = datetime.now().strftime("%d %b %Y, %I:%M %p")

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO notes (title, content, time, pinned) VALUES (?, ?, ?, 0)",
            (title, content, time)
        )
        conn.commit()
    except:
        return jsonify({"message": "Note already exists"})

    conn.close()
    return jsonify({"message": "Note added"})


# GET NOTES
@app.route('/notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, content, time, pinned
        FROM notes
        ORDER BY pinned DESC, id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    notes = {}
    for row in rows:
        notes[row[0]] = {
            "content": row[1],
            "time": row[2],

        }

    return jsonify(notes)


# UPDATE NOTE
@app.route('/update', methods=['PUT'])
def update_note():
    data = request.json
    title = data['title']
    content = data['content']
    time = datetime.now().strftime("%d %b %Y, %I:%M %p")

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notes SET content=?, time=? WHERE title=?",
        (content, time, title)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Updated"})


# DELETE NOTE
@app.route('/delete/<title>', methods=['DELETE'])
def delete_note(title):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM notes WHERE title=?", (title,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})



if __name__ == '__main__':
    app.run(debug=True)
