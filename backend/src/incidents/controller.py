from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.database.core import get_db
from src.incidents.models import IncidentCreate, IncidentResponse, IncidentUpdate
from src.incidents import service
from src.auth import get_current_user
from src.entities.user import User

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.post("/", response_model=IncidentResponse, status_code=201)
def create_incident(
    payload: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a new incident. Requires authentication."""
    return service.create_incident(db, payload)


@router.get("/", response_model=List[IncidentResponse])
def list_incidents(
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(50, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all incidents, newest first. Requires authentication."""
    return service.get_all_incidents(db, skip, limit)


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single incident by ID. Requires authentication."""
    return service.get_incident_by_id(db, incident_id)


@router.patch("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: UUID,
    payload: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update incident fields. Requires authentication."""
    return service.update_incident(db, incident_id, payload)