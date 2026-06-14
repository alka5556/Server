import socket

def start_server():
    # 1. Создаем TCP-сокет (AF_INET - IPv4, SOCK_STREAM - TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Позволяет повторно использовать порт сразу после перезапуска сервера
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 2. Привязываем сокет к адресу и порту
    HOST = '127.0.0.1'
    PORT = 8080
    server_socket.bind((HOST, PORT))
    
    # 3. Начинаем слушать входящие соединения
    server_socket.listen(5)
    print(f"[*] Сервер запущен на http://{HOST}:{PORT}")
    
    try:
        while True:
            # 4. Принимаем соединение от клиента (браузера или curl)
            client_socket, client_address = server_socket.accept()
            print(f"[+] Новое подключение от {client_address}")
            
            # Временно просто закрываем соединение, чтобы потестить
            client_socket.close()
            
    except KeyboardInterrupt:
        print("\n[*] Останавливаем сервер...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()