from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "validate" / "validate_markdown.py"
)
SPEC = importlib.util.spec_from_file_location("validate_markdown", MODULE_PATH)
assert SPEC and SPEC.loader
validate_markdown = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_markdown)


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_valid_source_file(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    write_markdown(
        content_root / "sources" / "upanishads" / "valid.md",
        """---
id: upanishads/valid
title: Valid Source
source_type: primary_text
tradition:
  - upanishadic
themes:
  - self_knowledge
status: template
citation: "Valid Citation"
copyright_status: verify
---
""",
    )

    assert validate_markdown.validate_content(content_root) == []


def test_missing_frontmatter_in_sources_fails(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    write_markdown(content_root / "sources" / "upanishads" / "missing.md", "# Missing")

    errors = validate_markdown.validate_content(content_root)

    assert any("missing YAML frontmatter" in error for error in errors)


def test_missing_required_field_fails(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    write_markdown(
        content_root / "sources" / "gita" / "missing_title.md",
        """---
id: gita/missing_title
source_type: translation
tradition:
  - gita
themes:
  - action
status: draft
---
""",
    )

    errors = validate_markdown.validate_content(content_root)

    assert any("missing required field 'title'" in error for error in errors)


def test_primary_text_without_citation_fails(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    write_markdown(
        content_root / "sources" / "gita" / "missing_citation.md",
        """---
id: gita/missing_citation
title: Missing Citation
source_type: primary_text
tradition:
  - gita
themes:
  - action
status: draft
copyright_status: verify
---
""",
    )

    errors = validate_markdown.validate_content(content_root)

    assert any("primary_text requires 'citation'" in error for error in errors)


def test_primary_text_without_copyright_status_fails(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    write_markdown(
        content_root / "sources" / "gita" / "missing_copyright.md",
        """---
id: gita/missing_copyright
title: Missing Copyright
source_type: primary_text
tradition:
  - gita
themes:
  - action
status: draft
citation: "Some Citation"
---
""",
    )

    errors = validate_markdown.validate_content(content_root)

    assert any("primary_text requires 'copyright_status'" in error for error in errors)


def test_documentation_like_content_can_omit_frontmatter(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    write_markdown(content_root / "ontology" / "notes.md", "# Notes")

    assert validate_markdown.validate_content(content_root) == []
