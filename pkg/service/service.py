import redis
from sqlalchemy.orm import Session
from fastapi import FastAPI
import pika

from typing import *

class Service:
    app: FastAPI
    dao: Session
    cache: redis.Redis
    mq: Dict

    def __init__(self, app, dao, cache,mqcli):
        self.app = app
        self.dao = dao
        self.cache =cache
        self.mq = mqcli


    def start(self):
        # dingshi renwu

        # MQ consumer

        # MQ producer
        pass

