# Клиент
import socket
import random

def generate_private_key():
    return random.randint(2, 100)

def generate_public_key(g, p, private_key):
    return (g ** private_key) % p

def generate_shared_secret(public_key, private_key, p):
    return (public_key ** private_key) % p

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))

    g = 5  # генератор
    p = 23  # простое число

    private_key = generate_private_key()
    public_key = generate_public_key(g, p, private_key)

    server_public_key = int(client.recv(1024).decode())
    client.send(str(public_key).encode())

    shared_secret = generate_shared_secret(server_public_key, private_key, p)
    print("Shared secret:", shared_secret)

    client.close()

if __name__ == "__main__":
    main()
