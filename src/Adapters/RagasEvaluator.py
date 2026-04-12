from __future__ import annotations

from dataclasses import dataclass
import logging
import time
from typing import Any

import pandas as pd

from src.DomainModels import EvalRecord

logger = logging.getLogger(__name__)

@dataclass
class RagasEvaluator:
    """
    RAGAS를 이용해 응답 품질 지표를 계산하는 평가기.
    Evaluator that computes response quality metrics using RAGAS.
    """

    def build_dataset(self, records: list[EvalRecord]):
        """
        EvalRecord 리스트를 RAGAS EvaluationDataset으로 변환한다.
        Convert EvalRecord list into a RAGAS EvaluationDataset.
        """
        try:
            from ragas import EvaluationDataset, SingleTurnSample
        except ImportError as exc:  # pragma: no cover - runtime dependency
            raise RuntimeError("ragas is required to build evaluation datasets") from exc

        samples = []
        for record in records:
            samples.append(
                SingleTurnSample(
                    user_input=record.user_input,
                    response=record.response,
                    retrieved_contexts=record.retrieved_contexts,
                    retrieved_context_ids=record.retrieved_context_ids,
                    reference_context_ids=record.reference_context_ids,
                )
            )
        return EvaluationDataset(samples=samples)

    def evaluate(
        self,
        records: list[EvalRecord],
        metrics: list[Any],
    ) -> dict[str, float]:
        """
        RAGAS metrics를 실행하고 요약 점수를 반환한다.
        Run RAGAS metrics and return aggregate scores.
        """
        if not metrics:
            raise ValueError("metrics must be provided for RAGAS evaluation")
        start = time.perf_counter()

        try:
            from ragas import evaluate as ragas_evaluate
        except ImportError as exc:  # pragma: no cover - runtime dependency
            raise RuntimeError("ragas is required to evaluate metrics") from exc

        dataset = self.build_dataset(records)
        result = ragas_evaluate(dataset=dataset, metrics=metrics)
        df = result.to_pandas()
        summary = pd.to_numeric(df, errors="coerce").mean(numeric_only=True).to_dict()
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "action=eval_ragas status=ok records=%s metrics=%s elapsed_ms=%s",
            len(records),
            len(metrics),
            elapsed_ms,
        )
        return summary
