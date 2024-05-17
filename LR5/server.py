import socket
import pickle
import random


def generate_private_key():
    return random.randint(2, 100)

def generate_public_key(g, p, private_key):
    return (g ** private_key) % p

def generate_shared_secret(public_key, private_key, p):
    return (public_key ** private_key) % p


HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

msg = conn.recv(1024)
print(pickle.loads(msg))

conn.close()