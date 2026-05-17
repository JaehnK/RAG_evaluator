from __future__ import annotations

import pytest

from src.Adapters.RagApiClient import RagApiClient


def test_build_payload_includes_contract_fields_and_advanced():
    payload = RagApiClient._build_payload(
        question="hello",
        dataset="scifact",
        split="test",
        sample_id="q1",
        advanced="hyde",
    )

    assert payload == {
        "question": "hello",
        "dataset": "scifact",
        "split": "test",
        "sample_id": "q1",
        "advanced": "hyde",
    }


def test_parse_rag_query_contract_response():
    answer = RagApiClient._parse_answer(
        {
            "status": "ok",
            "answer": "response",
            "retrieved_contexts": [
                {
                    "rank": 1,
                    "doc_id": "d1",
                    "chunk_id": 42,
                    "score": 0.91,
                    "text": "context",
                }
            ],
        }
    )

    assert answer.answer == "response"
    assert answer.contexts[0].doc_id == "d1"
    assert answer.contexts[0].text == "context"
    assert answer.contexts[0].score == 0.91


def test_parse_legacy_context_response():
    answer = RagApiClient._parse_answer(
        {
            "answer": "response",
            "contexts": [{"id": "d1", "score": 0.91, "text": "context"}],
        }
    )

    assert answer.contexts[0].doc_id == "d1"


def test_parse_error_response_raises_message():
    with pytest.raises(RuntimeError, match="blank"):
        RagApiClient._parse_answer(
            {
                "status": "error",
                "error": {"message": "Request field question must not be blank."},
            }
        )
