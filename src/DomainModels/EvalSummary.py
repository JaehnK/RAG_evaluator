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

    def __post_init__(self) -> None:
        """
        요약 메트릭의 기본 유효성을 점검한다.
        Validate basic invariants for the summary metrics.
        """
        if self.record_count < 0:
            raise ValueError("record_count must be >= 0")
