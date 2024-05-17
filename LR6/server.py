# тестить на http://localhost:8080/
import socket
import os
import datetime
import configparser
import threading

def load_config():
    config = configparser.ConfigParser()
    config.read("server_config.ini")
    return config["Server"]

def handle_request(request):
    method, resource = request.split()[:2]
    if resource == "/":
        resource = "/index.html"  # Если ресурс не указан, отдаем index.html
    return method, resource

def load_file_content(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def get_content_type(file_path):
    extension = os.path.splitext(file_path)[1]
    if extension in {'.html', '.htm'}:
        return 'text/html'
    elif extension == '.css':
        return 'text/css'
    elif extension == '.js':
        return 'application/javascript'
    elif extension == '.jpg' or extension == '.jpeg':
        return 'image/jpeg'
    elif extension == '.png':
        return 'image/png'
    else:
        return 'application/octet-stream'  # Бинарный тип данных

def build_response(status_code, content_type, content, keep_alive=False):
    response = f"HTTP/1.1 {status_code}\r\n"
    response += "Server: SimpleWebServer\r\n"
    response += "Content-Type: " + content_type + "\r\n"
    response += "Content-Length: " + str(len(content)) + "\r\n"
    if keep_alive:
        response += "Connection: keep-alive\r\n"
    else:
        response += "Connection: close\r\n"
    response += "Date: " + datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT") + "\r\n"
    response += "\r\n"  # Пустая строка, разделяющая заголовок и тело ответа
    response = response.encode() + content
    return response

def serve_client(client_socket):
    while True:
        request_data = client_socket.recv(int(config["max_request_size"])).decode()
        if not request_data:
            break  # Если запрос пустой, заканчиваем обработку
        method, resource = handle_request(request_data)
        
        if method == "GET":
            resource_path = os.path.join(config["work_dir"], resource.strip("/"))
            if os.path.exists(resource_path) and os.path.isfile(resource_path):
                content_type = get_content_type(resource_path)
                content = load_file_content(resource_path)
                response = build_response("200 OK", content_type, content, keep_alive=True)
            else:
                response = build_response("404 Not Found", "text/plain", b"Not Found")
        else:
            response = build_response("405 Method Not Allowed", "text/plain", b"Method Not Allowed")

        client_socket.sendall(response)

    client_socket.close()

def handle_client_connection(client_socket, client_address):
    print(f"Connection from {client_address}")
    serve_client(client_socket)

def main():
    global config
    config = load_config()

    HOST = ''
    PORT = int(config["port"])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server is listening on port {PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, client_address))
        client_thread.start()

    server_socket.close()

if __name__ == "__main__":
    main()
