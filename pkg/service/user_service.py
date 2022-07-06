import datetime

from fastapi import Request

import pkg.dao.user as dao_user
from pkg import codes
from pkg import constant
from pkg.codes import code
from pkg.dao import redis
from pkg.help.user_helper import UserHelper
from pkg.mq import rabbitmq
from pkg.response import JsonResponse
from pkg.routers.router import v1
from pkg.schemas.user import *
from pkg.utils.jwt_util import get_token


@v1.post("/login", response_model=LoginResponse)
def login(info: RequestLogin):
    u = UserHelper.fetch_user_by_name(info.username)
    if u is None:
        return LoginResponse(code=codes.REQUEST_ERROR)

    check_pwd = u.check_password(info.password)
    today_wrong_key = f"{u.uuid}|{datetime.date.today()}"
    today_wrong = redis.client.get(today_wrong_key)
    if (today_wrong if today_wrong else 0) > constant.user.UserWrongPWDMaxOneDay:
        return LoginResponse(code=codes.REQUEST_PARAM_ERROR)
    if check_pwd and u.is_normal():
        payload = {"username": u.username, "uuid": u.uuid}
        token = get_token(payload, px=constant.user.UserTokenDuration)
        refresh_token = get_token(payload, px=constant.user.UserTokenDuration * 2)

        redis.client.delete(today_wrong_key)
        # token_duration = constant.user.UserTokenLongDuration if info.keep_login else constant.user.UserTokenDuration
        # redis.client.set(token, uuid, px=token_duration)
        # redis.client.set(refresh_token, uuid, px=token_duration) if not info.keep_login else None

        response = JsonResponse(LoginResponse(data=u.to_dict()).dict())
        response.set_cookie("X-TOKEN", token)
        response.set_cookie("X-TOKEN-REFRESH", refresh_token)
        return response
    else:
        redis.client.incr(f"{u.uuid}|{datetime.date.today()}")
        return LoginResponse(code=codes.REQUEST_PARAM_ERROR).dict()


@v1.post("/logout", response_model=BoolResponse)
def logout():
    token = Request.cookies.getter("X-TOKEN")
    refresh_token = Request.cookies.getter("X-TOKEN-REFRESH")
    redis.client.delete(token)
    return BoolResponse(True).dict()


@v1.post("/register", response_model=BoolResponse)
def register(info: RequestRegister):
    res = False
    u = UserHelper.fetch_user_by_name(info.username)
    if u is not None:
        return BoolResponse(code=code.REQUEST_PARAM_ERROR, data=res).dict()
    u = dao_user.create_user(info)
    if u is None:
        return BoolResponse(code=code.INTERNAL_SERVICE_ERROR, data=res).dict()
    res = True
    return BoolResponse(data=res).dict()


@v1.post("/user_cancel", response_model=BoolResponse)
def user_cancel(info: RequestUserCancel):
    return BoolResponse(data=True).dict()


@v1.get("/verification_code", response_model=BoolResponse)
def verification_code(info: RequestVerificationCode):
    rabbitmq.client.publish_msg("user-service-producer", "", info.json())
    return BoolResponse(data=True).dict()
