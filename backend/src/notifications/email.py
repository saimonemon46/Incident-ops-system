from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.config import get_settings

settings = get_settings()


def send_email_alert(
    to_email: str,
    incident_id: str,
    title: str,
    severity: str,
    suggested_fix: str,
) -> bool:
    if not settings.sendgrid_api_key:
        print("[Email] No SendGrid key configured. Skipping.")
        return False

    subject = f"[{severity}] Incident #{incident_id}: {title}"
    body = f"""
    <h2>Incident Alert - #{incident_id}</h2>
    <p><strong>Title:</strong> {title}</p>
    <p><strong>Severity:</strong> {severity}</p>
    <p><strong>Suggested Fix:</strong> {suggested_fix or 'Under investigation'}</p>
    <br>
    <p>SLA timer has started. Please respond immediately.</p>
    """

    message = Mail(
        from_email=settings.sendgrid_from_email,
        to_emails=to_email,
        subject=subject,
        html_content=body,
    )

    try:
        sg = SendGridAPIClient(settings.sendgrid_api_key)
        sg.send(message)
        return True
    except Exception as exc:
        print(f"[Email] Failed to send: {exc}")
        return False


def send_email_sla_breach(to_email: str, incident_id: str, title: str) -> bool:
    if not settings.sendgrid_api_key:
        return False

    message = Mail(
        from_email=settings.sendgrid_from_email,
        to_emails=to_email,
        subject=f"SLA BREACHED - Incident #{incident_id}",
        html_content=(
            f"<h2>SLA Breached</h2>"
            f"<p>Incident #{incident_id}: {title} has exceeded SLA. Escalating.</p>"
        ),
    )

    try:
        sg = SendGridAPIClient(settings.sendgrid_api_key)
        sg.send(message)
        return True
    except Exception as exc:
        print(f"[Email] SLA breach email failed: {exc}")
        return False
