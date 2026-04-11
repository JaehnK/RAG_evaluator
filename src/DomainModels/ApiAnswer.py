from dataclasses import dataclass, field

from .RetrievedContext import RetrievedContext


@dataclass
class ApiAnswer:
    """
    FastAPI 응답을 도메인 모델로 정규화한 값 객체.
    Value object normalizing the FastAPI response into a domain model.
    """

    answer: str
    contexts: list[RetrievedContext] = field(default_factory=list)
    raw: dict = field(default_factory=dict)
