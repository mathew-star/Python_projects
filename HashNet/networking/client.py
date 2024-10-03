import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server's IP address and port
client_socket.connect(('127.0.0.1', 8888))

try:
    # Send data to the server
    message = "Hello, Server!"
    client_socket.sendall(message.encode('utf-8'))

    # Wait for the response from the server
    response = client_socket.recv(1024)
    print(f"Received: {response.decode('utf-8')}")

finally:
    client_socket.close()  # Close the socket
