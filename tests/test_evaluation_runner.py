from __future__ import annotations

from src.Adapters.BeirEvaluator import BeirEvaluator
from src.Adapters.RagasEvaluator import RagasEvaluator
from src.Application.EvaluationRunner import EvaluationRunner
from src.DomainModels.BEIRSample import BEIRSample
from src.DomainModels.EvalRecord import EvalRecord
from src.DomainModels.EvalSummary import EvalSummary


class _FakeLoader:
    def load(self, dataset_name: str, split: str = "test"):
        sample = BEIRSample(query_id="q1", query="hello", gold_doc_ids=["d1"])
        return [sample], {}, {}, {"q1": {"d1": 1}}


class _FakeApiClient:
    def ask(self, question: str, top_k=None):
        class _Ctx:
            def __init__(self):
                self.doc_id = "d1"
                self.text = "context"

        class _Answer:
            def __init__(self):
                self.answer = "response"
                self.contexts = [_Ctx()]

        return _Answer()


def test_evaluation_runner_sync_flow():
    """Run the sync flow and assert summary basics."""
    runner = EvaluationRunner(
        loader=_FakeLoader(),
        api_client=_FakeApiClient(),
        beir_evaluator=BeirEvaluator(),
        ragas_evaluator=RagasEvaluator(),
    )

    summary = runner.execute(dataset_name="dummy", use_async=False)
    assert isinstance(summary, EvalSummary)
    assert summary.record_count == 1
    assert "precision@1" in summary.beir_metrics
