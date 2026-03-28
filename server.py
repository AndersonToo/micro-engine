# server.py  —  Phase 1 + 2 + 3
import socket
from request import Request
from router import app              # ← add this

HOST = "localhost"
PORT = 8080

def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"\n[*] Listening on http://{HOST}:{PORT}\n")

    while True:
        client_socket, client_address = server_socket.accept()
        raw_data = client_socket.recv(4096)
        http_text = raw_data.decode("utf-8")

        req = Request(http_text)

        if req.method:
            print(f"[{req.method}] {req.path}")
            response = app.resolve(req)         # ← router handles it now
        else:
            response = (
                "HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n"
            )

        client_socket.sendall(response.encode("utf-8"))
        client_socket.close()

if __name__ == "__main__":
    run()