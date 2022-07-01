import json

from pkg.routers.router import v1, v2
from pkg.help.user_helper import UserHelper
import pkg.dao.user as dao_user
from pkg.schemas.user import *
from pkg.codes import code
from pkg.mq.rabbitmq import rabbitmq_cli


@v1.post("/login", response_model=LoginRes)
def login(info: RequestLogin):
    return LoginRes(info.dict()).dict()


@v1.post("/register", response_model=BoolResponse)
def register(info: RequestRegister):
    res = False
    u = UserHelper.fetch_user_by_name(info.username)
    if u is not None:
        return BoolResponse(code=code.REQUEST_PARAM_ERROR, data=res).dict()
    u = dao_user.create_user(info)
    if u is not None:
        return BoolResponse(code=code.INTERNAL_SERVICE_ERROR, data=res).dict()
    res = True
    return BoolResponse(res).dict()


@v1.post("/user_cancel", response_model=BoolResponse)
def user_cancel(info: RequestUserCancel):
    return BoolResponse(True).dict()


@v1.get("/verification_code", response_model=BoolResponse)
def verification_code(info: RequestVerificationCode):
    rabbitmq_cli.publish_msg("user-service-producer", "", info.json())
    return BoolResponse(data=True).dict()
