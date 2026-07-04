from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = REPO_ROOT / "content" / "processed" / "normalized_md"
DEFAULT_OUTPUT = REPO_ROOT / "content" / "processed" / "chunked"
DATA_OUTPUT = REPO_ROOT / "data" / "chunks"

FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.DOTALL)
CHUNK_SIZE = 900
CHUNK_OVERLAP = 120


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return {}, text
    data = yaml.safe_load(match.group(1)) or {}
    body = text[match.end() :]
    if not isinstance(data, dict):
        raise ValueError("Frontmatter must be a mapping.")
    return data, body


def extract_primary_text(body: str) -> str:
    match = re.search(r"## Normalized Primary Text\s*\n+(.*?)(?:\n## |\Z)", body, re.DOTALL)
    if match:
        return match.group(1).strip()
    return body.strip()


def split_paragraphs(text: str) -> list[str]:
    parts = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    return parts or [text.strip()]


def chunk_paragraphs(paragraphs: list[str], size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= size:
            current = candidate
            continue
        if current:
            chunks.append(current)
        if len(paragraph) <= size:
            current = paragraph
            continue
        start = 0
        while start < len(paragraph):
            end = min(start + size, len(paragraph))
            chunks.append(paragraph[start:end].strip())
            if end >= len(paragraph):
                break
            start = max(end - overlap, start + 1)
        current = ""

    if current:
        chunks.append(current)
    return chunks


def chunk_id(source_id: str, index: int) -> str:
    digest = hashlib.sha1(f"{source_id}:{index}".encode()).hexdigest()[:12]
    return f"{source_id}#chunk_{index:04d}_{digest}"


def build_chunk_records(source_path: Path, frontmatter: dict[str, object], body: str) -> list[dict[str, object]]:
    source_id = str(frontmatter.get("id", source_path.stem))
    primary_text = extract_primary_text(body)
    paragraphs = split_paragraphs(primary_text)
    text_chunks = chunk_paragraphs(paragraphs)

    records: list[dict[str, object]] = []
    for index, chunk_text in enumerate(text_chunks):
        records.append(
            {
                "chunk_id": chunk_id(source_id, index),
                "source_id": source_id,
                "source_path": source_path.as_posix(),
                "chunk_index": index,
                "text": chunk_text,
                "metadata": {
                    "title": frontmatter.get("title"),
                    "source_title": frontmatter.get("source_title"),
                    "source_type": frontmatter.get("source_type"),
                    "tradition": frontmatter.get("tradition"),
                    "themes": frontmatter.get("themes"),
                    "concepts": frontmatter.get("concepts"),
                    "copyright_status": frontmatter.get("copyright_status"),
                    "citation": frontmatter.get("citation"),
                    "status": frontmatter.get("status"),
                },
            }
        )
    return records


def chunk_file(source_path: Path, output_root: Path, data_root: Path, input_root: Path) -> Path | None:
    text = source_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    if not frontmatter:
        return None

    records = build_chunk_records(source_path, frontmatter, body)
    if not records:
        return None

    relative = source_path.relative_to(input_root)
    jsonl_path = output_root / relative.with_suffix(".jsonl")
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    data_path = data_root / relative.with_suffix(".jsonl")
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(jsonl_path.read_text(encoding="utf-8"), encoding="utf-8")
    return jsonl_path


def chunk_tree(input_root: Path, output_root: Path, data_root: Path) -> list[Path]:
    written: list[Path] = []
    for source_path in sorted(input_root.rglob("*.md")):
        result = chunk_file(source_path, output_root, data_root, input_root)
        if result:
            written.append(result)
    return written


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create semantic chunks from normalized Markdown.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--data-output", type=Path, default=DATA_OUTPUT)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    written = chunk_tree(args.input.resolve(), args.output.resolve(), args.data_output.resolve())
    total_chunks = 0
    for path in written:
        with path.open(encoding="utf-8") as handle:
            count = sum(1 for _ in handle)
        total_chunks += count
        print(f"{path.relative_to(REPO_ROOT).as_posix()} ({count} chunks)")
    print(f"Chunked {len(written)} files into {total_chunks} chunks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
