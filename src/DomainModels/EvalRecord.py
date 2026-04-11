from dataclasses import dataclass, field


@dataclass
class EvalRecord:
    """
    단일 질의에 대한 입력, 검색, 응답 정보를 묶은 평가 단위 객체.
    Evaluation unit aggregating input, retrieval, and response for one query.
    """

    query_id: str
    user_input: str
    response: str
    reference_context_ids: list[str] = field(default_factory=list)
    retrieved_context_ids: list[str] = field(default_factory=list)
    retrieved_contexts: list[str] = field(default_factory=list)
