from pydantic import BaseModel


class Response(BaseModel):
    code: int = 200
    msg: str = ""


class BoolResponse(Response):
    data: bool


class IntResponse(Response):
    data: int
