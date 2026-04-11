from dataclasses import dataclass


@dataclass
class BEIRSample:
    """
    BEIR 데이터셋의 단일 질의와 관련 문서 ID 집합을 담는 값 객체.
    Value object for a single BEIR query with its relevant document IDs.
    """

    query_id: str
    query: str
    gold_doc_ids: list[str]

    def __post_init__(self) -> None:
        """
        기본 필드 유효성을 점검한다.
        Validate basic field invariants.
        """
        if not self.query_id:
            raise ValueError("query_id must be non-empty")
        if not self.query:
            raise ValueError("query must be non-empty")
