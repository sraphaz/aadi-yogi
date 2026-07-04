from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = REPO_ROOT / "data" / "chunks"
DEFAULT_OUTPUT = REPO_ROOT / "content" / "processed" / "embeddings_ready"


def prepare_embeddings(input_root: Path, output_root: Path) -> list[Path]:
    written: list[Path] = []
    manifest: list[dict[str, object]] = []

    for jsonl_path in sorted(input_root.rglob("*.jsonl")):
        relative = jsonl_path.relative_to(input_root)
        output_path = output_root / relative
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(jsonl_path, output_path)
        written.append(output_path)

        with jsonl_path.open(encoding="utf-8") as handle:
            for line in handle:
                record = json.loads(line)
                manifest.append(
                    {
                        "chunk_id": record.get("chunk_id"),
                        "source_id": record.get("source_id"),
                        "source_path": record.get("source_path"),
                        "copyright_status": (record.get("metadata") or {}).get("copyright_status"),
                    }
                )

    manifest_path = output_root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    written.append(manifest_path)
    return written


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare embeddings-ready JSONL artifacts.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    written = prepare_embeddings(args.input.resolve(), args.output.resolve())
    for path in written:
        print(path.relative_to(REPO_ROOT).as_posix())
    print(f"Prepared {len(written)} embeddings-ready artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
