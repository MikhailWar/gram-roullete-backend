import datetime
import typing

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.config import Config
from app.database.schemas.game import Game, PlayerGame
from app.database.schemas.user import User, TransactionUser, TransactionType
from app.database.session import db_repo
from app.depends.security import get_current_user
from app.models.base import Response, ResponseMessage
from app.models.game import CurrentGame, Player, Bet
from app.models.ws import ResponseWebsocket
from app.services.jobs.game import end_game_job
from app.services.single import SingleObj
from app.services.websocket_manager import ManagerWebsocket

router = APIRouter(
    tags=['Игра']
)



@router.get('/game', response_model=CurrentGame)
async def current_game(
        user: User = Depends(
            get_current_user
        )
):
    repo = db_repo.get()

    game = await repo.game.get_current_game()

    if game is None:
        raise HTTPException(
            status_code=404,
            detail='Not found current game'
        )



    game_dto = CurrentGame(
        id=game.id,
        end_date=game.end_date,
        players=[
            Player(
                id=player.user_id,
                name=player.user.full_name,
                amount=player.bet_amount
            )
            for player in game.players
        ]
    )


    return game_dto





@router.post('/bet', response_model=ResponseMessage)
async def place_bet(
        bet: Bet,
        user: User = Depends(
            get_current_user
        ),
):


    repo = db_repo.get()


    current_balance = await repo.users.get_balance(user.id)
    if bet.amount > current_balance:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough money')

    game = await repo.game.get_current_game()

    scheduler = SingleObj.scheduler
    is_create = False


    if game is None:
        game = Game(
            is_finish=False,
            end_date=datetime.datetime.now() + datetime.timedelta(seconds=Config.misc.game_seconds)
        )
        is_create = True


    game.players.append(
        PlayerGame(
            user_id=user.id,
            bet_amount=bet.amount

        )
    )

    repo.session.add(game)

    transaction = TransactionUser(
        amount=-bet.amount,
        user_id=user.id,
        transaction_type=TransactionType.BET
    )

    repo.session.add(transaction)
    await repo.session.commit()

    if is_create:
        scheduler.add_job(
            end_game_job,
            args=(game.id,),
            run_date=game.end_date
        )



    await ManagerWebsocket.send_message(
        message=ResponseWebsocket(
            status='ok',
            type='bet',
            data={
                "player": {
                    "id": user.id,
                    'name': user.first_name + " " + user.last_name,
                },
                "amount": bet.amount,
                "game": {
                    'id': game.id,
                    'end_date': game.end_date.timestamp()
                }
            }
        ).dict()
    )

    return ResponseMessage(
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
