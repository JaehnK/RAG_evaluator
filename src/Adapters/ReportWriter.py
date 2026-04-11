from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from src.DomainModels.EvalSummary import EvalSummary


@dataclass
class ReportWriter:
    """
    평가 요약을 파일로 저장하는 어댑터.
    Adapter that writes evaluation summaries to files.
    """

    output_dir: str = "reports"

    def write_json(self, summary: EvalSummary, filename: str = "summary.json") -> Path:
        """
        EvalSummary를 JSON 파일로 저장한다.
        Persist EvalSummary to a JSON file.
        """
        output_path = Path(self.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / filename
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(asdict(summary), file, ensure_ascii=False, indent=2)
        return file_path
