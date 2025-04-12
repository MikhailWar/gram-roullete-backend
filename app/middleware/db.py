from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.database.repo.request import RequestRepo
from app.database.schemas.user import User
from app.database.session import get_session, db_repo


async def db_session_middleware(
        request: Request,
        call_next
):
    session: AsyncSession = await get_session()
    repo = RequestRepo(session)
    token_repo = db_repo.set(repo)
    try:
        return await call_next(request)
    finally:
        db_repo.reset(token_repo)
        await repo.close()

