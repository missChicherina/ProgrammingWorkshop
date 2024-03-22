import socket
from threading import Thread

# Модифицируйте код сервера таким образом, чтобы он читал строки в цикле до тех пор, пока клиент не введет “exit”.
def input_check(message=''):
    a = input(message)
    if a in ['exit', '/stop']:
        exit()
    return a

connection_alive = True

def receive_messages():
    global connection_alive
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            print(data)
        except (ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError) as e:
            connection_alive = False
            print(e)
            break

def send_text(conn, message):
    message = message.encode('utf-8')
    conn.send(message)

host = '127.0.1.1'
print(f"Выставили адрес хоста по умолчанию {host}")
port = 9000
print(f"Выставили порт по умолчанию: {port}")

try:
    sock = socket.socket()
    sock.connect((host, port))
    print(f"Подключение к {host}:{port} успешно!\n")
except (socket.gaierror, ConnectionRefusedError) as e:
    print(f"Не удается подключиться к {host}:{port} ({e})!")

Thread(target=receive_messages, daemon=True).start()

while True:
    while True:
        message = input_check()
        if connection_alive:
            send_text(sock, message)
        else:
            sock.close()
            break
