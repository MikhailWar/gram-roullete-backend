import datetime
import enum

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database.base import TimeMixin, Base


class User(Base, TimeMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    first_name: Mapped[str] = mapped_column(
        nullable=True
    )
    last_name: Mapped[str] = mapped_column(
        nullable=True
    )
    username: Mapped[str] = mapped_column(
        nullable=True
    )
    language_code: Mapped[str] = mapped_column(
        nullable=True
    )
    is_premium: Mapped[bool] = mapped_column(
        default=False, nullable=True
    )


class SessionUser(Base, TimeMixin):
    __tablename__ = "session_users"
    token: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('users.id', ondelete='CASCADE')
    )
    expiration_date: Mapped[datetime.datetime] = mapped_column()
    user: Mapped['User'] = relationship(
        foreign_keys=[user_id]
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



