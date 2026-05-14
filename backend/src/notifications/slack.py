import httpx

from src.config import get_settings
from src.entities.incident import Severity

settings = get_settings()

SEVERITY_LABEL = {
    Severity.CRITICAL.value: "[CRITICAL]",
    Severity.HIGH.value: "[HIGH]",
    Severity.MEDIUM.value: "[MEDIUM]",
    Severity.LOW.value: "[LOW]",
}


def send_slack_alert(
    incident_id: str,
    title: str,
    severity: str,
    category: str,
    suggested_fix: str,
    assigned_to: str | None,
) -> bool:
    if not settings.slack_webhook_url:
        print("[Slack] No webhook URL configured. Skipping.")
        return False

    severity_label = SEVERITY_LABEL.get(severity, "[UNKNOWN]")
    assignee = assigned_to or "Unassigned"

    payload = {
        "text": f"{severity_label} INCIDENT ALERT",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{severity_label} Incident #{incident_id}",
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Title:*\n{title}"},
                    {"type": "mrkdwn", "text": f"*Category:*\n{category}"},
                    {"type": "mrkdwn", "text": f"*Severity:*\n{severity}"},
                    {"type": "mrkdwn", "text": f"*Assigned To:*\n{assignee}"},
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Suggested Fix:*\n{suggested_fix or 'Under investigation'}",
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Please look into this immediately. SLA timer has started.",
                    }
                ],
            },
        ],
    }

    try:
        response = httpx.post(settings.slack_webhook_url, json=payload, timeout=5.0)
        return response.status_code == 200
    except Exception as exc:
        print(f"[Slack] Failed to send alert: {exc}")
        return False


def send_slack_sla_breach(incident_id: str, title: str, severity: str) -> bool:
    if not settings.slack_webhook_url:
        return False

    payload = {
        "text": (
            f"[SLA BREACHED] Incident #{incident_id} ({severity}): {title}\n"
            "No update received in time. Escalating now."
        )
    }

    try:
        response = httpx.post(settings.slack_webhook_url, json=payload, timeout=5.0)
        return response.status_code == 200
    except Exception as exc:
        print(f"[Slack] SLA breach alert failed: {exc}")
        return False
