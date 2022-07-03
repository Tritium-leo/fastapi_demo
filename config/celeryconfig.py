#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals
from kombu import Queue, Exchange
from celery.schedules import crontab

BROKER_URL = 'amqp://spider:****@IP:端口/yimian'

# 默认celery与broker的连接池连接数
BROKER_POOL_LIMIT = 10

CELERY_ACKS_LATE = True
CELERY_IGNORE_RESULT = True
CELERY_DISABLE_RATE_LIMITS = True
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 86400}
WORKER_MAX_MEMORY_PER_CHILD = 600
CELERYD_MAX_TASKS_PER_CHILD = 1
CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Shanghai'
TIME_ZONE = 'Asia/Shanghai'

# 配置队列
CELERY_QUEUES = {
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('spider_001', Exchange('spider_001'), routing_key='spider_001'),
    Queue('spider_002', Exchange('spider_002'), routing_key='spider_002'),
    Queue('spider_003', Exchange('spider_003'), routing_key='spider_003'),
}

# 队列路由
CELERY_ROUTES = {
    'spider_name.tasks.daily_spider_001': {'queue': 'spider_001', 'routing_key': 'spider_001'},
    'spider_name.tasks.daily_spider_002': {'queue': 'spider_002', 'routing_key': 'spider_002'},
    'spider_name.tasks.daily_spider_003': {'queue': 'spider_003', 'routing_key': 'spider_003'}
}
