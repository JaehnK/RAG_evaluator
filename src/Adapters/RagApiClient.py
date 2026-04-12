from __future__ import annotations

from dataclasses import dataclass
import logging
import time

import httpx

from src.DomainModels.ApiAnswer import ApiAnswer
from src.DomainModels.RetrievedContext import RetrievedContext

logger = logging.getLogger(__name__)


def _truncate(text: str, limit: int = 200) -> str:
    if len(text) <= limit:
        return text
    return f"{text[:limit]}..."


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
        """
        base_url과 endpoint를 결합해 호출 URL을 구성한다.
        Build the full request URL from base_url and endpoint.
        """
        endpoint = (
            self.endpoint if self.endpoint.startswith("/") else f"/{self.endpoint}"
        )
        return f"{self.base_url.rstrip('/')}{endpoint}"

    @staticmethod
    def _parse_answer(payload: dict) -> ApiAnswer:
        """
        API 응답 JSON을 ApiAnswer로 변환한다.
        Convert the API JSON payload into ApiAnswer.
        """
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
        """
        동기 방식으로 질문을 보내고 응답을 반환한다.
        Send a question synchronously and return the response.
        """
        payload = {"question": question}
        if top_k is not None:
            payload["top_k"] = top_k
        start = time.perf_counter()
        with httpx.Client(timeout=self.timeout_sec) as client:
            try:
                response = client.post(self._build_url(), json=payload)
                response.raise_for_status()
                answer = self._parse_answer(response.json())
                elapsed_ms = int((time.perf_counter() - start) * 1000)
                logger.info(
                    "action=ask status=ok elapsed_ms=%s query=%s",
                    elapsed_ms,
                    _truncate(question),
                )
                return answer
            except Exception:
                elapsed_ms = int((time.perf_counter() - start) * 1000)
                logger.exception(
                    "action=ask status=error elapsed_ms=%s query=%s",
                    elapsed_ms,
                    _truncate(question),
                )
                raise

    async def ask_async(self, question: str, top_k: int | None = None) -> ApiAnswer:
        """
        비동기 방식으로 질문을 보내고 응답을 반환한다.
        Send a question asynchronously and return the response.
        """
        payload = {"question": question}
        if top_k is not None:
            payload["top_k"] = top_k
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=self.timeout_sec) as client:
            try:
                response = await client.post(self._build_url(), json=payload)
                response.raise_for_status()
                answer = self._parse_answer(response.json())
                elapsed_ms = int((time.perf_counter() - start) * 1000)
                logger.info(
                    "action=ask_async status=ok elapsed_ms=%s query=%s",
                    elapsed_ms,
                    _truncate(question),
                )
                return answer
            except Exception:
                elapsed_ms = int((time.perf_counter() - start) * 1000)
                logger.exception(
                    "action=ask_async status=error elapsed_ms=%s query=%s",
                    elapsed_ms,
                    _truncate(question),
                )
                raise
