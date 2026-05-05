from sqlalchemy.orm import Session
from src.entities.incident import Incident
from src.incidents.models import IncidentCreate, IncidentUpdate

def create_incident(db: Session, incident_data: IncidentCreate):
    db_incident = Incident(**incident_data.model_dump())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

def get_incidents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Incident).offset(skip).limit(limit).all()

def get_incident_by_id(db: Session, incident_id: int):
    return db.query(Incident).filter(Incident.id == incident_id).first()

def update_incident(db: Session, incident_id: int, update_data: IncidentUpdate):
    db_incident = get_incident_by_id(db, incident_id)
    if not db_incident:
        return None
    
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_incident, key, value)
        
    db.commit()
    db.refresh(db_incident)
    return db_incident