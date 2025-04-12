from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.database.base import Base, TimeMixin


class Game(Base, TimeMixin):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_finish: Mapped[bool] = mapped_column(default=False)


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

    is_win: Mapped[bool] = mapped_column(
        default=False
    )

    game_id: Mapped[int] = mapped_column(
        ForeignKey('games.id', ondelete='CASCADE')
    )



