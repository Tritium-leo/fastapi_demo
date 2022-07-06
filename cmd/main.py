import enum
import os
import time

import snowflake.client
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel

from config import model as config_model
from pkg.dao import redis, db
from pkg.middlewares import ErrorMiddleware
from pkg.mq import consumers
from pkg.mq import rabbitmq
from pkg.routers import router
from root import PROJECT_ROOT_PATH

# logger
logger.remove(handler_id=None)
logger.add(
    f"{PROJECT_ROOT_PATH}/log/fastapi_demo_{str(int(time.time()))[:-5] + '0' * 5}.log",
    colorize=False,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
    rotation="1 day",
    retention="10 days",
    compression="zip",
    catch=True,
    enqueue=True
)


class EnvEnum(enum.Enum):
    Dev = 'dev'
    Prev = 'prev'
    Prod = 'prod'


class AppConfig(BaseModel):
    env: EnvEnum = 'dev'
    version: str
    machine_id: str
    sso_center: str
    # 分布式id
    snowflake_host: str
    snowflake_port: int

    def is_dev(self) -> bool:
        return self.env == EnvEnum.Dev.value

    def is_prev(self) -> bool:
        return self.env == EnvEnum.Prev.value

    def is_prod(self) -> bool:
        return self.env == EnvEnum.Prod.value


def init_app():
    config = config_model.Config.load_dir(f"{PROJECT_ROOT_PATH}/config/file/default.yaml",
                                          os.environ.get("APP.CONFIG_PATH",
                                                         f"{PROJECT_ROOT_PATH}/config/file/local.yaml"))
    app_conf = config.struct_map('app', AppConfig)
    # connect to snowflake server
    snowflake.client.setup(app_conf.snowflake_host, app_conf.snowflake_port)
    # init main db
    db.init_db(config.struct_map('db', db.DBConfig))
    # init redis
    redis.init_redis(config.struct_map("redis", redis.RedisConfig))

    # mq register
    rabbitmq.init_rabbitmq(config.struct_map("rabbitmq", rabbitmq.RabbitMQConfig))
    # producer
    rabbitmq.client.new_producer("user-service-producer")
    # mq init consumer
    consumers.init()
    rabbitmq.client.start()

    # -------app ---
    # docs show?
    if app_conf.is_dev():
        app = FastAPI(title="fast_api_demo", version=app_conf.version, debug=True)
    else:
        app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.include_router(router.v1)
    app.include_router(router.v2)
    # logger
    # registry middleware
    # 关闭跨域限制
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ErrorMiddleware)
    return app


app = init_app()


@app.on_event("startup")
def start_event():
    logger.info("data hot load")


@app.on_event("shutdown")
def shut_down_event():
    logger.info("before close app")

    # db close
    # from pkg.dao.mysql import Session
    # Session.close_all()

    # redis close
    redis.client.close()
    logger.info("redis closed")

    # mq close
    rabbitmq.client.close()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8070)

# else:
#     gunicorn_logger = logging.getLogger("gunicorn.error")
#     app.logger.handlers = gunicorn_logger.handlers
