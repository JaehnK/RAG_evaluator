from dataclasses import dataclass, field

from .RetrievedContext import RetrievedContext


@dataclass
class ApiAnswer:
    answer: str
    contexts: list[RetrievedContext] = field(default_factory=list)
    raw: dict = field(default_factory=dict)
