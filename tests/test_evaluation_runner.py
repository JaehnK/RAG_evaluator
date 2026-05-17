from __future__ import annotations

from src.Adapters import BeirEvaluator, RagasEvaluator
from src.Application import EvaluationRunner
from src.DomainModels import BEIRSample, EvalSummary


class _FakeLoader:
    def load(self, dataset_name: str, split: str = "test"):
        sample = BEIRSample(query_id="q1", query="hello", gold_doc_ids=["d1"])
        return [sample], {}, {}, {"q1": {"d1": 1}}


class _FakeApiClient:
    def __init__(self):
        self.last_kwargs = None

    def ask(self, question: str, **kwargs):
        self.last_kwargs = kwargs

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
    api_client = _FakeApiClient()
    runner = EvaluationRunner(
        loader=_FakeLoader(),
        api_client=api_client,
        beir_evaluator=BeirEvaluator(),
        ragas_evaluator=RagasEvaluator(),
    )

    summary = runner.execute(dataset_name="dummy", use_async=False, advanced="hyde")
    assert isinstance(summary, EvalSummary)
    assert summary.record_count == 1
    assert "precision@1" in summary.beir_metrics
    assert api_client.last_kwargs["dataset"] == "dummy"
    assert api_client.last_kwargs["split"] == "test"
    assert api_client.last_kwargs["sample_id"] == "q1"
    assert api_client.last_kwargs["advanced"] == "hyde"
