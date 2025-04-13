from pydantic import BaseModel


class ResponseWebsocket(BaseModel):
    status: str
    type: str
    data: dict
