#!/usr/bin/env python3
"""Run response-quality checks on golden questions using fallback mode."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from packages.evals.response_quality import run_response_quality_suite  # noqa: E402


def main() -> int:
    results = run_response_quality_suite()
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
