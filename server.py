import socket
import threading
import os

PORT = 8080
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

STATIC_ROOT = "www"
ALLOWED_SUBDIR = "public"  
BLOCKED_SUBDIR = "private" 

# create folders and test files automatically
def create_mock_files():
    os.makedirs(STATIC_ROOT + "/" + ALLOWED_SUBDIR, exist_ok=True)
    os.makedirs(STATIC_ROOT + "/" + BLOCKED_SUBDIR, exist_ok=True)
    
    with open(STATIC_ROOT + "/" + ALLOWED_SUBDIR + "/index.html", "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'><title>Home Page</title></head><body><h1>My HTTP Server is Working!</h1><p>The assignment is running successfully.</p></body></html>")
    with open(STATIC_ROOT + "/" + ALLOWED_SUBDIR + "/about.html", "w", encoding="utf-8") as f:
        f.write("<html><body><h1>About Us</h1><p>Multithreaded network programming assignment.</p></body></html>")
    with open(STATIC_ROOT + "/" + ALLOWED_SUBDIR + "/style.css", "w", encoding="utf-8") as f:
        f.write("body { background-color: #fafafa; font-family: sans-serif; }")
    with open(STATIC_ROOT + "/" + ALLOWED_SUBDIR + "/info.txt", "w", encoding="utf-8") as f:
        f.write("Plain text file successfully loaded.")
    with open(STATIC_ROOT + "/" + BLOCKED_SUBDIR + "/secret.html", "w", encoding="utf-8") as f:
        f.write("<html><body><h1>403 Forbidden: Access Denied</h1></body></html>")

# get content type based on file extension
def get_mime_type(file_path):
    if file_path.endswith(".html") or file_path.endswith(".htm"):
        return "text/html; charset=utf-8"
    elif file_path.endswith(".css"):
        return "text/css"
    elif file_path.endswith(".txt"):
        return "text/plain; charset=utf-8"
    elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
        return "image/jpeg"
    elif file_path.endswith(".png"):
        return "image/png"
    return "application/octet-stream"

# build and send the http response layout
def send_http_response(conn, status_code, status_text, content_type="text/html", body=b""):
    headers = "HTTP/1.0 " + str(status_code) + " " + status_text + "\r\n"
    headers += "Content-Type: " + content_type + "\r\n"
    headers += "Content-Length: " + str(len(body)) + "\r\n"
    headers += "Connection: close\r\n"
    headers += "\r\n"  # empty line between headers and body
    
    conn.sendall(headers.encode('ascii'))
    if body:
        conn.sendall(body)

# client handler function for threads
def handle_client(conn, addr):
    print("Client connected from: " + str(addr))
    try:
        # read from socket until end of headers
        req_bytes = b""
        while b"\r\n\r\n" not in req_bytes:
            chunk = conn.recv(1024)
            if not chunk:
                break
            req_bytes += chunk

        if not req_bytes:
            return

        req_text = req_bytes.decode('utf-8', errors='ignore')
        lines = req_text.split("\r\n")
        
        if len(lines) == 0 or not lines[0]:
            send_http_response(conn, 400, "Bad Request", body=b"400 Bad Request")
            return

        req_line = lines[0].split()
        
        if len(req_line) != 3:
            print("Error: invalid request line format from " + str(addr))
            send_http_response(conn, 400, "Bad Request", body=b"400 Bad Request")
            return

        method, path, version = req_line[0], req_line[1], req_line[2]
        print("Request: " + method + " " + path + " from " + str(addr))

        # only GET method allowed
        if method != "GET":
            send_http_response(conn, 405, "Method Not Allowed", body=b"405 Method Not Allowed")
            return

        # directory traversal security check
        if ".." in path or "\\" in path:
            print("Security warning! Blocked path attempt: " + path)
            send_http_response(conn, 403, "Forbidden", body=b"403 Forbidden")
            return

        # default route to index.html
        if path == "/":
            path = "/" + ALLOWED_SUBDIR + "/index.html"
        
        clean_path = path.lstrip("/")
        parts = clean_path.split("/")
        subdir = parts[0] if len(parts) > 1 else ""

        # check access permissions for subdirectory
        if subdir != ALLOWED_SUBDIR:
            print("Access blocked to folder: " + subdir + " for " + str(addr))
            send_http_response(conn, 403, "Forbidden", body=b"403 Forbidden")
            return

        full_path = os.path.join(STATIC_ROOT, clean_path)

        # handle 404 if file doesn't exist
        if not os.path.exists(full_path) or os.path.isdir(full_path):
            send_http_response(conn, 404, "Not Found", body=b"404 Not Found")
            return

        # read file content and serve it
        with open(full_path, "rb") as f:
            data = f.read()
            mime = get_mime_type(full_path)
            send_http_response(conn, 200, "OK", content_type=mime, body=data)

    except Exception as e:
        print("Error handling client " + str(addr) + ": " + str(e))
    finally:
        conn.close()

def start_server():
    create_mock_files()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(ADDR)
    server_socket.listen()
    print("Server started on http://" + SERVER + ":" + str(PORT))
    
    while True:
        conn, addr = server_socket.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()

if __name__ == "__main__":
    start_server()