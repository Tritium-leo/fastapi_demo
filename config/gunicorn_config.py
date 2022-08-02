import multiprocessing
from pathlib import Path
from root import PROJECT_ROOT_PATH

debug = True

daemon = True

bind = "0.0.0.0:8080"

timeout = 30

worker_class = 'uvicorn.user_tasks.UvicornWorker'
# worker_class = 'uvicorn.user_tasks.UvicornH11Worker'

workers = multiprocessing.cpu_count() * 2 + 1
worker_connections = 2000  # 最大客户端并发数量，默认情况下这个值为1000。
threads = 2

chdir = './cmd_'
RUN_PATH = Path(f"{PROJECT_ROOT_PATH}/run/gunicorn")
LOG_PATH = RUN_PATH.joinpath("log")
RUN_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH.mkdir(parents=True, exist_ok=True)

pidfile = f'{RUN_PATH}/gunicorn.pid'
# log -----
asscesslog = f"{LOG_PATH}/access.log"
errorlog = f"{LOG_PATH}/error.log"

loglevel = 'info'  # 设置日志记录水平
logconfig_dict = {
    'formatters': {
        "generic": {
            "format": "%(process)d %(asctime)s %(levelname)s %(message)s",  # 打日志的格式
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",  # 时间显示方法
            "class": "logging.Formatter"
        }
    }
}
