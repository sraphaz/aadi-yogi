#!/usr/bin/env python3
"""Report creator calibration status (ADR 0001, ADR 0003). Exit 0 always — informational gate."""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CAL_DIR = ROOT / "docs" / "calibrations"


def load(name: str) -> dict:
    path = CAL_DIR / name
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main() -> int:
    pending: list[str] = []
    for filename in ("0001-dana.yaml", "0003-health-reviewers.yaml"):
        data = load(filename)
        status = data.get("status", "pending")
        label = filename.replace(".yaml", "")
        if status != "calibrated":
            pending.append(label)
            print(f"PENDING  {label}  (status={status})")
        else:
            print(f"OK       {label}")

    if pending:
        print(f"\n{len(pending)} calibration(s) still pending — creators must fill docs/calibrations/")
        return 0
    print("\nAll creator calibrations recorded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
