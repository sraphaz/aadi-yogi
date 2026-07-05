#!/usr/bin/env python3
"""Run response-quality checks on golden questions using fallback or LLM mode."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from packages.evals.response_quality import run_response_quality_suite
from packages.prompts.llm_client import LLMClient


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run response-quality eval suite.")
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Use configured LLM provider (requires AADI_YOGI_LLM_API_KEY).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    llm_client = LLMClient()
    if args.llm:
        if not llm_client.available:
            print("FAIL LLM mode requested but AADI_YOGI_LLM_API_KEY is not configured.")
            return 1
        print(f"Running response eval in LLM mode (model={llm_client.model}).")
    else:
        llm_client = LLMClient(api_key=None)
        print("Running response eval in fallback mode (no LLM API key).")

    results = run_response_quality_suite(llm_client=llm_client)
    passed = 0
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{status} {result.question_id} notes={','.join(result.notes) or '-'}")
        if result.passed:
            passed += 1
    print(f"\n{passed}/{len(results)} response quality checks passed.")
    return 0 if passed >= len(results) - 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
