
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
import asyncio
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, driver_id: int):
        await websocket.accept()
        self.active_connections[driver_id] = websocket

    def disconnect(self, driver_id: int):
        if driver_id in self.active_connections:
            del self.active_connections[driver_id]

    async def broadcast(self, driver_id: int, message: dict):
        if driver_id in self.active_connections:
            try:
                await self.active_connections[driver_id].send_text(json.dumps(message))
            except:
                self.disconnect(driver_id)

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, driver_id: int):
    await manager.connect(websocket, driver_id)
    try:
        while True:
            # Keep connection alive
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        manager.disconnect(driver_id)
