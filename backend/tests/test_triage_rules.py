from src.entities.incident import IncidentCategory, Severity
from src.triage.rules import run_rules


def test_payment_rule_classifies_financial_impact_as_critical():
    result = run_rules(
        "Payment gateway down",
        "Money was deducted but the customer order was not created.",
    )

    assert result["category"] == IncidentCategory.PAYMENT
    assert result["severity"] == Severity.CRITICAL
    assert result["confidence"] == 0.75
    assert result["matched_by"] == "rule_engine"


def test_auth_rule_matches_case_insensitive_keywords():
    result = run_rules("Users see 401", "LOGIN token refresh is failing.")

    assert result["category"] == IncidentCategory.AUTH
    assert result["severity"] == Severity.HIGH


def test_unknown_incident_uses_fallback_classification():
    result = run_rules("Profile avatar is misaligned", "The image is slightly off center.")

    assert result["category"] == IncidentCategory.UNKNOWN
    assert result["severity"] == Severity.MEDIUM
    assert result["confidence"] == 0.3
    assert result["matched_by"] == "fallback"
