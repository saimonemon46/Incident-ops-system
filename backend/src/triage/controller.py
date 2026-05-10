from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.core import get_db
from src.auth import get_current_user
from src.entities.user import User
from src.entities.incident import Incident
from src.exceptions import IncidentNotFound
from src.triage.service import triage_incident
from src.triage.models import TriageResponse

router = APIRouter(prefix="/incidents", tags=["triage"])


@router.post("/{incident_id}/triage", response_model=TriageResponse)
def trigger_triage(
    incident_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise IncidentNotFound(incident_id)

    result = triage_incident(
        incident_id=str(incident.id),
        title=incident.title,
        description=incident.description or "",
    )

    # persist triage result back to incident
    incident.category = result.category
    incident.severity = result.severity
    incident.suggested_fix = result.suggested_fix
    incident.ai_notes = result.ai_notes
    db.commit()
    db.refresh(incident)

    return TriageResponse(
        incident_id=incident.id,
        triage=result,
        message=f"Triage complete. Category: {result.category}. Severity: {result.severity}.",
    )