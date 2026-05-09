from entities.incident import IncidentCategory, Severity

# keyword → (category, severity, suggested_fix)
RULES = [
    {
        "keywords": ["payment", "transaction", "money", "deducted", "charge", "billing", "refund"],
        "category": IncidentCategory.PAYMENT,
        "severity": Severity.CRITICAL,
        "suggested_fix": "Restart payment-service. Reprocess failed transactions via retry queue. Check payment gateway timeout settings.",
        "ai_notes": "Payment issues = financial impact. Escalate immediately.",
    },
    {
        "keywords": ["login", "auth", "token", "password", "unauthorized", "403", "401"],
        "category": IncidentCategory.AUTH,
        "severity": Severity.HIGH,
        "suggested_fix": "Check JWT secret rotation. Verify token expiry config. Restart auth service if needed.",
        "ai_notes": "Auth failure blocks all users. High priority.",
    },
    {
        "keywords": ["database", "db", "postgres", "sql", "connection pool", "query timeout"],
        "category": IncidentCategory.DATABASE,
        "severity": Severity.HIGH,
        "suggested_fix": "Check DB connection pool limits. Look for long-running queries. Restart DB connection pool.",
        "ai_notes": "DB issues cascade fast. Check pool exhaustion first.",
    },
    {
        "keywords": ["slow", "timeout", "latency", "response time", "lag", "hanging"],
        "category": IncidentCategory.PERFORMANCE,
        "severity": Severity.MEDIUM,
        "suggested_fix": "Profile slow endpoints. Check CPU/memory. Look for N+1 queries.",
        "ai_notes": "Performance degradation — not critical unless SLA breached.",
    },
    {
        "keywords": ["network", "dns", "connection refused", "unreachable", "502", "503", "gateway"],
        "category": IncidentCategory.NETWORK,
        "severity": Severity.HIGH,
        "suggested_fix": "Check upstream service health. Verify DNS resolution. Inspect load balancer logs.",
        "ai_notes": "Network issue — may be external dependency failure.",
    },
]

FALLBACK = {
    "category": IncidentCategory.UNKNOWN,
    "severity": Severity.MEDIUM,
    "suggested_fix": "No known fix pattern. Assign to on-call engineer for manual investigation.",
    "ai_notes": "No rule matched. Classified as UNKNOWN.",
}


def run_rules(title: str, description: str) -> dict:
    text = f"{title} {description}".lower()

    for rule in RULES:
        for keyword in rule["keywords"]:
            if keyword in text:
                return {
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "suggested_fix": rule["suggested_fix"],
                    "ai_notes": rule["ai_notes"],
                    "confidence": 0.75,  # rule match = decent confidence
                    "matched_by": "rule_engine",
                }

    return {**FALLBACK, "confidence": 0.3, "matched_by": "fallback"}