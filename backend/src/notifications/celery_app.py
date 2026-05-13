import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "incident_ops",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["notifications.tasks"],
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
            "task": "notifications.tasks.check_sla_breaches",
            "schedule": 300.0,  # every 5 min
        }
    },
)