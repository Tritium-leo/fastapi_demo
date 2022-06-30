from pkg.routers.router import v1, v2
from pkg.request.user import *
from pkg.model.base import *
from pkg.help.user_helper import UserHelper


@v1.get("/")
def v1_index():
    return {"msg": "hello v1"}


@v1.post("/login")
def login(info: RequestLogin):
    return SuccessResponse(info.dict()).dict()


@v1.post("/register")
def register(info: RequestRegister):
    u = UserHelper.get_user_by_name(info.username)

    return SuccessResponse(data=info.dict()).dict()


@v1.post("/user_cancel")
def user_cancel(info: RequestUserCancel):
    return SuccessResponse(info.dict()).dict()


@v1.get("/verification_code")
def verification_code(info: RequestVerificationCode):
    return SuccessResponse(info.dict()).dict()
