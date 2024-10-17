import socket
import threading
import sys

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                print("Connection closed by the server.")
                break
        except:
            print("An error occurred while receiving the message.")
            break

def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_ip> <server_port>")
        return

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
    except:
        print("Unable to connect to the server.")
        return

    # Start a thread to continuously listen for messages from the server
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    # Handle sending messages from the client to the server
    try:
        while True:
            message = input()
            if message.lower() == 'exit':
                client_socket.close()
                break
            client_socket.send(message.encode('utf-8'))

    except KeyboardInterrupt:
        print("Client disconnected.")
        client_socket.close()

if __name__ == "__main__":
    main()
