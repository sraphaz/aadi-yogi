from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from packages.rag.dense_vector_store import (  # noqa: E402
    DEFAULT_DENSE_INDEX_PATH,
    DenseVectorStore,
    build_dense_index,
)
from packages.rag.embeddings import get_embedding_provider  # noqa: E402
from packages.rag.qdrant_adapter import (  # noqa: E402
    export_qdrant_jsonl,
    sync_dense_store_to_qdrant,
)


DEFAULT_CHUNK_ROOT = REPO_ROOT / "data" / "chunks"
DEFAULT_QDRANT_EXPORT = REPO_ROOT / "data" / "indexes" / "qdrant_points.jsonl"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build dense embedding index and optional Qdrant sync.")
    parser.add_argument("--input", type=Path, default=DEFAULT_CHUNK_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_DENSE_INDEX_PATH)
    parser.add_argument("--qdrant-export", type=Path, default=DEFAULT_QDRANT_EXPORT)
    parser.add_argument("--prefer-openai", action="store_true")
    parser.add_argument("--sync-qdrant", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    provider = get_embedding_provider(prefer_openai=args.prefer_openai)
    count = build_dense_index(args.input.resolve(), args.output.resolve(), provider=provider)
    print(
        f"Built dense index with {count} chunks using provider={provider.name} "
        f"at {args.output.resolve().relative_to(REPO_ROOT)}"
    )

    store = DenseVectorStore.load(args.output.resolve())
    export_qdrant_jsonl(store, args.qdrant_export.resolve())
    print(f"Exported Qdrant JSONL to {args.qdrant_export.resolve().relative_to(REPO_ROOT)}")

    if args.sync_qdrant:
        upserted = sync_dense_store_to_qdrant(store)
        print(f"Upserted {upserted} points into Qdrant collection.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
