def test_incident_routes_require_authentication(client):
    response = client.get("/api/v1/incidents/")

    assert response.status_code == 401


def test_authenticated_user_can_create_list_get_and_update_incident(client, auth_headers, monkeypatch):
    calls = []
    monkeypatch.setattr("src.incidents.service.notify_incident.delay", lambda **kwargs: calls.append(kwargs))

    create = client.post(
        "/api/v1/incidents/",
        headers=auth_headers,
        json={
            "title": "Database pool exhausted",
            "description": "API requests are timing out because the database connection pool is full.",
            "severity": "HIGH",
            "assigned_to": "oncall",
        },
    )
    assert create.status_code == 201
    incident = create.json()
    assert incident["status"] == "OPEN"
    assert incident["severity"] == "HIGH"
    assert len(calls) == 1

    listed = client.get("/api/v1/incidents/", headers=auth_headers)
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [incident["id"]]

    fetched = client.get(f"/api/v1/incidents/{incident['id']}", headers=auth_headers)
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Database pool exhausted"

    updated = client.patch(
        f"/api/v1/incidents/{incident['id']}",
        headers=auth_headers,
        json={"status": "IN_PROGRESS", "assigned_to": "database-team"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "IN_PROGRESS"
    assert updated.json()["assigned_to"] == "database-team"


def test_get_missing_incident_returns_404(client, auth_headers):
    missing_id = "11111111-1111-4111-8111-111111111111"

    response = client.get(f"/api/v1/incidents/{missing_id}", headers=auth_headers)

    assert response.status_code == 404
    assert missing_id in response.json()["detail"]
