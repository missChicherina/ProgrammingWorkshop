import socket
import json

HOST = 'localhost'
PORT = 6666
USERS_FILE = 'users.json'

def load_users():
    with open(USERS_FILE) as f:
        return json.load(f)

USERS = load_users()
    
def login():
    user = input("Username: ")
    password = input("Password: ")
    return f"login {user} {password}"

def login_with_uname(user):
    password = input("Password: ")
    return f"login {user} {password}"

def register():
    user = input("Enter new username: ")
    if user in USERS: login_with_uname(user)
    password = input("Enter new password: ")
    return f"register {user} {password}"

def action_menu():
    print("Choose action:")
    print("1. View current directory contents")
    print("2. Print current working directory")
    print("3. Exit")

def send_to_serve(request):    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    print("sock.connect((HOST, PORT))")
    sock.send(request.encode())
    print("sock.send(request.encode())")
    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()

def main():
    sock = socket.socket()
    sock.connect((HOST, PORT))

    while True:
        print("1. Login")
        print("2. Register")
        choice = input("Select an option: ")

        if choice == '1':
            request = login()
        elif choice == '2':
            request = register()
        else:
            print("Invalid choice. Please enter 1 or 2.")
            continue

        sock.send(request.encode())
        response = sock.recv(1024).decode()
        print(response)

        if "Logged in" in response:
            break

    while True:
        action_menu()
        choice = input("Select an action: ")

        if choice == '1':            
            send_to_serve('pwd')
        
        elif choice == '2':
            send_to_serve('pwd')
            # request = "pwd"
            
        elif choice == 'ls':
            send_to_serve(request)

        elif choice == '3': 
            request = "exit"
            sock.send(request.encode())
            response = sock.recv(1024).decode()
            print(response)
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        # sock.send(request.encode())
        # response = sock.recv(1024).decode()
        # print(response)
        # sock = socket.socket()
        # sock.connect((HOST, PORT))
        
        # sock.send(request.encode())
        
        # response = sock.recv(1024).decode()
        # print(response)
        
        sock.close()

    sock.close()

if __name__ == "__main__":
    main()
