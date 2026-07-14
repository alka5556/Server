# Multi-Threaded HTTP/1.0 Web Server From Scratch

This project is an HTTP/1.0 web server built from scratch in Python using the basic socket library. It handles network connections directly without relying on high-level web frameworks.

## Features

* **Basic Socket Handling**: Uses standard TCP sockets to bind to a port, listen for connections, and accept clients.
* **Reading Requests**: Reads incoming data in chunks until it spots the `\r\n\r\n` sequence, which marks the end of the HTTP headers.
* **Parsing**: Manually reads the first line of the request to get the HTTP method (like GET), the requested file path, and the HTTP version.
* **Serving Files**: Only handles GET requests. It serves static files like HTML, CSS, images, and text files from the local directory.
* **Security**:
    * Blocks directory traversal attacks (rejects paths with `..` or `\`).
    * Restricts access to the `public` folder. If someone tries to look at the `private` folder, the server returns a `403 Forbidden` error.
* **Proper HTTP Formatting**: Builds the HTTP response from scratch, including the status line, headers (Content-Type, Content-Length), and the actual file data.
* **Status Codes**: Returns the correct HTTP codes: `200 OK`, `400 Bad Request`, `403 Forbidden`, `404 Not Found`, and `405 Method Not Allowed`.
* **Multi-threading**: Uses Python's `threading` module to create a new thread for each client. This way, if one request is slow, it doesn't block other users from connecting.
* **Stateless**: Closes the connection immediately after sending the response (`Connection: close`). It doesn't keep sessions open.

## Dependencies:

* **None.** This project uses only the Python Standard Library. 

# How to run and test:

1. Start the server from your terminal:
```bash
python server.py

The server will automatically create the www folder with public and private subdirectories and generate 5 test files.

2. Open your browser and navigate to:
[http://127.0.0.1:8080/](http://127.0.0.1:8080/)

3. To test security and error handling, you need to access to these URLs in your browser:

* **Blocked Directory:** http://127.0.0.1:8080/private/secret.html (Should return 403 Forbidden)
* **Directory Traversal:** http://127.0.0.1:8080/../../etc/passwd (Should return 403 Forbidden)
* **Not Found:** http://127.0.0.1:8080/public/notexists.html (Should return 404 Not Found)

4. Testing malformed request (400 Bad Request):
Test sending a corrupted HTTP request line that violates the standard format. This can only be tested via terminal:
```bash
python -c "import socket; s=socket.socket(); s.connect(('127.0.0.1',8080)); s.sendall(b'GET /\r\n\r\n'); print(s.recv(1024).decode()); s.close()"

5. Running a verbose connection trace in your terminal to review explicit \r\n tokens and raw protocol layouts:
curl -v http://127.0.0.1:8080/ -UseBasicParsing
Or
curl.exe -v http://127.0.0.1:8080/public/index.html

Testing video: https://drive.google.com/file/d/18Qqf5Feg5baKm1mJ5igZw08qzCDLpXkY/view?usp=sharing


