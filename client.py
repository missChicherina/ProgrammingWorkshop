import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))

    server_public_key = client.recv(4096)
    client_public_key = client.recv(4096)
    client.send(client_public_key)

    received_message = client.recv(4096)
    decrypted_message = decrypt_message(received_message, client_private_key)
    print("Received message from server:", decrypted_message.decode())

    message = "Hello, server!"
    encrypted_message = encrypt_message(message.encode(), server_public_key)
    client.send(encrypted_message)

    client.close()

if __name__ == "__main__":
    main()
