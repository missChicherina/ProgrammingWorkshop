# расширена process

import socket
import os
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

dirname = os.path.join(os.getcwd(), 'docs')
def process(req):
    cmd, *args = req.split()
    if cmd == 'pwd':
        return dirname
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