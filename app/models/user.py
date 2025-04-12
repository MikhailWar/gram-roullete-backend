from pydantic import BaseModel


class AuthenticateBody(BaseModel):
    init_data: str