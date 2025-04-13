import datetime
import typing

from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database.base import Base, TimeMixin


class Game(Base, TimeMixin):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_finish: Mapped[bool] = mapped_column(default=False)
    end_date: Mapped[datetime.datetime] = mapped_column(
        DateTime
    )
    winner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('game_players.id', ondelete='SET NULL'),
        nullable=True
    )
    players: Mapped[
        typing.List['PlayerGame']
    ] = relationship(
        'PlayerGame',
        primaryjoin="PlayerGame.game_id == Game.id",
        lazy='selectin'
    )

    def get_amount_total_game(
            self,
    ):
        amount = 0
        for player in self.players:
            amount += player.bet_amount

        return amount



class PlayerGame(Base, TimeMixin):
    __tablename__ = 'game_players'
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE')
    )

    bet_amount: Mapped[int] = mapped_column(
        Integer
    )

    game_id: Mapped[int] = mapped_column(
        ForeignKey('games.id', ondelete='CASCADE'),
    )

    user: Mapped['User'] = relationship(
        foreign_keys=[user_id],
        lazy='selectin'
    )
