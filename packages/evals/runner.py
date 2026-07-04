from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_QUESTIONS_PATH = REPO_ROOT / "packages" / "evals" / "golden_questions.json"


def load_golden_questions() -> list[dict[str, object]]:
    with GOLDEN_QUESTIONS_PATH.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("golden_questions.json must contain a list.")
    return data


def evaluate_retrieval_hit(question: dict[str, object], retrieved_source_ids: list[str]) -> bool:
    expected = question.get("expected_source_ids", [])
    if not isinstance(expected, list) or not expected:
        return bool(retrieved_source_ids)
    retrieved = set(retrieved_source_ids)
    return any(source_id in retrieved for source_id in expected)
