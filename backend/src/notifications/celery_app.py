from celery import Celery

from src.config import get_settings

settings = get_settings()

celery = Celery(
    "incident_ops",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["src.notifications.tasks"],
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    # SLA check runs every 5 minutes
    beat_schedule={
        "check-sla-breaches": {
            "task": "src.notifications.tasks.check_sla_breaches",
            "schedule": 300.0,  # every 5 min
        }
    },
)
