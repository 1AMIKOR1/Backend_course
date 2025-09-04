from celery import Celery
from celery.schedules import crontab

from src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.celery_tasks",
    ]
)
celery_instance.conf.beat_schedule = {
    "run-every-five-seconds": {
        "task": "booking_today_chekin",
        "schedule": 5,
    }
}