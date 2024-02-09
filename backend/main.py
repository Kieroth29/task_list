import json

from flask import Flask, request, Response
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest

from utils.validators import user_exists, task_exists
from modules.db import DB

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
    except BadRequest as e:
        return Response(status=422, response=json.dumps({'message': str(e)}), mimetype='application/json')
    
    print(request.json)
    
    if not username:
        return Response(status=422, response=json.dumps({'message': 'Username missing on request payload'}), mimetype='application/json')
    if not password:
        return Response(status=422, response=json.dumps({'message': 'Password missing on request payload'}), mimetype='application/json')
    
    db = DB()
    db.cursor.execute('SELECT id, password FROM users WHERE username = %s;', (username,))
    user = db.fetchone()
    
    if user:
        if check_password_hash(user[1], password):
            return Response(status=200, response=json.dumps({'user_id': user[0], 'username': username}), mimetype='application/json')
        else:
            return Response(status=403, response=json.dumps({'message': 'Invalid password.'}), mimetype='application/json')    
    else:
        return Response(status=404, response=json.dumps({'message': 'User not found.'}), mimetype='application/json')
    
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    hashed_password = generate_password_hash(password)
    
    db = DB()
    db.cursor.execute("SELECT * FROM users WHERE username = %s;", (username,))
    user_check = db.cursor.fetchone()
    if user_check:
        return Response(status=409, response=json.dumps({'message': 'Username already in use.'}), mimetype='application/json')
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
    
    if task_exists(task_id):
        db = DB()
        db.cursor.execute("UPDATE tasks SET description = %s WHERE id = %s", (description, task_id))
        db.commit()
        #TODO User validation
        return Response(status=200)
    else:
        return Response(status=404, response=json.dumps({'message': 'Task not found'}), mimetype='application/json')
    
@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    user_id = request.args.get('user_id')
    print(request)
    
    if not user_id:
        return Response(status=422, response=json.dumps({'message': 'User ID missing on request payload'}), mimetype='application/json')
    
    if user_exists(user_id):
        db = DB()
        db.cursor.execute("SELECT id, description FROM tasks WHERE user_id = %s;", (user_id,))
        
        #TODO Task validation
        tasks_query = db.fetchall()

        tasks = [{'id': task[0], 'description': task[1]} for task in tasks_query]
        print(tasks)
            
        return Response(status=200, response=json.dumps({'tasks': tasks}), mimetype='application/json')
    else:
        return Response(status=404, response=json.dumps({'message': 'User not found'}), mimetype='application/json')
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)