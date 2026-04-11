from dataclasses import dataclass, field


@dataclass
class EvalSummary:
    """
    전체 평가 결과를 요약한 메트릭 묶음 객체.
    Metrics bundle summarizing the full evaluation run.
    """

    beir_metrics: dict = field(default_factory=dict)
    ragas_metrics: dict = field(default_factory=dict)
    record_count: int = 0
