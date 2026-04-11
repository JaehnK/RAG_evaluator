from dataclasses import dataclass, field


@dataclass
class EvalRecord:
    query_id: str
    user_input: str
    response: str
    reference_context_ids: list[str] = field(default_factory=list)
    retrieved_context_ids: list[str] = field(default_factory=list)
    retrieved_contexts: list[str] = field(default_factory=list)
