import os

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from puncher import FemasPuncher

ACCOUNT = os.environ.get("ACCOUNT", "")
PASSWORD = os.environ.get("PASSWORD", "")
SUBDOMAIN = os.environ.get("SUBDOMAIN", "")
PUNCH_MINUTE = os.environ.get("PUNCH_MINUTE", "0")
PUNCH_HOUR = os.environ.get("PUNCH_HOUR", "9,19")
PUNCH_DAY_OF_WEEK = os.environ.get("PUNCH_DAY_OF_WEEK", "mon,tue,wed,thu,fri")
TIMEZONE = os.environ.get("TIMEZONE", "Asia/Taipei")

celery = Celery(__name__)
celery.conf.timezone = TIMEZONE
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL",
    "redis://redis:6379/1",
)
logger = get_task_logger(__name__)


@celery.task
def auto_punch_in_and_out():
    with FemasPuncher(
        account=ACCOUNT,
        password=PASSWORD,
        subdomain=SUBDOMAIN,
    ) as femas_puncher:

        with open("./indolent.txt") as f:
            for user_id in f:
                try:
                    femas_puncher.punch_in(user_id=user_id)
                    logger.info(f"Punch in user_id={user_id}")
                    femas_puncher.punch_out(user_id=user_id)
                    logger.info(f"Punch out user_id={user_id}")
                except Exception as e:
                    logger.info(f"Fail to punch user_id={user_id} due to {e}")


celery.conf.beat_schedule = {
    "punch-task": {
        "task": "main.auto_punch_in_and_out",
        "schedule": crontab(
            minute=PUNCH_MINUTE,
            hour=PUNCH_HOUR,
            day_of_week=PUNCH_DAY_OF_WEEK,
        ),
    }
}
