from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.database.schemas.user import User
from app.database.session import db_repo
from app.depends.security import get_current_user
from app.models.base import Response
from app.models.ws import ResponseWebsocket
from app.services.websocket_manager import ManagerWebsocket

router = APIRouter(
    tags=['Игра']
)


@router.post('/bet')
async def place_bet(
        amount: int,
        user: User = Depends(
            get_current_user
        ),
):




    await ManagerWebsocket.send_message(
        message=ResponseWebsocket(
            status='ok',
            type='bet',
            data={
                "player": {
                    "id": user.id,
                    'name': user.first_name + " " + user.last_name,
                },
                "amount": amount
            }
        ).dict()
    )

    return Response(
        success=True,
        message='The bet was placed successfully'
    )


@router.websocket('/ws')
async def websocket_endpoint(
        websocket: WebSocket,

):
    await ManagerWebsocket.accept(ws=websocket)

    try:
        await websocket.send_json(
            ResponseWebsocket(
                status='ok',
                type='connect',
                data={
                    'message': 'connect'
                }
            ).dict()
        )

        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ManagerWebsocket.disconnect(websocket)
