# Обработка информации в формате JSON
# Блок 2: Сервис принимает и отдает информацию в формате JSON

from flask import Flask, request, jsonify
import json
import hashlib
import datetime

app = Flask(__name__)
users = []

@app.route('/user/', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    salt = hashlib.sha256(username.encode()).hexdigest()
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    registration_date = datetime.datetime.now().isoformat()
    
    user = {
        "username": username,
        "password_hash": password_hash,
        "salt": salt,
        "registration_date": registration_date
    }
    users.append(user)
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = next((user for user in users if user["username"] == username), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user), 200

if __name__ == '__main__':
    app.run(debug=True)
