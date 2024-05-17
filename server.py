from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import socket

def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_message(message, public_key):
    recipient_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    encrypted_message = cipher_rsa.encrypt(message)
    return encrypted_message

def decrypt_message(encrypted_message, private_key):
    key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(key)
    decrypted_message = cipher_rsa.decrypt(encrypted_message)
    return decrypted_message

def main():
    server_private_key, server_public_key = generate_key_pair()
    client_private_key, client_public_key = generate_key_pair()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(1)
    print("Server listening...")

    conn, addr = server.accept()

    conn.send(server_public_key)
    client_public_key = conn.recv(4096)

    message = "Hello, client!"
    encrypted_message = encrypt_message(message.encode(), client_public_key)
    conn.send(encrypted_message)

    received_message = conn.recv(4096)
    decrypted_message = decrypt_message(received_message, server_private_key)
    print("Received message from client:", decrypted_message.decode())

    conn.close()
    server.close()

if __name__ == "__main__":
    main()
