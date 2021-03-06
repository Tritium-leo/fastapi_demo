import multiprocessing
from root import PROJECT_ROOT_PATH

debug = True

daemon = False

bind = "0.0.0.0:8080"

timeout = 30

worker_class = 'uvicorn.workers.UvicornWorker'
# worker_class = 'uvicorn.workers.UvicornH11Worker'

workers = multiprocessing.cpu_count() * 2 + 1
worker_connections = 2000 # 最大客户端并发数量，默认情况下这个值为1000。
loglevel = "debug"
threads = 2

chdir = './cmd'

# log -----
asscesslog = f"{PROJECT_ROOT_PATH}/log/access.log"
errorlog = f"{PROJECT_ROOT_PATH}/log/error.log"

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
