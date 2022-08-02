# 主程序
import os

from celery import Celery

from config import model as config_model
from root import PROJECT_ROOT_PATH

config = config_model.Config.load_dir(f"{PROJECT_ROOT_PATH}/config/file/default.yaml",
                                      os.environ.get("APP.CONFIG_PATH",
                                                     f"{PROJECT_ROOT_PATH}/config/file/local.yaml"))

# 创建celery实例对象
app = Celery("fastapi_demo")

# 通过app对象加载配置
app.config_from_object("config.celery_config")

# 加载任务
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# app.autodiscover_tasks(["pkg.celery.user_tasks", ])

#
app.conf.beat_schedule = {
    # 'add-every-30-seconds': {
    #     'task': 'tasks.add',
    #     'schedule': 30.0,
    #     'args': (16, 16)
    # },
}
# 启动Celery的命令
# celery -A mycelery.main worker --loglevel=info
