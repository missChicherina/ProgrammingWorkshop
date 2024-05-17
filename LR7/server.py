# расширена process
# возможность авторизации пользователя на сервере.

import socket
import os
import json

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

dirname = os.path.join(os.getcwd(), 'docs')
USERS_FILE = 'users.json'


def load_users():
    with open(USERS_FILE) as f:
        return json.load(f)

def process(req):
    cmd, *args = req.split()
    if cmd == 'login' and len(args) == 2:
        user, password = args
        if authenticate(user, password):
            return f'Logged in as {user}'
        else:
            return 'Authentication failed'
    elif cmd == 'pwd':
        work_dir = get_work_dir(user)
        if work_dir:
            return work_dir
        else:
            return f'Work directory for {user} does not exist'
    elif cmd == 'ls':
        return '; '.join(os.listdir(dirname))
    elif cmd == 'cat' and args:
        file_path = os.path.join(dirname, args[0])
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        else:
            return 'File not found'
    return 'bad request'


def authenticate(user, password):
    return USERS.get(user) == password

def get_work_dir(user):
    work_dir = USERS.get(user)
    if work_dir:
        # Проверяем, существует ли рабочая директория пользователя
        if not os.path.exists(work_dir):
            # Если не существует, создаем ее
            os.makedirs(work_dir)
        return work_dir
    else:
        return None


USERS = load_users()
PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())

conn.close()