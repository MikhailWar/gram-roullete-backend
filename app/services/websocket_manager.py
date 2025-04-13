import logging
import typing

from starlette.websockets import WebSocket


class ManagerWebsocket:
    clients: typing.List[WebSocket] = []

    @classmethod
    async def accept(cls, ws: WebSocket):
        await ws.accept()
        cls.clients.append(ws)


    @classmethod
    def disconnect(cls, ws: WebSocket):
        if ws in cls.clients:
            cls.clients.remove(ws)

    @classmethod
    async def send_message(cls, message: dict):
        for client in cls.clients:
            await client.send_json(message)


