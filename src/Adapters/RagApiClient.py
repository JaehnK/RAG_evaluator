from __future__ import annotations

from dataclasses import dataclass

import httpx

from src.DomainModels.ApiAnswer import ApiAnswer
from src.DomainModels.RetrievedContext import RetrievedContext


@dataclass
class RagApiClient:
    """
    FastAPI 엔드포인트 호출을 담당하는 어댑터.
    Adapter responsible for calling the FastAPI endpoint.
    """

    base_url: str
    endpoint: str = "/ask"
    timeout_sec: float = 30.0

    def _build_url(self) -> str:
        endpoint = self.endpoint if self.endpoint.startswith("/") else f"/{self.endpoint}"
        return f"{self.base_url.rstrip('/')}{endpoint}"

    @staticmethod
    def _parse_answer(payload: dict) -> ApiAnswer:
        contexts = []
        for ctx in payload.get("contexts", []) or []:
            contexts.append(
                RetrievedContext(
                    doc_id=str(ctx.get("id", "")),
                    text=str(ctx.get("text", "")),
                    score=float(ctx.get("score", 0.0)),
                )
            )
        return ApiAnswer(
            answer=str(payload.get("answer", "")),
            contexts=contexts,
            raw=payload,
        )

    def ask(self, question: str, top_k: int | None = None) -> ApiAnswer:
        payload = {"question": question}
        if top_k is not None:
            payload["top_k"] = top_k
        with httpx.Client(timeout=self.timeout_sec) as client:
            response = client.post(self._build_url(), json=payload)
            response.raise_for_status()
            return self._parse_answer(response.json())

    async def ask_async(self, question: str, top_k: int | None = None) -> ApiAnswer:
        payload = {"question": question}
        if top_k is not None:
            payload["top_k"] = top_k
        async with httpx.AsyncClient(timeout=self.timeout_sec) as client:
            response = await client.post(self._build_url(), json=payload)
            response.raise_for_status()
            return self._parse_answer(response.json())
