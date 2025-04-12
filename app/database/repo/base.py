from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def close(self):
        await self.session.close()
