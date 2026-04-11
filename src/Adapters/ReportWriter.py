from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from src.DomainModels.EvalSummary import EvalSummary


class ReportWriter:
    """
    평가 요약을 파일로 저장하는 어댑터.
    Adapter that writes evaluation summaries to files.
    """

    def __init__(self, output_dir: str = "reports") -> None:
        self.output_dir = output_dir

    def _ensure_output_dir(self) -> Path:
        output_path = Path(self.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path

    def write_json(self, summary: EvalSummary, filename: str = "summary.json") -> Path:
        """
        EvalSummary를 JSON 파일로 저장한다.
        Persist EvalSummary to a JSON file.
        """
        output_path = self._ensure_output_dir()
        file_path = output_path / filename
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(asdict(summary), file, ensure_ascii=False, indent=2)
        return file_path

    def write_markdown(
        self, summary: EvalSummary, filename: str = "summary.md"
    ) -> Path:
        """
        EvalSummary를 Markdown 파일로 저장한다.
        Persist EvalSummary to a Markdown file.
        """
        output_path = self._ensure_output_dir()
        file_path = output_path / filename

        lines: list[str] = []
        lines.append("# Evaluation Summary")
        lines.append("")
        lines.append("## Summary")
        lines.append(f"- Records: {summary.record_count}")
        lines.append("")

        lines.append("## BEIR Metrics")
        if summary.beir_metrics:
            lines.append("")
            lines.append("| Metric | Value |")
            lines.append("| --- | --- |")
            for key in sorted(summary.beir_metrics.keys()):
                lines.append(f"| {key} | {summary.beir_metrics[key]} |")
        else:
            lines.append("- (none)")
        lines.append("")

        lines.append("## RAGAS Metrics")
        if summary.ragas_metrics:
            lines.append("")
            lines.append("| Metric | Value |")
            lines.append("| --- | --- |")
            for key in sorted(summary.ragas_metrics.keys()):
                lines.append(f"| {key} | {summary.ragas_metrics[key]} |")
        else:
            lines.append("- (none)")
        lines.append("")

        file_path.write_text("\n".join(lines), encoding="utf-8")
        return file_path
