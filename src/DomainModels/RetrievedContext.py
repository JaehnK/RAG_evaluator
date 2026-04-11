from dataclasses import dataclass


@dataclass
class RetrievedContext:
    doc_id: str
    text: str
    score: float
