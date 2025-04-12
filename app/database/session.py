
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import Config
from app.database.repo.request import RequestRepo

engine: AsyncEngine = create_async_engine(
    Config.db.url, future=True, pool_pre_ping=True, echo=False
)
sessionmaker = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False
)

print(Config.db)

db_repo: ContextVar[RequestRepo] = ContextVar('db_repo')


async def get_session(_engine: AsyncEngine | None = engine):
    session = sessionmaker()
    return session
