# Код клиента

import socket
import os
import json

HOST = 'localhost'
PORT = 6666
USERS_FILE = os.path.join(os.getcwd(), 'users.json')

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
    print("View current directory contents: LS")
    print("Print current working directory: PWD")
    print("Create folder: MKDIR + new name of your dir")
    print("Delete folder: RMDIR + name of your folder to delete")
    print("Delete file: RM + filename to delete")
    print("Rename file: MV + oldname + newname")
    print("For exit: EXIT")


def send_to_serve(request):    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(request.encode())
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
            if request.split()[1] != "admin":
                user = os.path.join(os.getcwd(), "users", request.split()[1])
            else:
                user = os.path.join(os.getcwd(), "users")
            print(user)
        elif choice == '2':
            request = register()
            user = os.path.join(os.getcwd(), "users", request.split()[1])
            sock.send(request.encode())
            break
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
        print("---------------------------------------\n")
        req = input("your cmd here > ")
        cmd = req.split()[0]
        if cmd != 'mkdir' and cmd != "pwd" and cmd != "ls" and cmd != "rmdir" and cmd != "rm" and cmd != "mv" and cmd != "mv":
            print("Check your cmd is correct")
            continue
        req = req + " " + user
        sock = socket.socket()
        sock.connect((HOST, PORT))
        sock.send(req.encode())
        response = sock.recv(1024).decode()
        print(response)
        print("\n---------------------------------------\n")
        sock.close()

if __name__ == "__main__":
    main()

