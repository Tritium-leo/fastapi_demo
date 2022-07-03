import os
import sys

from config.app_config import AppConfig
from config.init import load_file, config
from root import PROJECT_ROOT_PATH

load_file(f"{PROJECT_ROOT_PATH}/config/file/default.yaml", f"{PROJECT_ROOT_PATH}/config/file/local.yaml",
          os.environ.get("CONFIG_PATH"))

import uvicorn
import snowflake.client
from fastapi import FastAPI
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

from pkg.routers import router
from pkg.mq import rabbitmq
from pkg.mq import consumers
from pkg.dao import redis, db
from pkg.middlewares import ErrorMiddleware

logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>")


def init_app():
    # connect to snowflake server
    snowflake.client.setup(config["snowflake"]["host"], config["snowflake"]["port"])
    # init main db
    db.init_db(db.DBConfig(**config['db']))
    # init redis
    redis.init_redis(redis.RedisConfig(**config['redis']))
    # conf
    app_conf = AppConfig(**config['app'])
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

    # mq register
    rabbitmq.init_rabbitmq(rabbitmq.RabbitMQConfig(**config["rabbitmq"]))
    rabbitmq.client.new_producer("user-service-producer")
    # mq init consumer
    consumers.init()
    rabbitmq.client.start()
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
