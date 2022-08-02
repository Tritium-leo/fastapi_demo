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


@v1.get("/error")
def login():
    c = 1 / 0
    return c


@v1.post("/error")
def login1():
    c = 1 / 0
    return c

