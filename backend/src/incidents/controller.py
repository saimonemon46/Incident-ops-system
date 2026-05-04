from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.core import get_db
from src.incidents.models import IncidentRead, IncidentCreate, IncidentUpdate
from src.incidents.service import IncidentService

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("/", response_model=list[IncidentRead])
def list_incidents(db: Session = Depends(get_db)):
    return IncidentService.get_all(db)

@router.post("/", response_model=IncidentRead)
def report_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    return IncidentService.create(db, incident)

@router.patch("/{incident_id}", response_model=IncidentRead)
def update_incident(incident_id: int, updates: IncidentUpdate, db: Session = Depends(get_db)):
    incident = IncidentService.update(db, incident_id, updates)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident