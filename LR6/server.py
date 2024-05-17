import socket
import os

def handle_request(request):
    # Разбираем запрос на метод и запрашиваемый ресурс
    method, resource = request.split()[:2]
    if resource == "/":
        resource = "/index.html"  # Если ресурс не указан, отдаем index.html
    return method, resource

def load_file_content(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def build_response(status_code, content_type, content):
    response = f"HTTP/1.1 {status_code}\r\n"
    response += "Server: SimpleWebServer\r\n"
    response += "Content-Type: " + content_type + "\r\n"
    response += "Content-Length: " + str(len(content)) + "\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"  # Пустая строка, разделяющая заголовок и тело ответа
    response = response.encode() + content
    return response

def serve_client(client_socket):
    request_data = client_socket.recv(1024).decode()
    method, resource = handle_request(request_data)
    
    if method == "GET":
        if os.path.exists(resource):
            content_type = "text/html" if resource.endswith(".html") else "text/plain"
            content = load_file_content(resource)
            response = build_response("200 OK", content_type, content)
        else:
            response = build_response("404 Not Found", "text/plain", b"Not Found")
    else:
        response = build_response("405 Method Not Allowed", "text/plain", b"Method Not Allowed")

    client_socket.sendall(response)
    client_socket.close()

def main():
    HOST = ''
    PORT = 80

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server is listening on port {PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        serve_client(client_socket)

    server_socket.close()

if __name__ == "__main__":
    main()
