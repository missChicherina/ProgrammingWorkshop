# Сервер
import socket
import random

def generate_private_key():
    return random.randint(2, 100)

def generate_public_key(g, p, private_key):
    return (g ** private_key) % p

def generate_shared_secret(public_key, private_key, p):
    return (public_key ** private_key) % p

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(1)
    print("Server listening...")

    conn, addr = server.accept()

    g = 5  # генератор
    p = 23  # простое число

    private_key = generate_private_key()
    public_key = generate_public_key(g, p, private_key)

    conn.send(str(public_key).encode())
    client_public_key = int(conn.recv(1024).decode())

    shared_secret = generate_shared_secret(client_public_key, private_key, p)
    print("Shared secret:", shared_secret)

    conn.close()
    server.close()

if __name__ == "__main__":
    main()
