import socket
import threading

# Function to handle incoming client messages
def handle_client(client_socket, address):
    print(f"Connected: {address}")
    while 1:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            print(f"Received from {address}: {message}")

            # Broadcast message to all clients except the sender
            broadcast(message, client_socket)
        except Exception as e:
            print(f"Error: {e}")
            break

    print(f"Disconnected: {address}")
    client_socket.close()

# Function to broadcast messages to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                client.close()
                clients.remove(client)

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

#TCP connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("Server started...")

clients = []

# Accept incoming connections and start a new thread for each client
while 1:
    client_socket, address = server.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
    client_thread.start()
