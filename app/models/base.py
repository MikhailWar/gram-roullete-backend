from pydantic import BaseModel


class Response(BaseModel):
    success: bool


