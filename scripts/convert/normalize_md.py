from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = REPO_ROOT / "content" / "sources"
DEFAULT_OUTPUT = REPO_ROOT / "content" / "processed" / "normalized_md"

FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.DOTALL)
SECTION_HEADERS = (
    "Public-Domain Translation",
    "Tamil Primary Text",
    "Chapter Scope",
    "Sanskrit",
    "Transliteration",
    "English Translation",
    "Translation",
    "Source Text",
    "Source Provenance",
    "Notes",
)


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return {}, text
    data = yaml.safe_load(match.group(1)) or {}
    body = text[match.end() :]
    if not isinstance(data, dict):
        raise ValueError("Frontmatter must be a mapping.")
    return data, body


def extract_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []

    for line in body.splitlines():
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = line[3:].strip()
            buffer = []
            continue
        if current is not None:
            buffer.append(line)

    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return sections


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def build_normalized_markdown(source_path: Path, frontmatter: dict[str, object], sections: dict[str, str]) -> str:
    primary_keys = [
        "Public-Domain Translation",
        "Tamil Primary Text",
        "Translation",
        "English Translation",
        "Source Text",
        "Chapter Scope",
    ]
    primary_text = ""
    for key in primary_keys:
        if sections.get(key):
            primary_text = sections[key]
            break
    if not primary_text:
        combined_keys = ("English Translation", "Sanskrit", "Transliteration")
        parts = [sections[key] for key in combined_keys if sections.get(key)]
        primary_text = "\n\n".join(parts)

    meta = dict(frontmatter)
    meta["normalized_from"] = source_path.as_posix()
    meta["normalized_sections"] = list(sections.keys())

    lines = ["---", yaml.safe_dump(meta, sort_keys=False).strip(), "---", ""]
    lines.append(f"# {frontmatter.get('title', source_path.stem)}")
    lines.append("")
    lines.append("## Normalized Primary Text")
    lines.append("")
    lines.append(normalize_whitespace(primary_text))
    lines.append("")

    if sections.get("Source Provenance"):
        lines.extend(["## Source Provenance", "", sections["Source Provenance"], ""])
    if sections.get("Notes"):
        lines.extend(["## Notes", "", sections["Notes"], ""])

    return "\n".join(lines).strip() + "\n"


def normalize_file(source_path: Path, output_root: Path, input_root: Path) -> Path | None:
    if source_path.name == "README.md" or ".template." in source_path.name:
        return None
    if not source_path.name.endswith(".md"):
        return None
    if "index.md" in source_path.name and "full.public_domain" not in source_path.name:
        return None

    text = source_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    if not frontmatter:
        return None
    if frontmatter.get("status") not in {"imported_public_domain", "approved"}:
        return None

    sections = extract_sections(body)
    if not any(sections.get(k) for k in SECTION_HEADERS):
        return None

    relative = source_path.relative_to(input_root)
    output_path = output_root / relative
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_normalized_markdown(source_path, frontmatter, sections),
        encoding="utf-8",
    )
    return output_path


def normalize_tree(input_root: Path, output_root: Path) -> list[Path]:
    written: list[Path] = []
    for source_path in sorted(input_root.rglob("*.md")):
        result = normalize_file(source_path, output_root, input_root)
        if result:
            written.append(result)
    return written


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize imported Markdown sources for downstream chunking.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    written = normalize_tree(args.input.resolve(), args.output.resolve())
    for path in written:
        print(path.relative_to(REPO_ROOT).as_posix())
    print(f"Normalized {len(written)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
