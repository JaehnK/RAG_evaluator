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

    def __post_init__(self) -> None:
        """
        검색 결과의 기본 필드를 검증한다.
        Validate basic fields of the retrieved context.
        """
        if not self.doc_id:
            raise ValueError("doc_id must be non-empty")
