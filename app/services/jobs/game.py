import logging
import random

from app.database.repo.request import RequestRepo
from app.database.schemas.game import PlayerGame
from app.database.schemas.user import TransactionUser, TransactionType
from app.database.session import get_session
from app.models.ws import ResponseWebsocket
from app.services.websocket_manager import ManagerWebsocket


async def end_game_job(
        game_id: int
):
    """
    Конец игры
    :return:
    """

    session = await get_session()
    repo = RequestRepo(session)
    try:

        game = await repo.game.get_game(game_id)
        player_winner: PlayerGame = random.choice(game.players)
        game.winner_id = player_winner.id
        game.is_finish = True
        total_amount = game.get_amount_total_game()
        transaction = TransactionUser(
            amount=total_amount,
            user_id=player_winner.user_id,
            type=TransactionType.WIN
        )
        repo.session.add(game)
        repo.session.add(transaction)

        await repo.session.commit()

        await ManagerWebsocket.send_message(
            message=ResponseWebsocket(
                status='ok',
                type='winner',
                data={
                    'game': {
                        'id': game.id,
                        'end_date': game.end_date.timestamp()
                    },
                    'total_win': total_amount,
                    'winner_player': {
                        'id': player_winner.user_id,
                        'name': player_winner.user.full_name
                    }
                }
            ).dict()
        )

    except Exception as e:
        logging.exception(e)
    finally:
        await repo.close()
