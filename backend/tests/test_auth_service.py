import pytest
from fastapi import HTTPException

from src.auth import create_access_token, decode_token, verify_password
from src.entities.user import UserRole
from src.users.models import UserCreate
from src.users.service import authenticate_user, register_user


def user_payload(**overrides):
    data = {
        "email": "engineer@example.com",
        "username": "engineer",
        "password": "very-secure-password",
        "role": UserRole.ENGINEER,
    }
    data.update(overrides)
    return UserCreate(**data)


def test_register_user_hashes_password_and_persists_role(db_session):
    user = register_user(db_session, user_payload(role=UserRole.ADMIN))

    assert user.id is not None
    assert user.email == "engineer@example.com"
    assert user.role == UserRole.ADMIN
    assert user.hashed_password != "very-secure-password"
    assert verify_password("very-secure-password", user.hashed_password)


def test_register_user_rejects_duplicate_email(db_session):
    register_user(db_session, user_payload())

    with pytest.raises(HTTPException) as exc:
        register_user(db_session, user_payload(username="different"))

    assert exc.value.status_code == 409
    assert "already registered" in exc.value.detail


def test_authenticate_user_rejects_wrong_password(db_session):
    register_user(db_session, user_payload())

    with pytest.raises(HTTPException) as exc:
        authenticate_user(db_session, "engineer@example.com", "wrong-password")

    assert exc.value.status_code == 401


def test_access_token_round_trip_contains_subject():
    token = create_access_token({"sub": "engineer@example.com"})

    assert decode_token(token)["sub"] == "engineer@example.com"
