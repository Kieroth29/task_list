import json
from flask import Flask, request, Response
from flask_cors import CORS
from modules.db import DB
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    
    db = DB()
    db.cursor.execute('SELECT id, password FROM users WHERE username = %s;', (username,))
    user = db.fetchone()
    if user:
        if check_password_hash(user[1], password):
            return Response(status=200, response=json.dumps({'id': user[0], 'username': username}), mimetype='application/json')
        else:
            return Response(status=403, response=json.dumps({'error': 'Wrong password.'}), mimetype='application/json')    
    else:
        return Response(status=404, response=json.dumps({'error': 'User not found.'}), mimetype='application/json')
    
@app.route('/register', methods=['POST'])
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    hashed_password = generate_password_hash(password)
    
    db = DB()
    db.cursor.execute("SELECT * FROM users WHERE username = %s;", (username,))
    user_check = db.cursor.fetchone()
    if user_check:
        return Response(status=400, response=json.dumps({'error': 'Username already in use.'}), mimetype='application/json')
    else:
        db.cursor.execute('INSERT INTO users(username, password) VALUES (%s, %s) RETURNING id;', (username, hashed_password))
        db.commit()
        user_id = db.fetchone()[0]
        return Response(status=200, response=json.dumps({'user_id': user_id}), mimetype='application/json')
    
@app.route('/create_task', methods=['POST'])
def create_task():
    user_id = int(request.args.get('user_id'))
    description = request.args.get('description')
    
    db = DB()
    db.cursor.execute("INSERT INTO tasks(description, user_id) VALUES (%s, %s)", (description, user_id))
    db.commit()
    #TODO User validation
    return Response(status=200)

app.route('/delete_task', methods=['DELETE'])
def delete_task():
    task_id = request.args.get('task_id')
    
    db = DB()
    db.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()
    #TODO User validation
    #TODO Task validation
    return Response(status=200)

@app.route('/update_task', methods=['PATCH'])
def update_task():
    task_id = request.args.get('task_id')
    description = request.args.get('description')
    
    db = DB()
    db.cursor.execute("UPDATE tasks SET description = %s WHERE id = %s", (description, task_id))
    db.commit()
    #TODO User validation
    #TODO Task validation
    return Response(status=200)
    
@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    user_id = int(request.args.get('user_id'))
    
    db = DB()
    db.cursor.execute("SELECT id, description FROM tasks WHERE user_id = %s;", (user_id,))
    #TODO User validation
    #TODO Task validation
    tasks_query = db.fetchall()

    tasks = []
    for task in tasks_query:
        tasks.append({'id': task[0], 'description': task[1]})
        
    return Response(status=200, response=json.dumps({'tasks': tasks}), mimetype='application/json')
    
if __name__ == '__main__':
    app.run(debug=True)