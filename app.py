from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# 数据库初始化
def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         content TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

# 确保数据库存在
init_db()

# 服务静态文件
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# API 路由
@app.route('/api/todos', methods=['GET'])
def get_todos():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM todos')
    todos = [{'id': row[0], 'content': row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('INSERT INTO todos (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo added successfully'}), 201

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True) 