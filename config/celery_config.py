#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from pathlib import Path

from root import PROJECT_ROOT_PATH

broker_url = 'amqp://guest:guest@localhost:5672/'
result_backend = 'redis://:000415@localhost:6379/10'

# 默认celery与broker的连接池连接数
broker_pool_limit = 10

task_acks_late = True
task_ignore_result = False
worker_disable_rate_limits = False
broker_transport_options = {'visibility_timeout': 86400}
worker_max_memory_per_child = 600
worker_max_tasks_per_child = 1
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = False
timezone = 'Asia/Shanghai'

RUN_PATH = Path(f"{PROJECT_ROOT_PATH}/run/celery")
LOG_PATH = RUN_PATH.joinpath("log")
RUN_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH.mkdir(parents=True, exist_ok=True)

CELERYD_LOG_FILE = f"{LOG_PATH}/%n%I.log"
CELERYD_PID_FILE = f"{RUN_PATH}/%n.pid"

# 配置队列
task_queues = {
    # Queue('default', Exchange('default'), routing_key='default'),
    # Queue('spider_001', Exchange('spider_001'), routing_key='spider_001'),
    # Queue('spider_002', Exchange('spider_002'), routing_key='spider_002'),
    # Queue('spider_003', Exchange('spider_003'), routing_key='spider_003'),
}

# 队列路由
task_routes = {
    # 'spider_name.tasks.daily_spider_001': {'queue': 'spider_001', 'routing_key': 'spider_001'},
    # 'spider_name.tasks.daily_spider_002': {'queue': 'spider_002', 'routing_key': 'spider_002'},
    # 'spider_name.tasks.daily_spider_003': {'queue': 'spider_003', 'routing_key': 'spider_003'}
}

imports = (
    "pkg.celery.user_tasks.tasks",

)
