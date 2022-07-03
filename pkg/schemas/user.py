from .base import *


class UserBase(BaseModel):
    uuid: int = -1
    username: str = ""


class LoginResponse(Response):
    data: UserBase = UserBase()


class RequestLogin(BaseModel):
    username: str
    password: str
    keep_login: bool = False


class RequestRegister(BaseModel):
    username: str
    password: str


class RequestUserCancel(BaseModel):
    username: str
    password: str


class RequestVerificationCode(BaseModel):
    email: str
