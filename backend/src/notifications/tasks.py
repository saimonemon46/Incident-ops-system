from src.notifications.celery_app import celery
from src.notifications.slack import send_slack_alert, send_slack_sla_breach
from src.notifications.email import send_email_alert, send_email_sla_breach
from src.notifications.sla import is_sla_breached

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@celery.task(name="notifications.tasks.notify_incident")
def notify_incident(
    incident_id: int,
    title: str,
    severity: str,
    category: str,
    suggested_fix: str,
    assigned_to: str | None,
    engineer_email: str | None,
):
    # Slack alert always
    send_slack_alert(
        incident_id=incident_id,
        title=title,
        severity=severity,
        category=category,
        suggested_fix=suggested_fix,
        assigned_to=assigned_to,
    )

    # Email only if engineer assigned + email known
    if engineer_email:
        send_email_alert(
            to_email=engineer_email,
            incident_id=incident_id,
            title=title,
            severity=severity,
            suggested_fix=suggested_fix,
        )

    print(f"[Tasks] Notifications sent for incident #{incident_id}")


@celery.task(name="notifications.tasks.check_sla_breaches")
def check_sla_breaches():
    """Runs every 5 min via celery beat. Checks all open incidents for SLA breach."""
    from database.core import SessionLocal
    from entities.incident import Incident, Status
    from datetime import datetime, timezone

    db = SessionLocal()
    try:
        open_incidents = (
            db.query(Incident)
            .filter(
                Incident.status != Status.RESOLVED,
                Incident.sla_deadline.isnot(None),
                Incident.sla_breached == False,
            )
            .all()
        )

        breached = 0
        for incident in open_incidents:
            if is_sla_breached(incident.sla_deadline):
                incident.sla_breached = True
                db.commit()

                send_slack_sla_breach(
                    incident_id=incident.id,
                    title=incident.title,
                    severity=incident.severity,
                )

                if incident.assigned_to:
                    send_email_sla_breach(
                        to_email=incident.assigned_to,
                        incident_id=incident.id,
                        title=incident.title,
                    )

                breached += 1

        print(f"[SLA Check] Checked {len(open_incidents)} incidents. Breached: {breached}")
    finally:
        db.close()