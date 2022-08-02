import time

from celery.utils.log import get_task_logger

from cmd_.celery.main import app

logger = get_task_logger(__name__)


@app.task(bind=True)
def send_email(self, email: str) -> bool:
    try:
        # smtp to
        logger.info(email)
        time.sleep(1)

        logger.info(f"SUCCESSFUL! SEND_EMAIL TO {email}")
    except Exception as e:
        """
                邮件发送失败，使用retry进行重试

                retry的参数可以有：
                    exc：指定抛出的异常
                    throw：重试时是否通知worker是重试任务
                    eta：指定重试的时间／日期
                    countdown：在多久之后重试（每多少秒重试一次）
                    max_retries：最大重试次数
        """
        raise self.retry(exc=e, args=(email, ), countdown=3, max_retries=5)
    return True


@app.task
def send_node(phone: str) -> bool:
    logger.info(phone)
    time.sleep(1)
    return True
