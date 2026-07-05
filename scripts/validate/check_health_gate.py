#!/usr/bin/env python3
"""RF-037: block unreviewed health-sensitive content from rendering promotion."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / "content" / "sources"
MANIFEST_DIR = ROOT / "scripts" / "ingest" / "manifests"
NATURE_DIR = ROOT / "apps" / "web" / "static" / "data" / "nature"
LIBRARY_DIR = ROOT / "apps" / "web" / "static" / "data" / "library"

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.DOTALL)


def parse_frontmatter(text: str) -> dict | None:
    match = FRONTMATTER.match(text)
    if not match:
        return None
    data = yaml.safe_load(match.group(1)) or {}
    return data if isinstance(data, dict) else None


def check_markdown_sources() -> list[str]:
    errors: list[str] = []
    for path in sorted(SOURCES.rglob("*.md")):
        if path.name == "README.md":
            continue
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not fm:
            continue
        if not (fm.get("health_sensitive") or fm.get("health_touching")):
            continue
        review = fm.get("safety_review")
        if not isinstance(review, dict):
            rel = path.relative_to(ROOT).as_posix()
            errors.append(f"{rel}: health_sensitive without safety_review block")
            continue
        for field in ("reviewer", "reviewed_at", "tier_decision"):
            if not review.get(field):
                rel = path.relative_to(ROOT).as_posix()
                errors.append(f"{rel}: safety_review missing '{field}'")
    return errors


def check_ingest_manifests() -> list[str]:
    errors: list[str] = []
    for path in sorted(MANIFEST_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not data.get("health_sensitive"):
            continue
        review = data.get("health_review")
        if not isinstance(review, dict) or not review.get("reviewer"):
            errors.append(f"{path.relative_to(ROOT).as_posix()}: health_sensitive collection without health_review.reviewer")
    return errors


def check_ui_tiers() -> list[str]:
    errors: list[str] = []
    for path in sorted(NATURE_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for passage in data.get("passages", []):
            tier = passage.get("tier", "documentary")
            if tier == "closed":
                rel = path.relative_to(ROOT).as_posix()
                errors.append(f"{rel}: closed-tier passage must not ship in UI data")
    for path in sorted(LIBRARY_DIR.glob("*.json")):
        if path.name == "catalog.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("health_tier") == "closed":
            errors.append(f"{path.relative_to(ROOT).as_posix()}: closed health_tier in library passage")
    return errors


def main() -> int:
    errors = check_markdown_sources() + check_ingest_manifests() + check_ui_tiers()
    if errors:
        print("Health gate violations:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("Health gate OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
