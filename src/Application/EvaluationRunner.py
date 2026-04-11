from __future__ import annotations

from dataclasses import dataclass

from src.Adapters.BeirEvaluator import BeirEvaluator
from src.Adapters.BeirLoader import BeirLoader
from src.Adapters.RagApiClient import RagApiClient
from src.Adapters.RagasEvaluator import RagasEvaluator
from src.DomainModels.EvalSummary import EvalSummary


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

    def execute(self) -> EvalSummary:
        """
        최소 실행 경로를 제공하는 스텁 메서드.
        Stub method that provides a minimal execution path.
        """
        # TODO: Load BEIR samples, query API, build EvalRecord list.
        # TODO: Run BEIR and RAGAS evaluators.
        return EvalSummary()
