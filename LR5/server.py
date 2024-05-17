# Сервер
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import threading

# Функция для генерации ключей
def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Функция для загрузки ключей сервера
def load_keys():
    if os.path.exists("server_private_key.pem") and os.path.exists("server_public_key.pem"):
        with open("server_private_key.pem", "r") as f:
            private_key = f.read()
        with open("server_public_key.pem", "r") as f:
            public_key = f.read()
        return private_key, public_key
    else:
        private_key, public_key = generate_key_pair()
        with open("server_private_key.pem", "w") as f:
            f.write(private_key.decode())
        with open("server_public_key.pem", "w") as f:
            f.write(public_key.decode())
        return private_key, public_key

# Функция для загрузки разрешенных публичных ключей
def load_allowed_public_keys():
    allowed_keys = []
    if os.path.exists("allowed_public_keys.txt"):
        with open("allowed_public_keys.txt", "r") as f:
            for line in f:
                allowed_keys.append(line.strip())
    return allowed_keys


# Функция для проверки публичного ключа клиента
def verify_client_key(client_public_key, allowed_keys):
    return client_public_key in allowed_keys
# Функция для шифрования сообщения
def encrypt_message(message, public_key):
    recipient_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    encrypted_message = cipher_rsa.encrypt(message)
    return encrypted_message

# Функция для дешифрования сообщения
def decrypt_message(encrypted_message, private_key):
    key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(key)
    decrypted_message = cipher_rsa.decrypt(encrypted_message)
    return decrypted_message

# Функция для установления режима шифрования
def establish_encryption_mode(client_socket):
    private_key, public_key = load_keys()
    client_socket.send(public_key)
    client_public_key = client_socket.recv(4096)
    return private_key, public_key, client_public_key

# Функция для обработки соединения с клиентом
def handle_client(client_socket, client_addr):
    server_private_key, server_public_key = load_keys()
    allowed_keys = load_allowed_public_keys()

    print("Handling connection from", client_addr)

    client_public_key = client_socket.recv(4096)
    if not verify_client_key(client_public_key.decode(), allowed_keys):
        print("Client public key not allowed. Closing connection.")
        client_socket.close()
        return

    client_socket.send(server_public_key)

    message = "Hello, client!"
    encrypted_message = encrypt_message(message.encode(), client_public_key)
    client_socket.send(encrypted_message)

    received_message = client_socket.recv(4096)
    decrypted_message = decrypt_message(received_message, server_private_key)
    print("Received message from client:", decrypted_message.decode())

    client_socket.close()

def main():
    # Пул портов для обработки соединений
    ports = [12345, 12346, 12347]  # Пример пула портов

    # Создание потоков для обработки соединений на каждом порту
    threads = []
    for port in ports:
        thread = threading.Thread(target=start_server, args=(port,))
        thread.start()
        threads.append(thread)

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

# Функция для запуска сервера на определенном порту
def start_server(port):
    server_private_key, server_public_key = load_keys()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen(5)
    print("Server listening on port", port)

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
