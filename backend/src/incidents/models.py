from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

from src.entities.incident import Severity, Status


class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, examples=["Payment gateway down"])
    description: str = Field(..., min_length=10, examples=["Users cannot complete payment. Money deducted but order not placed."])
    severity: Severity = Severity.LOW
    assigned_to: Optional[str] = Field(None, examples=["rahim"])


class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    severity: Optional[Severity] = None
    status: Optional[Status] = None
    assigned_to: Optional[str] = None


class IncidentResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    severity: Severity
    status: Status
    assigned_to: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}