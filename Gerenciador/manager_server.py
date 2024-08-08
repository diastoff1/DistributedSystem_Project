import socket
import random

# Manager Server Configuration
MANAGER_HOST = ""
MANAGER_PORT = 8080

# Worker Servers Configuration
WORKER_SERVERS = [("127.0.0.1", 8082)]

def handle_client(client_socket):
    # Choose a worker server to handle the request
    worker_host, worker_port = random.choice(WORKER_SERVERS)
    
    # Create a connection to the worker server
    worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker_socket.connect((worker_host, worker_port))
    
    # Forward the client request to the worker server
    request = client_socket.recv(1024)
    worker_socket.sendall(request)
    
    # Get the response from the worker server
    response = worker_socket.recv(1024)
    
    # Send the response back to the client
    client_socket.sendall(response)
    
    # Close the sockets
    worker_socket.close()
    client_socket.close()

def start_manager():
    manager_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    manager_socket.bind((MANAGER_HOST, MANAGER_PORT))
    manager_socket.listen(5)
    
    print(f"Manager Server listening on port {MANAGER_PORT}...")
    
    while True:
        client_socket, addr = manager_socket.accept()
        print(f"Accepted connection from {addr}")
        
        # Handle the client request (sequentially)
        handle_client(client_socket)

start_manager()
