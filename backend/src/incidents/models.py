from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class IncidentBase(BaseModel):
    title: str
    description: str
    service: str
    severity: str = Field(..., pattern="^(P1|P2|P3|P4)$")
    status: Optional[str] = "open"
    assignee: Optional[str] = None

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    status: Optional[str] = None
    assignee: Optional[str] = None

class IncidentRead(IncidentBase):
    id: int
    created_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True