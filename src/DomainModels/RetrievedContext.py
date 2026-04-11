from dataclasses import dataclass


@dataclass
class RetrievedContext:
    """
    검색 결과로 회수된 문서 조각과 메타데이터를 담는 값 객체.
    Value object holding a retrieved document chunk and its metadata.
    """

    doc_id: str
    text: str
    score: float
