from threading import Thread
from getpass import getpass
import socket
import sys
import logging
import pickle
import time


class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        # состояние для обработки входящих пакетов
        self.server_connection()
        self.server_sync()

    def server_connection(self):
        # Соединение с сервером
        sock = socket.socket()
        try:
            sock.connect((self.server_ip, self.server_port))
        except ConnectionRefusedError:
            print(f"Не удалось присоединиться к серверу {self.server_ip, self.server_port}")
            sys.exit(0)
        self.sock = sock
        print(f"Установлено соединение с сервером ('{self.server_ip}', {self.server_port})")
        logging.info(
            f"Установлено соединение {self.sock.getsockname()} с сервером ('{self.server_ip}', {self.server_port})")

    def server_sync(self):
        # Вызов функций при получении команд (статусов) от сервера
        Thread(target=self.receive_data).start()
        self.status = "auth"
        print("'exit' - разорвать соединение, 'shutdown' - выключить сервер")
        while True:
            if self.status:
                if self.status == "auth":
                    self.auth()
                elif self.status == "success":
                    self.success()
                else:
                    user_input = input(f"{self.username}> ")
                    if user_input != "":
                        if user_input == "exit":
                            print(f"Разрыв соединения {self.sock.getsockname()} с сервером по команде")
                            logging.info(f"Разрыв соединения {self.sock.getsockname()} с сервером по команде")
                            close_connection = pickle.dumps(["exit", "Разрыв соедиенения", self.username])
                            self.sock.send(close_connection)
                            self.sock.close()
                            sys.exit(0)
                        elif user_input == "shutdown":
                            shutdown_server = pickle.dumps(["shutdown", "Отключение сервера", self.username])
                            self.sock.send(shutdown_server)
                        elif user_input == "pause":
                            pause_server = pickle.dumps(["pause", "Остановить прослушивание порта", self.username])
                            self.sock.send(pause_server)
                        
                        # Отправляем сообщение и имя клиента
                        send_message = pickle.dumps(["message", user_input, self.username])
                        self.sock.send(send_message)
                        logging.info(f"Отправка данных от {self.sock.getsockname()} на сервер: {user_input}")
            


    def auth(self):
        self.username = input("Введите имя пользователя: ")
        self.sock.send(pickle.dumps(["auth", self.username]))
        time.sleep(0.25)
        
    def success(self):
        # Вывод сообщения об успешной регистрации или авторизации
        print(self.data)
        self.status = "ready"
        self.username = self.data.split(" ")[2]
        logging.info(f"Клиент {self.sock.getsockname()} прошел авторизацию")


def ip_validation(ip):
    if ip == "":
        return False
    else:
        try:
            octets = ip.split(".", 4)
            if len(octets) == 4:
                for octet in octets:
                    octet = int(octet)
                    if 0 <= octet <= 255:
                        pass
                    else:
                        return False
            else:
                return False
        except ValueError:
            return False
        return True


def port_validation(port):
    try:
        value = int(port)
        if 1 <= value <= 65535:
            return True
        print(f"Неправильное значение - {value} для порта")
        return False
    except ValueError:
        print(f"{port} - не число")
        return False


logging.basicConfig(filename='logs/client.log',
                    format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s", level=logging.INFO)


def main():
    user_port = input("Введите порт сервера (enter для значения по умолчанию):")
    user_ip = input("Введите IP-адрес сервера (enter для значения по умолчанию):")
    # Валидация порта и IP адреса клиента
    if not port_validation(user_port):
        user_port = 9090
        print(f"Установлен порт {user_port} по умолчанию")
    if not ip_validation(user_ip):
        user_ip = "127.0.0.1"
        print(f"Установлен IP-адрес {user_ip} по умолчанию")
    Client(user_ip, int(user_port))


if __name__ == "__main__":
    main()

    # & C:/Users/msch/.virtualenvs/robot-zJnRdA8x/Scripts/python.exe c:/Users/msch/OneDrive/PP/LR4/client.py