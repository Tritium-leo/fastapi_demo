from .base import *


class UserBase(BaseModel):
    uuid: int
    username: str


class LoginRes(Response):
    data: UserBase


class RequestLogin(BaseModel):
    username: str
    password: str


class RequestRegister(BaseModel):
    username: str
    password: str


class RequestUserCancel(BaseModel):
    username: str
    password: str


class RequestVerificationCode(BaseModel):
    email: str
