import os
import time
import signal

from config.init import load_file, config
from config.app_config import AppConfig
from root import PROJECT_ROOT_PATH

load_file(f"{PROJECT_ROOT_PATH}/config/file/default.yaml", f"{PROJECT_ROOT_PATH}/config/file/local.yaml",
          os.environ.get("CONFIG_PATH"))

import uvicorn
import snowflake.client
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pkg.routers import router
from pkg.mq.rabbitmq import rabbitmq_cli
import pkg.mq.consumers


def init_app():
    # connect to snowflake server
    snowflake.client.setup("0.0.0.0", "8910")
    # conf
    app_conf = AppConfig(**config['app'])
    # docs show?
    if app_conf.is_dev():
        app = FastAPI(title="fast_api_demo", version=app_conf.version, debug=True)
    else:
        app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.include_router(router.v1)
    app.include_router(router.v2)
    # 关闭跨域限制
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # mq register
    rabbitmq_cli.new_producer("user-service-producer")
    rabbitmq_cli.start()
    return app


app = init_app()


@app.on_event("startup")
def start_event():
    print("data hot load")


@app.on_event("shutdown")
def shut_down_event():
    print("before close app")
    # db close
    # from pkg.dao.mysql import Session
    # Session.close_all()

    # redis close
    from pkg.dao.redis import redis_cli
    redis_cli.close()
    print("redis closed")

    # mq close
    from pkg.mq.rabbitmq import rabbitmq_cli
    rabbitmq_cli.close()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8070)

# else:
#     gunicorn_logger = logging.getLogger("gunicorn.error")
#     app.logger.handlers = gunicorn_logger.handlers
