from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database.core import get_db
from src.incidents import models, service

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.post("/", response_model=models.IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(incident: models.IncidentCreate, db: Session = Depends(get_db)):
    return service.create_incident(db=db, incident_data=incident)

@router.get("/", response_model=List[models.IncidentResponse])
def read_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_incidents(db, skip=skip, limit=limit)

@router.get("/{incident_id}", response_model=models.IncidentResponse)
def read_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = service.get_incident_by_id(db, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.patch("/{incident_id}", response_model=models.IncidentResponse)
def update_incident(incident_id: int, incident_update: models.IncidentUpdate, db: Session = Depends(get_db)):
    updated_incident = service.update_incident(db, incident_id, incident_update)
    if not updated_incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return updated_incident