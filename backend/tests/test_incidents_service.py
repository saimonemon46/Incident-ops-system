import pytest
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone

from src.entities.incident import Severity, Status
from src.incidents.models import IncidentCreate, IncidentUpdate
from src.incidents.service import (
    create_incident,
    get_all_incidents,
    get_incident_by_id,
    update_incident,
)


def incident_payload(**overrides):
    data = {
        "title": "Checkout is failing",
        "description": "Customers cannot complete payment during checkout.",
        "severity": Severity.LOW,
        "assigned_to": "rahim",
    }
    data.update(overrides)
    return IncidentCreate(**data)


def test_create_low_incident_does_not_send_notification(db_session, monkeypatch):
    calls = []
    monkeypatch.setattr("src.incidents.service.notify_incident.delay", lambda **kwargs: calls.append(kwargs))

    incident = create_incident(db_session, incident_payload())

    assert incident.id is not None
    assert incident.status == Status.OPEN
    assert incident.sla_deadline is None
    assert incident.notified_at is None
    assert calls == []


def test_create_high_incident_sets_sla_and_sends_notification(db_session, monkeypatch):
    calls = []
    monkeypatch.setattr("src.incidents.service.notify_incident.delay", lambda **kwargs: calls.append(kwargs))

    incident = create_incident(db_session, incident_payload(severity=Severity.HIGH))

    assert incident.sla_deadline is not None
    assert incident.notified_at is not None
    assert len(calls) == 1
    assert calls[0]["incident_id"] == str(incident.id)
    assert calls[0]["severity"] == "HIGH"
    assert calls[0]["title"] == "Checkout is failing"


def test_list_incidents_returns_newest_first(db_session, monkeypatch):
    monkeypatch.setattr("src.incidents.service.notify_incident.delay", lambda **kwargs: None)
    first = create_incident(db_session, incident_payload(title="First incident"))
    second = create_incident(db_session, incident_payload(title="Second incident"))
    first.created_at = datetime.now(timezone.utc) - timedelta(minutes=5)
    second.created_at = datetime.now(timezone.utc)
    db_session.commit()

    incidents = get_all_incidents(db_session)

    assert [incident.id for incident in incidents] == [second.id, first.id]


def test_update_incident_changes_only_provided_fields(db_session, monkeypatch):
    monkeypatch.setattr("src.incidents.service.notify_incident.delay", lambda **kwargs: None)
    incident = create_incident(db_session, incident_payload())

    updated = update_incident(
        db_session,
        incident.id,
        IncidentUpdate(status=Status.IN_PROGRESS, assigned_to="karim"),
    )

    assert updated.title == "Checkout is failing"
    assert updated.status == Status.IN_PROGRESS
    assert updated.assigned_to == "karim"


def test_get_incident_by_id_raises_for_missing_incident(db_session):
    import uuid

    missing_id = uuid.uuid4()

    with pytest.raises(HTTPException) as exc:
        get_incident_by_id(db_session, missing_id)

    assert exc.value.status_code == 404
    assert str(missing_id) in exc.value.detail
