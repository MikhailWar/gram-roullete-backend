from pydantic import BaseModel

from app.models.base import Response


class AuthenticateBody(BaseModel):
    init_data: str


class SuccessAuthenticate(Response):
    token: str
