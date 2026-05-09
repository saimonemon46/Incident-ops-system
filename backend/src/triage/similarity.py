import faiss
import numpy as np
from dataclasses import dataclass, field

EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 output size

@dataclass
class IncidentRecord:
    incident_id: int
    text: str
    suggested_fix: str

@dataclass
class FAISSIndex:
    index: faiss.IndexFlatIP = field(default_factory=lambda: faiss.IndexFlatIP(EMBEDDING_DIM))
    records: list[IncidentRecord] = field(default_factory=list)

_faiss_index = FAISSIndex()


def get_index() -> FAISSIndex:
    return _faiss_index


def add_incident(incident_id: int, text: str, suggested_fix: str, embedding: np.ndarray):
    idx = get_index()
    vec = embedding.reshape(1, -1).astype("float32")
    idx.index.add(vec)
    idx.records.append(IncidentRecord(
        incident_id=incident_id,
        text=text,
        suggested_fix=suggested_fix,
    ))


def search_similar(embedding: np.ndarray, top_k: int = 3) -> list[dict]:
    idx = get_index()

    if idx.index.ntotal == 0:
        return []

    vec = embedding.reshape(1, -1).astype("float32")
    k = min(top_k, idx.index.ntotal)
    scores, indices = idx.index.search(vec, k)

    results = []
    for score, i in zip(scores[0], indices[0]):
        if i == -1:
            continue
        record = idx.records[i]
        results.append({
            "incident_id": record.incident_id,
            "text": record.text,
            "suggested_fix": record.suggested_fix,
            "similarity_score": float(score),
        })

    return results