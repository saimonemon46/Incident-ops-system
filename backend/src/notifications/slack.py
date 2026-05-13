import os
import httpx
from entities.incident import Severity

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

SEVERITY_EMOJI = {
    Severity.CRITICAL: "🔴",
    Severity.HIGH: "🟠",
    Severity.MEDIUM: "🟡",
    Severity.LOW: "🟢",
}


def send_slack_alert(
    incident_id: int,
    title: str,
    severity: str,
    category: str,
    suggested_fix: str,
    assigned_to: str | None,
) -> bool:
    if not SLACK_WEBHOOK_URL:
        print("[Slack] No webhook URL configured. Skipping.")
        return False

    emoji = SEVERITY_EMOJI.get(severity, "⚪")
    assignee = assigned_to or "Unassigned"

    payload = {
        "text": f"{emoji} *INCIDENT ALERT* {emoji}",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} Incident #{incident_id} — {severity}",
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
        response = httpx.post(SLACK_WEBHOOK_URL, json=payload, timeout=5.0)
        return response.status_code == 200
    except Exception as e:
        print(f"[Slack] Failed to send alert: {e}")
        return False


def send_slack_sla_breach(incident_id: int, title: str, severity: str) -> bool:
    if not SLACK_WEBHOOK_URL:
        return False

    payload = {
        "text": f"🚨 *SLA BREACHED* — Incident #{incident_id} ({severity}): {title}\nNo update received in time. Escalating now."
    }

    try:
        response = httpx.post(SLACK_WEBHOOK_URL, json=payload, timeout=5.0)
        return response.status_code == 200
    except Exception as e:
        print(f"[Slack] SLA breach alert failed: {e}")
        return False