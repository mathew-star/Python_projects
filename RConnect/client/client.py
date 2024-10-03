import socket
import asyncio

class Client:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    async def start(self):
        await asyncio.get_event_loop().sock_connect(self.client_socket, (self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

        # Start listening for incoming messages
        receive_task = asyncio.create_task(self.receive_messages())

        # Start sending messages
        await self.send_messages()

        # Ensure the receive task is cancelled when sending is done
        receive_task.cancel()
        try:
            await receive_task  # Wait for the receive task to fully cancel
        except asyncio.CancelledError:
            print("Receive task cancelled successfully.")

        # Close the socket after exiting
        self.client_socket.close()

    async def send_messages(self):
        while True:
            print("Enter 0 to exit ....")
            message = input("Enter message: ")
            if message == '0':  # User wants to exit
                print("Closing connection...")
                break
            await asyncio.get_event_loop().sock_sendall(self.client_socket, message.encode('utf-8'))

    async def receive_messages(self):
        try:
            while True:
                data = await asyncio.get_event_loop().sock_recv(self.client_socket, 1024)
                if not data: 
                    print("Server closed the connection.")
                    break
                print(f"Received: {data.decode('utf-8')}")
        except asyncio.CancelledError:
            print("Receive task cancelled.")
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            print("Connection closed by server.")
        finally:
            print("Closing receive task...")

if __name__ == '__main__':
    client = Client()
    try:
        asyncio.run(client.start())
    except KeyboardInterrupt:
        print("Client stopped by user.")
