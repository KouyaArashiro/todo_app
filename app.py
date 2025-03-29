from flask import Flask, request, jsonify, render_template
import pymysql

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'todo_user',
    'password': 'medialab',
    'database': 'todo_app',
    'charset': 'utf8mb4',
    # get dict from mysql 
    'cursorclass': pymysql.cursors.DictCursor
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    todo = request.form.get('todo')
    if not todo:
        return "No input", 400

    conn = pymysql.connect(**DB_CONFIG)
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO todos (todo) VALUES (%s)", (todo,))
        conn.commit()
    return "OK"

@app.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete(todo_id):
    conn = pymysql.connect(**DB_CONFIG)
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        conn.commit()
    return "Deleted"

@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit(todo_id):
    new_todo = request.form.get('todo')
    conn = pymysql.connect(**DB_CONFIG)
    with conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE todos SET todo = %s WHERE id = %s", (new_todo, todo_id))
        conn.commit()
    return "Updated"



@app.route('/list')
def list_todos():
    conn = pymysql.connect(**DB_CONFIG)
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, todo FROM todos ORDER BY id DESC")
            todos = cur.fetchall()
    return jsonify(todos)

if __name__ == '__main__':
    app.run(debug=True)
