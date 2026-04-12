from __future__ import annotations

from dataclasses import dataclass
import logging
import time

from src.DomainModels.EvalRecord import EvalRecord

logger = logging.getLogger(__name__)

@dataclass
class BeirEvaluator:
    """
    검색 결과를 기반으로 간단한 IR 지표를 계산하는 평가기.
    Evaluator that computes simple IR metrics from retrieval results.
    """

    def evaluate(
        self,
        records: list[EvalRecord],
        k_values: tuple[int, ...] = (1, 3, 5, 10),
    ) -> dict[str, float]:
        """
        EvalRecord 리스트로부터 precision/recall@k를 계산한다.
        Compute precision/recall@k from EvalRecord list.
        """
        start = time.perf_counter()
        metrics: dict[str, float] = {}
        if not records:
            for k in k_values:
                metrics[f"precision@{k}"] = 0.0
                metrics[f"recall@{k}"] = 0.0
            return metrics

        for k in k_values:
            precision_sum = 0.0
            recall_sum = 0.0

            for record in records:
                retrieved = record.retrieved_context_ids[:k]
                gold = set(record.reference_context_ids)

                if not retrieved:
                    precision = 0.0
                else:
                    precision = len(
                        [doc_id for doc_id in retrieved if doc_id in gold]
                    ) / len(retrieved)

                if not gold:
                    recall = 0.0
                else:
                    recall = len(
                        [doc_id for doc_id in retrieved if doc_id in gold]
                    ) / len(gold)

                precision_sum += precision
                recall_sum += recall

            metrics[f"precision@{k}"] = precision_sum / len(records)
            metrics[f"recall@{k}"] = recall_sum / len(records)

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "action=eval_beir status=ok records=%s k_values=%s elapsed_ms=%s",
            len(records),
            k_values,
            elapsed_ms,
        )
        return metrics
