from uuid import UUID
from fastapi import HTTPException


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


class DatabaseError(HTTPException):
    def __init__(self, detail: str = "A database error occurred"):
        super().__init__(status_code=500, detail=detail)