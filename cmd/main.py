import os
import signal
from config.init import load_file
from root import PROJECT_ROOT_PATH

load_file(f"{PROJECT_ROOT_PATH}/config/file/default.yaml", f"{PROJECT_ROOT_PATH}/config/file/local.yaml", os.environ.get("CONFIG_PATH"))

import uvicorn
from fastapi import FastAPI
from pkg.routers import router
import time


def init_app():
    # init

    # start
    # service.start()

    app = FastAPI()
    app.include_router(router.v1)
    app.include_router(router.v2)

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8070)


def handler(a, b):
    print(f"Signal Number", a, "Frame", b)


signal.signal(signal.SIGINT, handler)
while True:
    time.sleep(3)

# else:
#     gunicorn_logger = logging.getLogger("gunicorn.error")
#     app.logger.handlers = gunicorn_logger.handlers
