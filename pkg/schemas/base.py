from typing import *
from pydantic import *


class Response(BaseModel):
    code: int = 200
    msg: str = ""


class BoolResponse(Response):
    data: bool


class IntResponse(Response):
    data: int


class JsonResponse(Response):
    data: Dict[str, Any]
