import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "alerts@yourapp.com")


def send_email_alert(
    to_email: str,
    incident_id: int,
    title: str,
    severity: str,
    suggested_fix: str,
) -> bool:
    if not SENDGRID_API_KEY:
        print("[Email] No SendGrid key configured. Skipping.")
        return False

    subject = f"[{severity}] Incident #{incident_id}: {title}"
    body = f"""
    <h2>Incident Alert — #{incident_id}</h2>
    <p><strong>Title:</strong> {title}</p>
    <p><strong>Severity:</strong> {severity}</p>
    <p><strong>Suggested Fix:</strong> {suggested_fix or 'Under investigation'}</p>
    <br>
    <p>SLA timer has started. Please respond immediately.</p>
    """

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=body,
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return True
    except Exception as e:
        print(f"[Email] Failed to send: {e}")
        return False


def send_email_sla_breach(to_email: str, incident_id: int, title: str) -> bool:
    if not SENDGRID_API_KEY:
        return False

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=f"🚨 SLA BREACHED — Incident #{incident_id}",
        html_content=f"<h2>SLA Breached</h2><p>Incident #{incident_id}: {title} has exceeded SLA. Escalating.</p>",
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return True
    except Exception as e:
        print(f"[Email] SLA breach email failed: {e}")
        return False