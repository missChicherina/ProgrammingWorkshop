# Код сервера

import socket
import os
import json

# DIRNAME = os.path.join(os.getcwd(), 'docs')
USERS_FILE = os.path.join(os.getcwd(), 'users.json')

def setWD(wd):
    return wd

def load_users():
    with open(USERS_FILE) as f: 
        return json.load(f)

def process(req):
    cmd, *args = req.split()
    if cmd == 'login' and len(args) == 2:
        print("IN LOGGINING")
        user, password = args
        print(user)
        wd = os.path.join(os.getcwd(), user)
        setWD(wd)
        print("working in dir ", wd)
        if authenticate(user, password):
            return f'Logged in as {user}'
        else:
            return 'Authentication failed'
            
    elif cmd == 'register' and len(args) == 2:
        user, password = args
        if user not in USERS:
            USERS[user] = password
            update_users_file()
            os.makedirs(os.path.join("users", user))
            return f'Registered as {user}'
        else:
            return f'User {user} already exists'
        
    elif cmd == 'ls' and len(args) == 1:
        
        users_wd = os.path.join(os.getcwd(), args[0])
        return '; '.join(os.listdir(users_wd))
    
    elif cmd == 'pwd' and len(args) == 1:
        return os.getcwd()
    
    elif cmd == 'mkdir' and len(args) == 2:
        folder_name = args[0]
        os.makedirs(os.path.join(args[1], folder_name))
        return f'Folder {folder_name} created'
    
    elif cmd == 'rmdir' and len(args) == 2:
        folder_name = args[0]
        try:
            os.rmdir(os.path.join(args[1], folder_name))
        except: 
            return f'Folder {folder_name} doesnt exist'
        return f'Folder {folder_name} deleted'
    
    elif cmd == 'rm' and len(args) == 2:
        file_name = args[0]
        try:
            os.remove(os.path.join(args[1], file_name))
        except: 
            return f'File {file_name} doesnt exist'
        return f'File {file_name} deleted'
    
    elif cmd == 'mv' and len(args) == 3:
        try:
            os.rename(os.path.join(args[2], args[0]), os.path.join(args[2], args[1]))
        except: 
            return f'File {args[0]} doesnt exist'
        return f'File {args[0]} renamed to {args[1]}'
    
    elif cmd == 'exit':
        return 'Goodbye!'
    else:
        return 'Bad request'

def authenticate(user, password):
    return USERS.get(user) == password

def get_work_dir(user):
    work_dir = USERS.get(user)
    if work_dir:
        # Проверка что директория пользователя существует
        if not os.path.exists(work_dir):
            # создание, если не существует
            os.makedirs(work_dir)
        return work_dir
    else:
        return None

def update_users_file():
    with open(USERS_FILE, 'w') as f:
        json.dump(USERS, f)

USERS = load_users()
PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Listening on port", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())

conn.close()