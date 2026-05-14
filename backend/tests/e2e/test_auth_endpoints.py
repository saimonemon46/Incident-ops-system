def test_register_returns_token_and_public_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "very-secure-password",
            "role": "MANAGER",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"
    assert body["user"]["email"] == "new@example.com"
    assert body["user"]["role"] == "MANAGER"
    assert "hashed_password" not in body["user"]


def test_login_and_me_return_authenticated_profile(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "me@example.com",
            "username": "meuser",
            "password": "very-secure-password",
            "role": "ENGINEER",
        },
    )

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "me@example.com", "password": "very-secure-password"},
    )
    assert login.status_code == 200

    me = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {login.json()['access_token']}"},
    )

    assert me.status_code == 200
    assert me.json()["email"] == "me@example.com"


def test_register_duplicate_email_returns_conflict(client):
    payload = {
        "email": "dupe@example.com",
        "username": "dupeuser",
        "password": "very-secure-password",
        "role": "ENGINEER",
    }

    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    payload["username"] = "anotheruser"
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 409
    assert "already registered" in response.json()["detail"]
