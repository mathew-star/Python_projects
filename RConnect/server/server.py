import socket
import asyncio
import multiprocessing
from server.logger import Logger
from server.client_handler import ClientHandler
from server.message_queue import MessageQueue
from termcolor import colored
import pyfiglet
from server.worker import worker_process


class Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(False)
        self.logger = Logger('server')
        self.message_queue = MessageQueue()
        self.clients = []
        
        # Creating a multiprocessing pool for CPU-bound tasks
        self.worker_pool = multiprocessing.Pool(processes=4)

    async def start(self):
        result = pyfiglet.figlet_format("S E R V I O", font="slant")
        print(colored(result, 'blue'))
        self.logger.log(f"Server started and listening on {self.host}:{self.port}")

        asyncio.create_task(self.broadcast_loop())  # Start broadcasting loop
        
        while True:
            try:
                client_socket, client_address = await asyncio.get_event_loop().sock_accept(self.server_socket)
                self.logger.log(f"Accepted connection from {client_address}")
                client_handler = ClientHandler(client_socket, client_address, self.logger, self.message_queue)
                self.clients.append(client_handler)
                
                # Handle the client asynchronously
                asyncio.create_task(client_handler.handle())

                # Submit CPU-intensive tasks to the worker pool
                self.worker_pool.apply_async(worker_process, args=(client_address,))  # Submit task to worker
                
            except asyncio.CancelledError:
                self.logger.log("Server shutting down...")
                break
            except Exception as e:
                self.logger.log(f"Error accepting connection: {e}")

    async def broadcast_loop(self):
        while True:
            client_address, message = await self.message_queue.dequeue()
            formatted_message = f"From {client_address}: {message}"
            self.logger.log(f"Broadcasting: {formatted_message}")
            for client in self.clients:
                try:
                    await client.send_response(formatted_message)
                except (ConnectionResetError, BrokenPipeError) as e:
                    self.logger.log(f"Failed to send message to {client.client_address}: {e}")
                    self.clients.remove(client)

if __name__ == '__main__':
    server = Server()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("Server stopped by user.")
