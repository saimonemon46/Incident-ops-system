import uuid
import enum
from datetime import datetime

from sqlalchemy import Column, String, Text, Enum as SQLEnum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from src.database.core import Base


class Severity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Status(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"

class IncidentCategory(str, enum.Enum):
    PAYMENT = "PAYMENT"
    AUTH = "AUTH"
    DATABASE = "DATABASE"
    NETWORK = "NETWORK"
    PERFORMANCE = "PERFORMANCE"
    UNKNOWN = "UNKNOWN"

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(SQLEnum(Severity), default=Severity.LOW, nullable=False)
    status = Column(SQLEnum(Status), default=Status.OPEN, nullable=False)
    assigned_to = Column(String(100), nullable=True)

    # Phase 3 — AI triage columns
    category = Column(SQLEnum(IncidentCategory), default=IncidentCategory.UNKNOWN, nullable=True)
    suggested_fix = Column(Text, nullable=True)
    ai_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())