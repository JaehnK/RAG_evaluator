from dataclasses import dataclass


@dataclass
class BEIRSample:
    """
    BEIR 데이터셋의 단일 질의와 학습용 양/음성 문서를 담는 값 객체.
    Value object for a single BEIR query with positive/negative documents for training.
    """

    query: str
    positive_doc: str
    negative_doc: str

    def __post_init__(self) -> None:
        """
        기본 필드 유효성을 점검한다.
        Validate basic field invariants.
        """
        if not self.query:
            raise ValueError("query must be non-empty")
