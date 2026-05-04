from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from src.database.core import Base

class IncidentEntity(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primarykey=True, index=True)
    title = Column(String)
    description = Column(String)
    service = Column(String)
    status = Column(String, default="open")
    severity = Column(String)
    assignee = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime, nullable=True)