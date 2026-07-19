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
        "source_dirs": ["content/sources/bhagavad_gita"],
    },
    "upanishads": {
        "name": {"en": "the Upanishads", "pt": "as Upanishads"},
        "line": {
            "en": "seer texts on the Self — arriving as witnesses land.",
            "pt": "textos dos videntes sobre o Self — chegando conforme entram testemunhas.",
        },
        "source_dirs": ["content/sources/upanishads"],
    },
    "integral_yoga": {
        "name": {"en": "Sri Aurobindo", "pt": "Sri Aurobindo"},
        "line": {
            "en": "integral yoga in prose and verse — arriving room by room.",
            "pt": "yoga integral em prosa e verso — sala a sala, enquanto chega.",
        },
        "source_dirs": ["content/sources/sri_aurobindo/complete_works"],
    },
}

SHELF_TRADITIONS: dict[str, list[str]] = {
    "gita": ["gita", "vedantic"],
    "upanishads": ["upanishadic"],
    "integral_yoga": ["integral_yoga"],
}


def traditions_for_shelf(shelf_id: str) -> list[str]:
    return list(SHELF_TRADITIONS.get(shelf_id, [shelf_id]))


def traditions_for_passage(passage: dict, shelf_id: str) -> list[str]:
    explicit = passage.get("traditions")
    if isinstance(explicit, list) and explicit:
        return [str(t) for t in explicit]
    return traditions_for_shelf(shelf_id)


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


def count_md_files(root: Path) -> int:
    if not root.exists():
        return 0
    return sum(1 for p in root.rglob("*.md") if p.name not in ("README.md", "index.md"))


def count_source_files(collection: str, manifest: dict | None = None) -> int:
    if manifest and manifest.get("content_dir"):
        return count_md_files(ROOT / str(manifest["content_dir"]))
    for shelf in DEFAULT_SHELVES.values():
        for rel in shelf.get("source_dirs", []):
            if collection.replace("_", "/") in rel or rel.endswith(collection):
                return count_md_files(ROOT / rel)
    root = SOURCES_DIR / collection.replace("_", "/")
    if not root.exists():
        root = SOURCES_DIR / collection
    return count_md_files(root)


def load_facets(
    manifests: list[dict],
    shelves: list[dict],
    browse_entries: list[dict],
) -> list[dict]:
    counts: dict[str, int] = {}
    for data in manifests:
        for raw in data.get("tradition") or []:
            key = str(raw)
            counts[key] = counts.get(key, 0) + 1
    for shelf in shelves:
        weight = max(1, len(shelf.get("passages") or []))
        for tradition in traditions_for_shelf(str(shelf["id"])):
            counts[tradition] = counts.get(tradition, 0) + weight
    for entry in browse_entries:
        for tradition in entry.get("traditions") or []:
            counts[str(tradition)] = counts.get(str(tradition), 0) + 1
    return [
        {"type": "tradition", "id": key, "count": counts[key]}
        for key in sorted(counts)
    ]


def build_browse_entries(passages: list[dict]) -> list[dict]:
    entries: list[dict] = []
    for passage in passages:
        shelf_id = shelf_id_for_passage(passage)
        depths = passage.get("depths") or {}
        preview = depths.get("d0") or depths.get("d1") or {}
        entries.append(
            {
                "id": passage["_file"],
                "passage_id": passage.get("passage_id"),
                "shelf": shelf_id,
                "traditions": traditions_for_passage(passage, shelf_id),
                "work": passage.get("work", {}),
                "preview": preview,
            }
        )
    return sorted(entries, key=lambda item: str(item.get("passage_id") or item["id"]))


def load_collections() -> tuple[list[dict], list[dict]]:
    collections: list[dict] = []
    manifests: list[dict] = []
    for path in sorted(MANIFEST_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        manifests.append(data)
        collection = str(data.get("collection", path.stem))
        full_text_volumes = sum(1 for v in data.get("volumes", []) if v.get("full_text"))
        total_volumes = len(data.get("volumes", []))
        source_files = count_source_files(collection, data)
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
                "traditions": list(data.get("tradition") or []),
            }
        )
    return collections, manifests


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
        entry["traditions"] = traditions_for_passage(passage, shelf_id)

    for shelf_id, meta in DEFAULT_SHELVES.items():
        if shelf_id not in shelves_map:
            source_count = sum(count_md_files(ROOT / rel) for rel in meta.get("source_dirs", []))
            shelves_map[shelf_id] = {
                "id": shelf_id,
                "name": meta["name"],
                "line": meta["line"],
                "state": "open" if source_count > 0 and shelf_id == "gita" else ("arriving" if source_count > 0 else "future"),
                "passages": [],
                "source_files": source_count,
                "traditions": traditions_for_shelf(shelf_id),
            }
        elif "traditions" not in shelves_map[shelf_id]:
            shelves_map[shelf_id]["traditions"] = traditions_for_shelf(shelf_id)

    shelves = sorted(shelves_map.values(), key=lambda s: s["id"])
    collections, manifests = load_collections()
    browse_entries = build_browse_entries(passages)
    facets = load_facets(manifests, shelves, browse_entries)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return {
        "bundle_version": now,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "shelves": shelves,
        "facets": facets,
        "browse_entries": browse_entries,
        "collections": collections,
        "passage_count": len(passages),
    }


def stable_catalog_view(catalog: dict) -> dict:
    """Fields that should not change between runs on the same corpus."""
    return {
        "shelves": catalog.get("shelves"),
        "facets": catalog.get("facets"),
        "browse_entries": catalog.get("browse_entries"),
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
