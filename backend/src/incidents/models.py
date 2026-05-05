from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from src.entities.incident import SeverityEnum, StatusEnum

# What the user sends us
class IncidentCreate(BaseModel):
    title: str = Field(..., example="Payment Gateway Timeout")
    description: str = Field(..., example="User money deducted but order not placed.")
    severity: SeverityEnum = SeverityEnum.MEDIUM

# What we send back to the user
class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: SeverityEnum
    status: StatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# What engineers use to update status
class IncidentUpdate(BaseModel):
    status: Optional[StatusEnum] = None
    severity: Optional[SeverityEnum] = None