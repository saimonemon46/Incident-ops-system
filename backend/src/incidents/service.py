from uuid import UUID
from typing import List

from sqlalchemy.orm import Session

from src.entities.incident import Incident
from src.incidents.models import IncidentCreate, IncidentUpdate
from src.exceptions import IncidentNotFound


def create_incident(db: Session, data: IncidentCreate) -> Incident:
    incident = Incident(**data.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


def get_all_incidents(db: Session, skip: int = 0, limit: int = 50) -> List[Incident]:
    return db.query(Incident).order_by(Incident.created_at.desc()).offset(skip).limit(limit).all()


def get_incident_by_id(db: Session, incident_id: UUID) -> Incident:
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise IncidentNotFound(incident_id)
    return incident


def update_incident(db: Session, incident_id: UUID, data: IncidentUpdate) -> Incident:
    incident = get_incident_by_id(db, incident_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(incident, field, value)
    db.commit()
    db.refresh(incident)
    return incident