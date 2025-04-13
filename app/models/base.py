from pydantic import BaseModel


class Response(BaseModel):
    success: bool



class ResponseMessage(BaseModel):
    message: str
