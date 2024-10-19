import asyncio
import websockets

class RealTimeNotifier:
    def __init__(self):
        self.connections = set()

    async def handler(self, websocket, path):
        self.connections.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.connections.remove(websocket)

    async def broadcast(self, message):
        if self.connections:
            await asyncio.wait([conn.send(message) for conn in self.connections])

    async def start_server(self):
        server = await websockets.serve(self.handler, "localhost", 8765)
        await server.wait_closed()

