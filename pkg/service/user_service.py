import datetime

from fastapi import Request

import pkg.dao.user as dao_user
from pkg import codes
from pkg import constant
from pkg.celery.user_tasks.tasks import send_email
from pkg.codes import code
from pkg.dao import redis
from pkg.help.user_helper import UserHelper
from pkg.model.user import User
from pkg.mq import rabbitmq
from pkg.response import JsonResponse
from pkg.routers.router import v1
from pkg.schemas.user import *


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
        with redis.client.get_cli() as cli:
            cli.delete(today_wrong_key)
        response = JsonResponse()
        response = UserHelper.set_token(payload, response)
        return response
    else:
        with redis.client.get_cli() as cli:
            cli.incr(f"{u.uuid}|{datetime.date.today()}")
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
    if not User.check_username(info.username):
        return BoolResponse(code=code.REQUEST_PARAM_ERROR, data=res, msg="USERNAME INVALID").dict()
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
    # test rabbitmq
    rabbitmq.client.publish_msg("user-service-producer", "", info.json())
    # test celery
    send_email.apply_async(args=[info.email, ])
    return BoolResponse(data=True).dict()
