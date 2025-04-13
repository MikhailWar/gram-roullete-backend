import typing

from sqlalchemy import select

from app.database.repo.base import BaseRepo
from app.database.schemas.game import Game


class GameRepo(BaseRepo):


    async def get_game(self, game_id) -> Game:

        stmt = select(
            Game
        ).where(
            Game.id == game_id
        )
        response = await self.session.execute(stmt)
        return response.scalar()

    async def get_current_game(self) -> typing.Optional[Game]:

        stmt = select(
            Game
        ).where(
            Game.is_finish.is_(False)
        )

        response = await self.session.execute(stmt)

        return response.scalar()

