import asyncio

class MessageQueue:
    """We are adding a simple message queue using Python’s asyncio.Queue to handle the broadcasting of messages. 
    The queue will hold messages that need to be broadcasted to all connected clients.
    """
    def __init__(self):
        self.queue = asyncio.Queue()

    async def enqueue(self, message):
        await self.queue.put(message)

    async def dequeue(self):
        return await self.queue.get()
