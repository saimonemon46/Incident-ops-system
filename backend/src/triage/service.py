from triage.rules import run_rules
from triage.classifier import embed
from triage.similarity import search_similar, add_incident
from triage.models import TriageResult
from entities.incident import IncidentCategory, Severity


def triage_incident(
    incident_id: int,
    title: str,
    description: str,
) -> TriageResult:
    text = f"{title} {description or ''}"

    # Step 1: rule engine (fast, no model)
    rule_result = run_rules(title, description or "")

    # Step 2: embed text
    embedding = embed(text)

    # Step 3: find similar past incidents
    similar = search_similar(embedding, top_k=3)

    # Step 4: build ai_notes
    ai_notes = rule_result["ai_notes"]
    if similar:
        top = similar[0]
        score = top["similarity_score"]
        if score > 0.75:
            ai_notes += f" | Similar past incident #{top['incident_id']} (score: {score:.2f}): {top['suggested_fix']}"

    # Step 5: confidence boost if similar found
    confidence = rule_result["confidence"]
    if similar and similar[0]["similarity_score"] > 0.75:
        confidence = min(confidence + 0.15, 1.0)

    # Step 6: index this incident for future similarity
    add_incident(
        incident_id=incident_id,
        text=text,
        suggested_fix=rule_result["suggested_fix"],
        embedding=embedding,
    )

    return TriageResult(
        category=rule_result["category"],
        severity=rule_result["severity"],
        suggested_fix=rule_result["suggested_fix"],
        ai_notes=ai_notes,
        confidence=round(confidence, 2),
    )