from datetime import datetime, timezone
from src.entities.incident import Severity
from src.config import get_settings

settings = get_settings()

SLA_MINUTES = {
    Severity.CRITICAL: settings.sla_critical_minutes,
    Severity.HIGH: settings.sla_high_minutes,
    Severity.MEDIUM: 240,
    Severity.LOW: 1440,
}


def get_sla_deadline(severity: Severity | str) -> datetime:
    from datetime import timedelta

    severity_key = severity if isinstance(severity, Severity) else Severity(severity)
    minutes = SLA_MINUTES.get(severity_key, 240)
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)


def is_sla_breached(sla_deadline: datetime) -> bool:
    if sla_deadline is None:
        return False
    return datetime.now(timezone.utc) > sla_deadline
