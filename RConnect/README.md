# Real-Time Communication Server with Python (`asyncio` & `multiprocessing`)

**Note:** !!  This project is still under active development and has not yet reached its full potential. There are known issues and areas for improvement. Contributions and feedback are welcome as we work towards a more complete and robust solution. !!


## Overview

This project implements a real-time communication service using **Python's `asyncio` for I/O-bound tasks** and **`multiprocessing` for CPU-bound tasks**. The server can handle multiple clients simultaneously, broadcasting messages between them and utilizing worker processes to handle CPU-intensive operations in parallel.

### Features

- **Asynchronous Communication**: Non-blocking communication between the server and clients using Python's `asyncio`.
- **Multiprocessing**: Offload CPU-bound tasks to multiple worker processes, improving scalability and performance.
- **Message Broadcasting**: All connected clients receive messages from each other in real-time.
- **Graceful Error Handling**: Handles exceptions and connection errors gracefully, with detailed logging.
- **Log Monitoring**: Logs key events, client connections, disconnections, and errors for monitoring the system.

---




## Development Approach

This project was developed with a focus on writing clean, maintainable, and extensible code. We adhered to several key software engineering principles:

1. **SOLID Principles:** We have leveraged on SOLID principles to improve the quality of software.

2. **Modular Architecture:** The project is organized into distinct modules (auth, password, storage) to separate concerns and improve maintainability.

3. **Design Patterns:** We've implemented patterns like Dependency Injection (e.g., injecting the DataStore into the PasswordManager) to reduce coupling between components.

4. **Code Structure and Organization:** The codebase follows a clear, logical structure with meaningful file and directory names, adhering to Python's PEP 8 style guide.

5. **Error Handling and Logging:** Robust error handling is implemented throughout the application to improve reliability and user experience.

## Project Structure

```
RConnect/
├── server/
│   ├── __init__.py
│   ├── server.py            # Main server file with multiprocessing
│   ├── client_handler.py     # Handles individual client connections
│   ├── message_queue.py      # Queue implementation for client message broadcasting
│   ├── logger.py            # Logging for debugging and monitoring
│   ├── error_handler.py     # Graceful error handling
│   ├── worker.py            # Worker process handling individual tasks
│
├── client/
│   ├── __init__.py
│   ├── client.py            # Client for communicating with the server
│
├── logs/
│   └── server.log           # Log file for server monitoring
├── README.md                # Project documentation
└── requirements.txt         # Dependencies

```


### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/mathew-star/Python_project.git
    cd Python_projects/Rconnect
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```



---

## Running the Server

To start the server:

```bash
python -m server.server
```

To start the client :

```bash
cd client
python client.py
```


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.