from dataclasses import dataclass

from environs import Env
from sqlalchemy import URL, make_url

env = Env()
env.read_env('.env')


@dataclass
class DbConfig:
    user: str = env.str('DB_USER')
    password: str = env.str('DB_PASSWORD')
    host: str = env.str('DB_HOST')
    name: str = env.str('DB_NAME')


    @property
    def url(self) -> str:
        url = URL(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.name,
            query={},
            port=5432
        )
        return make_url(url)



class BotConfig:
    token: str = env.str('BOT_TOKEN')


class MiscConfig:
    debug: bool = True


@dataclass
class Config:
    db = DbConfig()
    bot = BotConfig()
    misc = MiscConfig()


