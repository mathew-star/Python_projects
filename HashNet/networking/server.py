import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_socket.bind(('localhost', 8080))

# Listen for incoming connections
server_socket.listen(1)
print("Server is listening...")

# Accept a connection
connection, client_address = server_socket.accept()

try:
    print(f"Connected by {client_address}")
    
    # Receive data in small chunks
    while True:
        data = connection.recv(1024)  # Receive up to 1024 bytes
        if data:
            print(f"Received: {data.decode('utf-8')}")
            # Send some data back to the client
            connection.sendall(b"Message received")
        else:
            # If no more data, close the connection
            break

finally:
    connection.close()  # Close the connection
