import datetime
import typing

from pydantic import BaseModel


class Player(BaseModel):
    id: int
    name: str
    amount: int



class CurrentGame(BaseModel):
    id: int
    end_date: datetime.datetime
    players: typing.List[Player]
