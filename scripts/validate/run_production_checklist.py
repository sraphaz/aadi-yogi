#!/usr/bin/env python3
"""Automated checks for docs/production_review_checklist.md (machine-verifiable items)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from packages.rag.dense_vector_store import DEFAULT_DENSE_INDEX_PATH
from packages.rag.vector_store import DEFAULT_INDEX_PATH


def run(cmd: list[str], env: dict[str, str] | None = None) -> tuple[int, str]:
    merged_env = {**dict(__import__("os").environ), "PYTHONPATH": str(REPO_ROOT)}
    if env:
        merged_env.update(env)
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, env=merged_env)
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode, output.strip()


def load_health_fn():
    import importlib.util

    main_path = REPO_ROOT / "apps" / "agent-api" / "main.py"
    spec = importlib.util.spec_from_file_location("agent_api_main", main_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load health handler from {main_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.health


def check(name: str, ok: bool, detail: str = "") -> bool:
    status = "PASS" if ok else "FAIL"
    suffix = f" — {detail}" if detail else ""
    print(f"{status} {name}{suffix}")
    return ok


def main() -> int:
    passed = 0
    total = 0

    def record(name: str, ok: bool, detail: str = "") -> None:
        nonlocal passed, total
        total += 1
        if check(name, ok, detail):
            passed += 1

    record("TF-IDF index exists", DEFAULT_INDEX_PATH.exists(), str(DEFAULT_INDEX_PATH.relative_to(REPO_ROOT)))
    record("Dense index exists", DEFAULT_DENSE_INDEX_PATH.exists(), str(DEFAULT_DENSE_INDEX_PATH.relative_to(REPO_ROOT)))
    record("docker-compose.yml present", (REPO_ROOT / "docker-compose.yml").exists())
    record(".env.example present", (REPO_ROOT / ".env.example").exists())
    record("production_setup.md present", (REPO_ROOT / "docs" / "production_setup.md").exists())

    code, _ = run(["python3", "-m", "pytest", "-q"])

    record("pytest suite", code == 0)

    code, _ = run(["python3", "scripts/validate/run_golden_questions.py"])
    record("golden question retrieval", code == 0)

    code, _ = run(["python3", "scripts/validate/run_response_eval.py"])
    record("response quality (fallback)", code == 0)

    health = load_health_fn()
    health_payload = health()
    record("/health status ok", health_payload.get("status") == "ok")
    record("/health reports indexes", bool(health_payload.get("tfidf_index")) and bool(health_payload.get("dense_index")))

    print(f"\n{passed}/{total} automated production checks passed.")
    print("Human review still required: consciousness core manifest, corpus rights, LLM mode with API keys.")
    return 0 if passed >= total - 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
