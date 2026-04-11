from __future__ import annotations

from dataclasses import dataclass

from src.DomainModels.EvalRecord import EvalRecord


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

        return metrics
