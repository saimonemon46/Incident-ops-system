import os
from datetime import datetime, timezone
from entities.incident import Severity

SLA_MINUTES = {
    Severity.CRITICAL: int(os.getenv("SLA_CRITICAL_MINUTES", 15)),
    Severity.HIGH: int(os.getenv("SLA_HIGH_MINUTES", 60)),
    Severity.MEDIUM: 240,
    Severity.LOW: 1440,
}


def get_sla_deadline(severity: str) -> datetime:
    from datetime import timedelta
    minutes = SLA_MINUTES.get(severity, 240)
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)


def is_sla_breached(sla_deadline: datetime) -> bool:
    if sla_deadline is None:
        return False
    return datetime.now(timezone.utc) > sla_deadline