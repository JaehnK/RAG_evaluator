from __future__ import annotations

import argparse
import logging
import json
from dataclasses import asdict
from typing import Any

from src.Adapters.BeirEvaluator import BeirEvaluator
from src.Adapters.BeirLoader import BeirLoader
from src.Adapters.RagApiClient import RagApiClient
from src.Adapters.RagasEvaluator import RagasEvaluator
from src.Application.EvaluationRunner import EvaluationRunner


def _build_metrics(metric_names: list[str]) -> list[Any]:
    if not metric_names:
        return []
    try:
        from ragas import metrics as ragas_metrics_module
    except ImportError as exc:  # pragma: no cover - runtime dependency
        raise RuntimeError("ragas is required to use ragas metrics") from exc

    metrics: list[Any] = []
    for name in metric_names:
        if not hasattr(ragas_metrics_module, name):
            raise ValueError(f"Unknown ragas metric: {name}")
        metric_obj = getattr(ragas_metrics_module, name)
        metric = metric_obj() if isinstance(metric_obj, type) else metric_obj
        metrics.append(metric)
    return metrics


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BEIR + RAGAS evaluation CLI")
    parser.add_argument("--dataset", required=True, help="BEIR dataset name")
    parser.add_argument("--split", default="test", help="BEIR split (default: test)")
    parser.add_argument("--base-url", required=True, help="FastAPI base URL")
    parser.add_argument("--top-k", type=int, default=None, help="Top-k contexts")
    parser.add_argument(
        "--async",
        dest="use_async",
        action="store_true",
        help="Use async HTTP requests",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=8,
        help="Max concurrent requests when async is enabled",
    )
    parser.add_argument(
        "--ragas-metric",
        dest="ragas_metrics",
        action="append",
        default=[],
        help="RAGAS metric name from ragas.metrics (repeatable)",
    )
    return parser.parse_args()


def run() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    args = _parse_args()

    loader = BeirLoader()
    api_client = RagApiClient(base_url=args.base_url)
    beir_evaluator = BeirEvaluator()
    ragas_evaluator = RagasEvaluator()

    runner = EvaluationRunner(
        loader=loader,
        api_client=api_client,
        beir_evaluator=beir_evaluator,
        ragas_evaluator=ragas_evaluator,
    )

    metrics = _build_metrics(args.ragas_metrics)
    summary = runner.execute(
        dataset_name=args.dataset,
        split=args.split,
        top_k=args.top_k,
        ragas_metrics=metrics,
        use_async=args.use_async,
        concurrency=args.concurrency,
    )

    print(json.dumps(asdict(summary), ensure_ascii=False, indent=2))
    return 0
