from pydantic import BaseModel


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
