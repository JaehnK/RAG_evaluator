from dataclasses import dataclass, field


@dataclass
class EvalSummary:
    beir_metrics: dict = field(default_factory=dict)
    ragas_metrics: dict = field(default_factory=dict)
    record_count: int = 0
