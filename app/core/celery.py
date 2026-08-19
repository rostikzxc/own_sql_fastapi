from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "app",
    broker="redis://redis:6379/0",
    include=["app.tasks.auth_tasks"]
)


celery_app.conf.beat_schedule = {
    "cleanup-expired-refresh-tokens": {
        "task": "app.tasks.auth_tasks.cleanup_expired_refresh_tokens",
        "schedule": crontab(hour=3, minute=""),
    },
}