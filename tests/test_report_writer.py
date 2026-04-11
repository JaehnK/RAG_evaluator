from __future__ import annotations

"""Tests for ReportWriter output formats."""

import json

from src.Adapters.ReportWriter import ReportWriter
from src.DomainModels.EvalSummary import EvalSummary


def test_report_writer_writes_json_and_markdown(tmp_path):
    writer = ReportWriter(output_dir=str(tmp_path))
    summary = EvalSummary(
        beir_metrics={"precision@1": 0.5},
        ragas_metrics={"faithfulness": 0.75},
        record_count=2,
    )

    json_path = writer.write_json(summary, filename="out.json")
    md_path = writer.write_markdown(summary, filename="out.md")

    assert json_path.exists()
    assert md_path.exists()

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["record_count"] == 2
    assert data["beir_metrics"]["precision@1"] == 0.5
    assert data["ragas_metrics"]["faithfulness"] == 0.75

    md_text = md_path.read_text(encoding="utf-8")
    assert "# Evaluation Summary" in md_text
    assert "| precision@1 | 0.5 |" in md_text
    assert "| faithfulness | 0.75 |" in md_text
