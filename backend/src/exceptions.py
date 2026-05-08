from uuid import UUID
from fastapi import HTTPException


# ── Incident ──────────────────────────────────────────────────────────────────

class IncidentNotFound(HTTPException):
    def __init__(self, incident_id: UUID):
        super().__init__(
            status_code=404,
            detail=f"Incident '{incident_id}' not found"
        )


class InvalidSeverity(HTTPException):
    def __init__(self, value: str):
        super().__init__(
            status_code=422,
            detail=f"Invalid severity value: '{value}'. Must be LOW, MEDIUM, HIGH, or CRITICAL."
        )


# ── General ───────────────────────────────────────────────────────────────────

class DatabaseError(HTTPException):
    def __init__(self, detail: str = "A database error occurred"):
        super().__init__(status_code=500, detail=detail)


# ── Auth ──────────────────────────────────────────────────────────────────────

class EmailAlreadyExists(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=409,
            detail=f"Email '{email}' is already registered"
        )


class UsernameAlreadyExists(HTTPException):
    def __init__(self, username: str):
        super().__init__(
            status_code=409,
            detail=f"Username '{username}' is already taken"
        )


class InvalidCredentials(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid email or password"
        )