#!/usr/bin/env python3
"""Build library catalog for PWA shelves (RF-038 living corpus protocol)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
LIBRARY_DIR = ROOT / "apps" / "web" / "static" / "data" / "library"
MANIFEST_DIR = ROOT / "scripts" / "ingest" / "manifests"
SOURCES_DIR = ROOT / "content" / "sources"
OUTPUT = LIBRARY_DIR / "catalog.json"

DEFAULT_SHELVES = {
    "gita": {
        "name": {"en": "the Bhagavad Gita", "pt": "a Bhagavad Gita"},
        "line": {
            "en": "the battlefield as the inner field.",
            "pt": "o campo de batalha como campo interior.",
        },
    },
}


def load_passages() -> list[dict]:
    passages: list[dict] = []
    for path in sorted(LIBRARY_DIR.glob("*.json")):
        if path.name == "catalog.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_file"] = path.stem
        passages.append(data)
    return passages


def shelf_id_for_passage(data: dict) -> str:
    passage_id = str(data.get("passage_id", ""))
    if passage_id.startswith("gita."):
        return "gita"
    work = data.get("work", {})
    en = str(work.get("en", "")).lower()
    if "gita" in en:
        return "gita"
    return passage_id.split(".")[0] if passage_id else data["_file"]


def count_source_files(collection: str) -> int:
    root = SOURCES_DIR / collection.replace("_", "/")
    if not root.exists():
        # try direct path (bhagavad_gita)
        root = SOURCES_DIR / collection
    if not root.exists():
        return 0
    return sum(1 for _ in root.rglob("*.md") if _.name != "README.md")


def load_collections() -> list[dict]:
    collections: list[dict] = []
    for path in sorted(MANIFEST_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        collection = str(data.get("collection", path.stem))
        full_text_volumes = sum(1 for v in data.get("volumes", []) if v.get("full_text"))
        total_volumes = len(data.get("volumes", []))
        source_files = count_source_files(collection)
        if full_text_volumes > 0 or source_files > 0:
            state = "open" if source_files > 0 else "arriving"
        else:
            state = "arriving"
        collections.append(
            {
                "id": collection,
                "title": data.get("collection_title", collection),
                "state": state,
                "source_files": source_files,
                "volumes_full_text": full_text_volumes,
                "volumes_total": total_volumes,
                "health_sensitive": bool(data.get("health_sensitive", False)),
            }
        )
    return collections


def build_catalog() -> dict:
    passages = load_passages()
    shelves_map: dict[str, dict] = {}

    for passage in passages:
        shelf_id = shelf_id_for_passage(passage)
        meta = DEFAULT_SHELVES.get(shelf_id, {})
        entry = shelves_map.setdefault(
            shelf_id,
            {
                "id": shelf_id,
                "name": meta.get("name", {"en": shelf_id, "pt": shelf_id}),
                "line": meta.get("line", {"en": "", "pt": ""}),
                "state": "open",
                "passages": [],
            },
        )
        entry["passages"].append(passage["_file"])

    for shelf_id, meta in DEFAULT_SHELVES.items():
        if shelf_id not in shelves_map:
            shelves_map[shelf_id] = {
                "id": shelf_id,
                "name": meta["name"],
                "line": meta["line"],
                "state": "arriving",
                "passages": [],
            }

    shelves = sorted(shelves_map.values(), key=lambda s: s["id"])
    collections = load_collections()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return {
        "bundle_version": now,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "shelves": shelves,
        "collections": collections,
        "passage_count": len(passages),
    }


def stable_catalog_view(catalog: dict) -> dict:
    """Fields that should not change between runs on the same corpus."""
    return {
        "shelves": catalog.get("shelves"),
        "collections": catalog.get("collections"),
        "passage_count": catalog.get("passage_count"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write catalog.json")
    parser.add_argument("--check", action="store_true", help="Fail if catalog is stale")
    args = parser.parse_args()

    catalog = build_catalog()
    rendered = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        if not OUTPUT.exists():
            print(f"Missing {OUTPUT.relative_to(ROOT)} — run with --write")
            return 1
        existing = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if stable_catalog_view(existing) != stable_catalog_view(catalog):
            print("catalog.json is stale — run: python scripts/content/build_library_catalog.py --write")
            return 1
        print("catalog.json OK")
        return 0

    if args.write:
        OUTPUT.write_text(rendered, encoding="utf-8")
        print(f"Wrote {OUTPUT.relative_to(ROOT)} ({catalog['passage_count']} passages, {len(catalog['shelves'])} shelves)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
