import asyncio

class ClientHandler:
    def __init__(self, client_socket, client_address, logger, message_queue):
        self.client_socket = client_socket
        self.client_address = client_address
        self.logger = logger
        self.message_queue = message_queue
        
    async def handle(self):
        try:
            while True:
                data = await asyncio.get_event_loop().sock_recv(self.client_socket, 1024)
                if not data:
                    self.logger.log(f"Client {self.client_address} disconnected.")
                    break
                
                message = data.decode('utf-8')
                self.logger.log(f"Received from {self.client_address}: {message}")
                await self.message_queue.enqueue((self.client_address, message))  # Enqueue message for broadcasting
                
        except (ConnectionResetError, BrokenPipeError) as e:
            self.logger.log(f"Connection error with {self.client_address}: {e}")
        finally:
            self.client_socket.close()

    async def send_response(self, message):
        response = f"Server received: {message}"
        self.logger.log(f"Sending response to {self.client_address}")
        await asyncio.get_event_loop().sock_sendall(self.client_socket, response.encode('utf-8'))
