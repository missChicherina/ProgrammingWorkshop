# расширена process
# команды для работы с файлами и папками на сервере.

import socket
import os
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    cmd, *args = req.split()
    if cmd == 'pwd':
        return dirname
    elif cmd == 'ls':
        return '; '.join(os.listdir(dirname))
    elif cmd == 'cat' and args:
        file_path = os.path.join(dirname, args[0])
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        else:
            return 'File not found'
    elif cmd == 'mkdir' and args:
        new_dir = os.path.join(dirname, args[0])
        os.makedirs(new_dir, exist_ok=True)
        return f'Created directory {new_dir}'
    elif cmd == 'rmdir' and args:
        dir_to_remove = os.path.join(dirname, args[0])
        if os.path.exists(dir_to_remove) and os.path.isdir(dir_to_remove):
            os.rmdir(dir_to_remove)
            return f'Directory {dir_to_remove} removed'
        else:
            return 'Directory not found'
    elif cmd == 'delete' and args:
        file_to_delete = os.path.join(dirname, args[0])
        if os.path.exists(file_to_delete) and os.path.isfile(file_to_delete):
            os.remove(file_to_delete)
            return f'File {file_to_delete} removed'
        else:
            return 'File not found'
    elif cmd == 'rename' and len(args) == 2:
        old_name, new_name = args
        old_path = os.path.join(dirname, old_name)
        new_path = os.path.join(dirname, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            return f'File {old_path} renamed to {new_path}'
        else:
            return 'File not found'
    elif cmd == 'upload' and args:
        filename = args[0]
        with open(os.path.join(dirname, filename), 'w') as file:
            file.write(input('Enter file content: '))
        return f'File {filename} uploaded'
    return 'bad request'


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())

conn.close()