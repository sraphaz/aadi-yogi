from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from packages.rag.vector_store import DEFAULT_INDEX_PATH, TfidfVectorStore, load_records_from_jsonl  # noqa: E402
DEFAULT_CHUNK_ROOT = REPO_ROOT / "data" / "chunks"


def build_index(chunk_root: Path, output_path: Path) -> int:
    records = load_records_from_jsonl(chunk_root)
    store = TfidfVectorStore()
    store.build_from_records(records)
    store.save(output_path)
    return len(store.chunks)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build TF-IDF vector index from chunked JSONL corpus.")
    parser.add_argument("--input", type=Path, default=DEFAULT_CHUNK_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_INDEX_PATH)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    count = build_index(args.input.resolve(), args.output.resolve())
    print(f"Built vector index with {count} chunks at {args.output.resolve().relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
