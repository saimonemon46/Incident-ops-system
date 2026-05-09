from pydantic import BaseModel
from entities.incident import IncidentCategory, Severity

class TriageResult(BaseModel):
    category: IncidentCategory
    severity: Severity
    suggested_fix: str
    ai_notes: str
    confidence: float  # 0.0 - 1.0

class TriageResponse(BaseModel):
    incident_id: int
    triage: TriageResult
    message: str