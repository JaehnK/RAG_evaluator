from __future__ import annotations

import asyncio
from dataclasses import dataclass
import logging
import time
from typing import Any

from src.Adapters.BeirEvaluator import BeirEvaluator
from src.Adapters.BeirLoader import BeirLoader
from src.Adapters.RagApiClient import RagApiClient
from src.Adapters.RagasEvaluator import RagasEvaluator
from src.DomainModels.EvalRecord import EvalRecord
from src.DomainModels.EvalSummary import EvalSummary

logger = logging.getLogger(__name__)

@dataclass
class EvaluationRunner:
    """
    평가 파이프라인을 구성하는 오케스트레이터.
    Orchestrator that wires the evaluation pipeline.
    """

    loader: BeirLoader
    api_client: RagApiClient
    beir_evaluator: BeirEvaluator
    ragas_evaluator: RagasEvaluator

    async def _build_records_async(
        self,
        samples: list,
        top_k: int | None,
        concurrency: int,
    ) -> list[EvalRecord]:
        semaphore = asyncio.Semaphore(concurrency)

        async def _one(sample) -> EvalRecord:
            async with semaphore:
                answer = await self.api_client.ask_async(sample.query, top_k=top_k)
            return EvalRecord(
                query_id=sample.query_id,
                user_input=sample.query,
                response=answer.answer,
                reference_context_ids=sample.gold_doc_ids,
                retrieved_context_ids=[ctx.doc_id for ctx in answer.contexts],
                retrieved_contexts=[ctx.text for ctx in answer.contexts],
            )

        tasks = [_one(sample) for sample in samples]
        return await asyncio.gather(*tasks)

    def _build_records_sync(
        self, samples: list, top_k: int | None
    ) -> list[EvalRecord]:
        records: list[EvalRecord] = []
        for sample in samples:
            answer = self.api_client.ask(sample.query, top_k=top_k)
            records.append(
                EvalRecord(
                    query_id=sample.query_id,
                    user_input=sample.query,
                    response=answer.answer,
                    reference_context_ids=sample.gold_doc_ids,
                    retrieved_context_ids=[ctx.doc_id for ctx in answer.contexts],
                    retrieved_contexts=[ctx.text for ctx in answer.contexts],
                )
            )
        return records

    def execute(
        self,
        dataset_name: str,
        split: str = "test",
        top_k: int | None = None,
        ragas_metrics: list[Any] | None = None,
        use_async: bool = False,
        concurrency: int = 8,
    ) -> EvalSummary:
        """
        BEIR + RAGAS 평가를 실행하고 요약 결과를 반환한다.
        Run BEIR + RAGAS evaluation and return a summary.
        """
        start = time.perf_counter()
        logger.info(
            "action=run_evaluation status=start dataset=%s split=%s use_async=%s concurrency=%s",
            dataset_name,
            split,
            use_async,
            concurrency,
        )

        samples, _corpus, _queries, _qrels = self.loader.load(
            dataset_name=dataset_name, split=split
        )

        if use_async:
            records = asyncio.run(
                self._build_records_async(samples, top_k=top_k, concurrency=concurrency)
            )
        else:
            records = self._build_records_sync(samples, top_k=top_k)

        logger.info(
            "action=build_records status=ok records=%s",
            len(records),
        )

        beir_metrics = self.beir_evaluator.evaluate(records)
        ragas_metrics_result: dict[str, float] = {}
        if ragas_metrics:
            ragas_metrics_result = self.ragas_evaluator.evaluate(
                records=records, metrics=ragas_metrics
            )

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "action=run_evaluation status=ok records=%s elapsed_ms=%s",
            len(records),
            elapsed_ms,
        )
        return EvalSummary(
            beir_metrics=beir_metrics,
            ragas_metrics=ragas_metrics_result,
            record_count=len(records),
        )
