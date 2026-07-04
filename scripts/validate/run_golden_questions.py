#!/usr/bin/env python3
"""Run golden-question retrieval checks against chunked corpus."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from packages.evals.runner import evaluate_retrieval_hit, load_golden_questions
from packages.rag.retriever import SimpleRetriever


def main() -> int:
    retriever = SimpleRetriever()
    questions = load_golden_questions()
    passed = 0
    for question in questions:
        hits = retriever.retrieve(str(question["question"]), top_k=5)
        source_ids = [hit.source_id for hit in hits]
        ok = evaluate_retrieval_hit(question, source_ids)
        status = "PASS" if ok else "FAIL"
        print(f"{status} {question['id']}: {question['question'][:70]}")
        if ok:
            passed += 1
    print(f"\n{passed}/{len(questions)} golden questions passed retrieval check.")
    return 0 if passed >= len(questions) - 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
