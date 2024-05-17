# Функции для работы с пользователями:
# load_users(): Загружает данные о пользователях из файла users.json.
# save_users(users): Сохраняет данные о пользователях в файл users.json.

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
import json
import os
from datetime import datetime

app = Flask(__name__)

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/user/', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    users = load_users()
    
    if username in users:
        return jsonify({"error": "User already exists"}), 400
    
    hashed_password = generate_password_hash(password)
    users[username] = {
        "password": hashed_password,
        "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    save_users(users)
    
    return jsonify({"message": "User registered successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
