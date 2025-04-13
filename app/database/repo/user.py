import datetime

from aiogram.utils.web_app import WebAppUser
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert

from app.database.repo.base import BaseRepo
from app.database.schemas.user import SessionUser, User, TransactionUser
from app.services.token import generate_token
from app.services.webapp import verify_token


class UserRepo(BaseRepo):
    async def get_session(self, token: str) -> SessionUser:
        stmt = select(
            SessionUser
        ).where(
            SessionUser.token == token
        )
        response = await self.session.execute(stmt)

        return response.scalar()

    async def get_user(self, wheres: tuple) -> User:
        stmt = select(
            User
        ).where(
            *wheres
        )
        response = await self.session.execute(stmt)

        return response.scalar()

    async def create(self, user: WebAppUser) -> User:
        stmt = insert(
            User
        ).values(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            language_code=user.language_code,
            is_premium=user.is_premium
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[
                User.id
            ],
            set_=dict(
                first_name=stmt.excluded.first_name,
                last_name=stmt.excluded.last_name,
                username=stmt.excluded.username,
                language_code=stmt.excluded.language_code,
                is_premium=stmt.excluded.is_premium
            )
        ).returning(User)
        response = await self.session.execute(stmt)
        await self.session.commit()

        return response.scalar()

    async def current_session(self, user_id: int) -> SessionUser:
        stmt = select(
            SessionUser
        ).where(
            SessionUser.user_id == user_id,
            SessionUser.expiration_date >= datetime.datetime.now()
        )
        response = await self.session.execute(stmt)
        return response.scalar()

    async def generate_session(self, initdata: str) -> SessionUser:
        webapp_initdata = verify_token(init_data=initdata)
        user = await self.create(user=webapp_initdata.user)

        if not (session_user := await self.current_session(user.id)):
            session_user = SessionUser(
                user_id=user.id,
                expiration_date=datetime.datetime.now() + datetime.timedelta(days=7),
                token=generate_token()
            )
            self.session.add(session_user)
            await self.session.flush([session_user])
            await self.session.commit()

        return session_user

    async def get_balance(self, user_id: int) -> int:
        stmt = select(
            func.coalesce(
               func.sum(TransactionUser.amount), 0
            )
        ).where(
            TransactionUser.user_id == user_id
        )

        response = await self.session.execute(stmt)
        return response.scalar()