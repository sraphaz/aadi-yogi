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

from functools import lru_cache
import json
import sys
from pathlib import Path

import yaml

EVALS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EVALS_DIR))

from aadi_evals import ResponseEnvelope, evaluate_probe, load_probe_file  # noqa: E402

PROBES_DIR = EVALS_DIR / "probes"
RUBRICS_DIR = EVALS_DIR / "rubrics"
CONTENT_SOURCES_DIR = EVALS_DIR.parents[1] / "content" / "sources"


def _duplicate_probe_ids(probes, existing_ids: set[str]) -> list[str]:
    duplicated: set[str] = set()
    file_ids: set[str] = set()
    for probe in probes:
        if probe.id in existing_ids or probe.id in file_ids:
            duplicated.add(probe.id)
        file_ids.add(probe.id)
    return sorted(duplicated)


def _ordinal_suffix(value: str, prefix: str) -> str | None:
    if not value.startswith(prefix):
        return None
    suffix = value.removeprefix(prefix)
    if not suffix.isdigit():
        return None
    return f"{int(suffix):02d}"


@lru_cache(maxsize=None)
def _resolve_passage_text(passage_id: str) -> str | None:
    parts = passage_id.split(".")
    if not parts:
        return None

    candidates: list[Path] = []
    collection = parts[0]
    if collection == "gita" and len(parts) >= 2:
        chapter = _ordinal_suffix(parts[1], "ch")
        if chapter is not None:
            candidates.append(CONTENT_SOURCES_DIR / "bhagavad_gita" / f"chapter_{chapter}.template.md")
    elif collection == "upanishads" and len(parts) >= 3:
        mantra = _ordinal_suffix(parts[2], "m")
        if mantra is not None:
            candidates.append(
                CONTENT_SOURCES_DIR / "upanishads" / parts[1] / f"mantra_{mantra}.template.md"
            )
    elif collection == "cwsa" and len(parts) >= 4 and parts[1] == "life_divine":
        book = _ordinal_suffix(parts[2], "bk")
        chapter = _ordinal_suffix(parts[3], "ch")
        if book is not None and chapter is not None:
            candidates.append(
                CONTENT_SOURCES_DIR
                / "sri_aurobindo"
                / "the_life_divine"
                / f"book_{book}_chapter_{chapter}.template.md"
            )
    elif collection == "cwm" and len(parts) >= 2 and parts[1] == "prayers_and_meditations":
        candidates.append(
            CONTENT_SOURCES_DIR / "the_mother" / "prayers_and_meditations" / "selection_01.template.md"
        )
    elif collection == "siddha" and len(parts) >= 2 and parts[1] == "tirumandiram":
        candidates.append(CONTENT_SOURCES_DIR / "siddha_texts" / "tirumandiram" / "README.md")

    for candidate in candidates:
        if candidate.exists():
            return candidate.read_text(encoding="utf-8")
    return None


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
        duplicated = _duplicate_probe_ids(probes, all_ids)
        if duplicated:
            print(f"INVALID {path.name}: duplicate probe ids {duplicated}")
            failures += 1
        else:
            print(f"ok {path.name} ({len(probes)} probes)")
        all_ids.update(p.id for p in probes)
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
    all_ids: set[str] = set()
    for path in sorted(PROBES_DIR.glob("*.yaml")):
        file_probes = load_probe_file(path)
        duplicated = _duplicate_probe_ids(file_probes, all_ids)
        if duplicated:
            print(f"INVALID {path.name}: duplicate probe ids {duplicated}")
            return 1
        for probe in file_probes:
            probes[probe.id] = probe
        all_ids.update(probe.id for probe in file_probes)

    total = passed = 0
    unknown_probe_ids = 0
    with responses_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            probe = probes.get(record["probe_id"])
            if probe is None:
                print(f"unknown probe_id {record['probe_id']}")
                unknown_probe_ids += 1
                continue
            envelope = ResponseEnvelope.from_dict(record["envelope"])
            for result in evaluate_probe(probe, envelope, resolver=_resolve_passage_text):
                if result.status == "needs_grader":
                    continue
                total += 1
                passed += int(result.passed)
                if not result.passed:
                    print(f"FAIL {probe.id} {result.name}: {result.details}")
    print(f"{passed}/{total} checks passed")
    if total == 0:
        print("FAIL no checks ran")
    return 0 if total > 0 and passed == total and unknown_probe_ids == 0 else 1


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        return score_responses(Path(argv[1]))
    return validate_files()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
