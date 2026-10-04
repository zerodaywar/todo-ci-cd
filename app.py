from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

DATABASE = "todo.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/todos", methods=["GET"])
def get_todos():
    conn = get_db()

    todos = conn.execute(
        "SELECT * FROM todos ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([
        {
            "id": todo["id"],
            "title": todo["title"],
            "completed": bool(todo["completed"])
        }
        for todo in todos
    ])


@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json()

    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Task cannot be empty"}), 400

    conn = get_db()

    cursor = conn.execute(
        "INSERT INTO todos (title) VALUES (?)",
        (title,)
    )

    conn.commit()

    todo_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "id": todo_id,
        "title": title,
        "completed": False
    }), 201


@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()

    completed = bool(data.get("completed", False))

    conn = get_db()

    conn.execute(
        "UPDATE todos SET completed = ? WHERE id = ?",
        (int(completed), todo_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_db()

    conn.execute(
        "DELETE FROM todos WHERE id = ?",
        (todo_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
