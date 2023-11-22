from typing import List
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, idSala:int):
        await websocket.accept()
        self.active_connections.append([websocket, idSala])

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, data: List[str]):
        data = {"nomeUsuario": data[0], "mensagem": data[1], "idUsuario": data[2], "idSala": data[3]}
        for connection in self.active_connections:
            if data['idSala'] == connection[1]:
                await connection[0].send_json(data)