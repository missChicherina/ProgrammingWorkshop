# Клиент
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os


def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

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


def load_keys():
    if os.path.exists("client_private_key.pem") and os.path.exists("client_public_key.pem"):
        with open("client_private_key.pem", "r") as f:
            private_key = f.read()
        with open("client_public_key.pem", "r") as f:
            public_key = f.read()
        return private_key, public_key
    else:
        private_key, public_key = generate_key_pair()
        with open("client_private_key.pem", "w") as f:
            f.write(private_key.decode())
        with open("client_public_key.pem", "w") as f:
            f.write(public_key.decode())
        return private_key, public_key
    


def main():
    client_private_key, client_public_key = load_keys()
    print("Keys loaded")
    
    # Подключение к серверу для установления режима шифрования
    encryption_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    encryption_client.connect(('localhost', 12345))
    print("Encription mode")

    # Получаем публичный ключ сервера для установления режима шифрования
    server_public_key = encryption_client.recv(4096)
    print("Getting public key")

    # Создаем новый сокет для основного общения
    communication_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socked created")

    # Получаем номер порта для основного общения
    communication_port = int(encryption_client.recv(4096).decode())
    print("Communication port:", communication_port)

    # Подключаемся к серверу для основного общения
    communication_client.connect(('localhost', communication_port))

    # Отправляем публичный ключ клиента для установления режима шифрования
    encryption_client.send(server_public_key)

    # Ожидаем сообщение от сервера
    received_message = communication_client.recv(4096)
    decrypted_message = decrypt_message(received_message, client_private_key)
    print("Received message from server:", decrypted_message.decode())

    message = "Hello, server!"
    encrypted_message = encrypt_message(message.encode(), server_public_key)
    communication_client.send(encrypted_message)

    communication_client.close()
    encryption_client.close()

if __name__ == "__main__":
    main()
