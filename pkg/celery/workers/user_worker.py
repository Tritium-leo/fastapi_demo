import time

from celery.utils.log import get_task_logger

from pkg.celery import app

logger = get_task_logger(__name__)


@app.task
def send_email(email: str) -> bool:
    # smtp to
    logger.info(email)
    time.sleep(1)
    return True


@app.task
def send_node(phone: str) -> bool:
    logger.info(phone)
    time.sleep(1)
    return True
