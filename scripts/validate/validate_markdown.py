from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REQUIRED_FIELDS = ("id", "title", "source_type", "tradition", "themes", "status")
PRIMARY_TEXT_FIELDS = ("citation", "copyright_status")
ALLOWED_NO_FRONTMATTER_PREFIXES = (
    "content/consciousness_core/",
    "content/ontology/",
    "content/synthesis/",
)
FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.DOTALL)


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") or text.startswith("---\r\n")


def parse_frontmatter(text: str) -> dict[str, object] | None:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return None

    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        raise ValueError("YAML frontmatter must parse to a mapping.")
    return data


def can_omit_frontmatter(relative_path: str) -> bool:
    return relative_path.startswith(ALLOWED_NO_FRONTMATTER_PREFIXES)


def validate_file(file_path: Path, repo_root: Path) -> list[str]:
    relative_path = file_path.relative_to(repo_root).as_posix()

    if file_path.name == "README.md":
        return []

    text = file_path.read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(text)
    except (ValueError, yaml.YAMLError) as exc:
        return [f"{relative_path}: invalid YAML frontmatter ({exc})."]

    if relative_path.startswith("content/sources/"):
        if frontmatter is None:
            return [f"{relative_path}: missing YAML frontmatter."]
    elif frontmatter is None and can_omit_frontmatter(relative_path):
        return []

    if frontmatter is None:
        return []

    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        value = frontmatter.get(field)
        if value in (None, "", []):
            errors.append(f"{relative_path}: missing required field '{field}'.")

    if frontmatter.get("source_type") == "primary_text":
        for field in PRIMARY_TEXT_FIELDS:
            value = frontmatter.get(field)
            if value in (None, "", []):
                errors.append(f"{relative_path}: primary_text requires '{field}'.")

    return errors


def validate_content(content_root: Path) -> list[str]:
    repo_root = content_root.parent
    errors: list[str] = []

    for file_path in sorted(content_root.rglob("*.md")):
        errors.extend(validate_file(file_path, repo_root))

    return errors


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parents[2]
    content_root = Path(argv[1]).resolve() if len(argv) > 1 else repo_root / "content"

    if not content_root.exists():
        print(f"Content root not found: {content_root}")
        return 1

    errors = validate_content(content_root)
    if errors:
        print("Markdown validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Markdown validation passed for {content_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
