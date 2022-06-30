from typing import *
from pydantic import BaseModel


class Response(BaseModel):
    code: int
    data: Dict[str, Any]
    msg: str


# class ErrorResponse(Response):
#     data = {"":""}


class SuccessResponse(Response):
    code = 200
    msg = ""
