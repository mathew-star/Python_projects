import time
import random

def worker_process(client_address):
    """
    Simulate a CPU-intensive task performed by a worker process.
    This task could be any computation, analysis, or processing related to client input.
    """
    print(f"Worker handling task for {client_address}")
    
    # Simulate a long-running computation or task
    processing_time = random.randint(1, 5)
    time.sleep(processing_time)
    
    print(f"Task completed for {client_address} after {processing_time} seconds")
