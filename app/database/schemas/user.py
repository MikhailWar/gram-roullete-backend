import enum

from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from app.database.base import TimeMixin, Base


class User(Base, TimeMixin):
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        nullable=True
    )


class TransactionType(enum.Enum):
    DEPOSIT = 'пополнение'
    WITHDRAWAL = 'вывод'
    BET = 'ставка'
    WIN = 'выигрыш'





class TransactionUser(Base, TimeMixin):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    amount: Mapped[int] = mapped_column()
    type: Mapped[TransactionType] = mapped_column()



