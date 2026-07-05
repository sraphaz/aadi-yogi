"""Run restraint probes against the contract router (no LLM required)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
EVALS_DIR = REPO_ROOT / "packages" / "evals"
sys.path.insert(0, str(EVALS_DIR))

from aadi_evals import ResponseEnvelope, evaluate_probe, load_probe_file  # noqa: E402
from packages.prompts.contract import envelope_to_dict, restraint_envelope  # noqa: E402
from packages.prompts.restraint import detect_restraint  # noqa: E402
from packages.prompts.orchestrator import inquire  # noqa: E402


def main() -> int:
    restraint_path = EVALS_DIR / "probes" / "restraint_cases.yaml"
    probes = load_probe_file(restraint_path)
    passed = total = 0
    lines: list[dict] = []

    for probe in probes:
        case = detect_restraint(probe.prompt)
        if case:
            envelope = restraint_envelope(case)
            provider = "restraint_router"
        else:
            result = inquire(probe.prompt)
            envelope = result.envelope
            provider = result.provider

        record = {
            "probe_id": probe.id,
            "envelope": envelope_to_dict(envelope),
            "provider": provider,
        }
        lines.append(record)

        for check in evaluate_probe(probe, envelope):
            if check.status == "needs_grader":
                continue
            total += 1
            ok = check.passed
            passed += int(ok)
            if not ok:
                print(f"FAIL {probe.id} {check.name}: {check.details}")

    out = REPO_ROOT / ".tmp_contract_probes.jsonl"
    out.write_text("\n".join(json.dumps(line) for line in lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    print(f"{passed}/{total} restraint probe checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
