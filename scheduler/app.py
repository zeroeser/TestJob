from celery import Celery
from celery.schedules import crontab

from app.settings import settings


def crontab_string_to_celery_schedule(crontab_str: str) -> crontab:
    minute, hour, day_of_week, day_of_month, month_of_year = crontab_str.split(" ")

    return crontab(
        minute=minute,
        hour=hour,
        day_of_week=day_of_week,
        day_of_month=day_of_month,
        month_of_year=month_of_year,
    )


celery = Celery(
    "tasks",
    backend=f"redis://:"
    f"@{settings.REDIS_ADDRESS}:{settings.REDIS_PORT}/{settings.REDIS_DB_BACKEND_NUMBER}",
    broker=f"redis://:"
    f"@{settings.REDIS_ADDRESS}:{settings.REDIS_PORT}/{settings.REDIS_DB_BROKER_NUMBER}",
)

celery.autodiscover_tasks(["scheduler.tasks"])

celery.conf.beat_schedule = {
    "database_update": {
        "task": "database_update",
        "schedule": crontab_string_to_celery_schedule(settings.EXCEL_TASK_INTERVAL),
    },
}

celery.conf.timezone = settings.CELERY_TIMEZONE
celery.conf.update({"worker_hijack_root_logger": False})
