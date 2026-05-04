from sqlalchemy.orm import Session
from datetime import datetime, timezone
from src.entities.incident import IncidentEntity
from src.incidents.models import IncidentCreate, IncidentUpdate

class IncidentService:
    @staticmethod
    def get_all(db: Session):
        return db.query(IncidentEntity).all()

    @staticmethod
    def create(db: Session, incident_data: IncidentCreate):
        db_incident = IncidentEntity(**incident_data.model_dump())
        db.add(db_incident)
        db.commit()
        db.refresh(db_incident)
        return db_incident

    @staticmethod
    def update(db: Session, incident_id: int, updates: IncidentUpdate):
        db_incident = db.query(IncidentEntity).filter(IncidentEntity.id == incident_id).first()
        if not db_incident:
            return None
        
        data = updates.model_dump(exclude_unset=True)
        
        # Handle auto-timestamping for resolution
        if "status" in data and data["status"] in ["resolved", "closed"]:
            db_incident.resolved_at = datetime.now(timezone.utc)
            
        for key, value in data.items():
            setattr(db_incident, key, value)
            
        db.commit()
        db.refresh(db_incident)
        return db_incident