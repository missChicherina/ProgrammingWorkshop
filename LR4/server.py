from threading import Thread
import socket
import json
import pickle
import logging
import hashlib


class Server:
    def __init__(self, port):
        self.database = "./users.json"
        self.server_port = port
        self.users = []
        self.connections = []
        self.paused = False

        self.init_server()

    def init_server(self):
        # 2. при подключении клиента создавался новый поток, в котором происходило взаимодействие с ним.
        sock = socket.socket()
        sock.bind(('', self.server_port))
        sock.listen(5)
        self.sock = sock
        logging.info(f"Старт сервера, порт: {self.server_port}")
        while True:
            conn, addr = self.sock.accept()
            Thread(target=self.client_logic, args=(conn, addr)).start()
            logging.info(f"Подключение клиента {addr}")
            self.connections.append(conn)

    def broadcast(self, msg, conn, username):
        # Отправка сообщений всем клиентам (чат)
        for connection in self.connections:
            if connection != conn:
                connection.send(pickle.dumps(["message", msg, username]))
                logging.info(f"Отправка данных клиенту {connection.getsockname()}: {msg}")

    
    def client_logic(self, conn, address):
        # Поток прослушивания клиентов
        self.authorization(address, conn)
        while True:
            try:
                data = conn.recv(1024)
            except ConnectionResetError:
                conn.close()
                self.connections.remove(conn)
                logging.info(f"Отключение клиента {address}")
                break
            if data:
                status, data, username = pickle.loads(data)
                logging.info(f"Прием данных от клиента '{username}_{address[1]}': {data}")

                if status == "message":
                    self.broadcast(data, conn, username)

                # 4. Команда "Отключение сервера" (завершение программы):
                elif status == "shutdown":
                    for connection in self.connections:
                        connection.send(pickle.dumps(["message", f"{username} выключил сервер", "~SERVER~"]))
                        connection.close()
                    logging.info(f"Отключение сервера по команде")
                    self.sock.close()
                    break

                elif status == "exit":
                    logging.info(f"Закрытие соединения с клиентом {username}")
                    conn.close()
                    self.connections.remove(conn)
                    for connection in self.connections:
                        connection.send(pickle.dumps(["message", f"{username} отключился от сервера", "~SERVER~"]))
                    break

            else:
                # Закрываем соединение
                conn.close()
                self.connections.remove(conn)
                logging.info(f"Отключение клиента {address}")
                break

    def authorization(self, addr, conn):
        # "Реализовать простой чат сервер на базе сервера аутентификации.
        # Авторизация пользователей
        conn.send(pickle.dumps(["auth", "Введите имя пользователя: "]))
        logging.info(f"Клиент {self.sock.getsockname()} успешно авторизировался")

    def database_read(self):
        with open(self.database, 'r') as f:
            users = json.load(f)
        return users

    def database_write(self):
        with open(self.database, 'w') as f:
            json.dump(self.users, f, indent=4)


def is_available_port(port):
    try:
        sock = socket.socket()
        sock.bind(("", port))
        sock.close()
        logging.info(f"Порт {port} свободен")
        return True
    except OSError:
        logging.info(f"Порт {port} занят")
        return False


def main():
    server_port = 9090  # порт по умолчанию
    # Если порт по умолчанию занят, то перебираем порты
    if not is_available_port(server_port):
        logging.info(f"Порт по умолчанию {server_port} занят")
        port_available = False
        while not port_available:
            server_port += 1
            port_available = is_available_port(server_port)
    Server(server_port)


if __name__ == "__main__":
    main()
