import json
import random
import socket
from threading import Thread
import logging

USERS = {}
CONNECTIONS_LIST = []
SALT = 'random_salt'.encode('utf-8')
COLORS = ['\33[31m', '\33[32m', '\33[33m', '\33[34m', '\33[35m', '\33[36m', '\33[91m', '\33[92m', '\33[93m', '\33[94m',
          '\33[95m', '\33[96m']

class ClientThread(Thread):
    def __init__(self, connection, address):
        super().__init__(daemon=True)
        self.connected = True
        self.conn = connection
        self.addr = address
        self.username = None
        self.color = random.choice(COLORS)

    def close_connection(self, reason=''):
        logging.info(f'Соединение закрыто {self.addr} {" - " + reason if reason else ""}')
        self.connected = False
        if self in CONNECTIONS_LIST:
            CONNECTIONS_LIST.remove(self)

    def send_msg(self, message):
        if self.connected:
            send_text(self.conn, message)

    # 3. Модифицируйте код сервера таким образом, чтобы при разрыве соединения клиентом он продолжал слушать данный порт и, 
    # таким образом, был доступен для повторного подключения.
    def run(self):
        CONNECTIONS_LIST.append(self)
        self.send_msg(f'добро пожаловать в чат')
        service_msg(self, 'присоединился к чату')

        while True and self.connected:
            message = self.receive_msg()
            if message == 'exit':
                self.close_connection('пользователь вышел из чата')
                break
            send_msg_all(f'{self.color}{self.username}\33[0m: {message}')


def send_msg_all(message):
    [i.send_msg(message) for i in CONNECTIONS_LIST]

def service_msg(user, message):
    [i.send_msg(f'\33[4m{user.username} {message}\33[0m') for i in CONNECTIONS_LIST if i != user]


def send_text(conn, message):
    message = message.encode('utf-8')
    conn.send(message)

if __name__ == '__main__':
    sock = socket.socket()
    port = 9000
    while True:
        try:
            sock.bind(('', port))
            break
        except OSError:
            port += 1
    print(f'Запущено на {socket.gethostbyname(socket.gethostname())}:{port}')
    logging.info(f'Запущено на {socket.gethostbyname(socket.gethostname())}:{port}')
    sock.listen(10)
    try:
        with open('users.json', 'r') as file:
            USERS = json.load(file)
    except json.decoder.JSONDecodeError:
        USERS = {}
    while True:
        conn, addr = sock.accept()
        print(f'Открыто соединение {addr} ')
        logging.info(f'Открыто соединение {addr} ')
        thread = ClientThread(conn, addr)
        thread.start()
