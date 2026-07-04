"""Evaluation runner.

Modes:
1. Validation (default): parse every probe and rubric file, verify schemas.
2. Scoring: given a JSONL of agent responses ({"probe_id": ..., "envelope": {...}}),
   run each probe's checks and print a summary with exit code.

Usage:
    python packages/evals/run_evals.py                 # validate probe/rubric files
    python packages/evals/run_evals.py responses.jsonl # score agent responses
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

EVALS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EVALS_DIR))

from aadi_evals import ResponseEnvelope, evaluate_probe, load_probe_file  # noqa: E402

PROBES_DIR = EVALS_DIR / "probes"
RUBRICS_DIR = EVALS_DIR / "rubrics"


def validate_files() -> int:
    failures = 0
    all_ids: set[str] = set()
    for path in sorted(PROBES_DIR.glob("*.yaml")):
        try:
            probes = load_probe_file(path)
        except (ValueError, KeyError, yaml.YAMLError) as exc:
            print(f"INVALID {path.name}: {exc}")
            failures += 1
            continue
        duplicated = [p.id for p in probes if p.id in all_ids]
        if duplicated:
            print(f"INVALID {path.name}: duplicate probe ids {duplicated}")
            failures += 1
        all_ids.update(p.id for p in probes)
        print(f"ok {path.name} ({len(probes)} probes)")
    for path in sorted(RUBRICS_DIR.glob("*.yaml")):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
            print(f"ok {path.name} (rubric)")
        except yaml.YAMLError as exc:
            print(f"INVALID {path.name}: {exc}")
            failures += 1
    print(f"{len(all_ids)} probes total")
    return 1 if failures else 0


def score_responses(responses_path: Path) -> int:
    probes = {}
    for path in sorted(PROBES_DIR.glob("*.yaml")):
        for probe in load_probe_file(path):
            probes[probe.id] = probe

    total = passed = 0
    with responses_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            probe = probes.get(record["probe_id"])
            if probe is None:
                print(f"unknown probe_id {record['probe_id']}")
                continue
            envelope = ResponseEnvelope.from_dict(record["envelope"])
            for result in evaluate_probe(probe, envelope):
                if result.status == "needs_grader":
                    continue
                total += 1
                passed += int(result.passed)
                if not result.passed:
                    print(f"FAIL {probe.id} {result.name}: {result.details}")
    print(f"{passed}/{total} checks passed")
    return 0 if passed == total else 1


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        return score_responses(Path(argv[1]))
    return validate_files()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
