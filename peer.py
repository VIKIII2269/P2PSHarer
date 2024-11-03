
import socket
import threading
import os

# Constants
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
BUFFER_SIZE = 4096  # 4 KB
SEPARATOR = "<SEPARATOR>"

# Start a server to listen for incoming file requests
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, port))
    server_socket.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"[+] {address} is connected.")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    # Receive the filename requested
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename = received.strip()

    if os.path.isfile(filename):
        # Send file size and filename
        filesize = os.path.getsize(filename)
        client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

        # Start sending the file
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)
        print(f"[+] File '{filename}' sent successfully.")
    else:
        client_socket.send(f"ERROR: File '{filename}' not found.".encode())
    client_socket.close()

# Function to request a file from a peer
def request_file(host, port, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(filename.encode())

    # Receive file details
    file_details = client_socket.recv(BUFFER_SIZE).decode()
    if "ERROR" in file_details:
        print(file_details)
        client_socket.close()
        return

    filename, filesize = file_details.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    # Start receiving the file
    with open(filename, "wb") as f:
        total_received = 0
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            total_received += len(bytes_read)
            print(f"[+] Downloading '{filename}': {total_received/filesize*100:.2f}% complete", end="\r")

    print(f"\n[+] File '{filename}' downloaded successfully.")
    client_socket.close()

# Start server in a separate thread
server_thread = threading.Thread(target=start_server, args=(SERVER_PORT,))
server_thread.daemon = True
server_thread.start()

# Interact with other peers
print("Type 'exit' to quit.")
while True:
    command = input("Enter command (e.g., 'download <host> <port> <filename>'): ")
    if command.lower() == "exit":
        break
    elif command.startswith("download"):
        _, host, port, filename = command.split()
        request_file(host, int(port), filename)
    else:
        print("Invalid command. Use 'download <host> <port> <filename>' or 'exit'.")
