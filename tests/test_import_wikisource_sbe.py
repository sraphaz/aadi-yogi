from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "ingest"
    / "import_wikisource_sbe.py"
)
SPEC = importlib.util.spec_from_file_location("import_wikisource_sbe", MODULE_PATH)
assert SPEC and SPEC.loader
import_wikisource_sbe = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = import_wikisource_sbe
SPEC.loader.exec_module(import_wikisource_sbe)


def test_html_to_lines_strips_style_and_joins_wrapped_text() -> None:
    html = """
    <style>.mw-parser-output{display:none;}</style>
    <div>
      <p>KATHA-UPANISHAD.</p>
      <p>3. He by whom it is not thought,\nby him it is thought.</p>
    </div>
    """

    lines = import_wikisource_sbe.html_to_lines(html)

    assert ".mw-parser-output" not in lines
    assert "3. He by whom it is not thought, by him it is thought." in lines


def test_extract_body_lines_uses_title_and_stops_before_footnotes() -> None:
    config = import_wikisource_sbe.TEXTS["kena"]
    lines = [
        "preamble",
        "TALAVAKÂRA-UPANISHAD.",
        "First Khanda.",
        "1. Verse.",
        "Footnotes",
        "ignored",
    ]

    body = import_wikisource_sbe.extract_body_lines(lines, config)

    assert body == ["TALAVAKÂRA-UPANISHAD.", "First Khanda.", "1. Verse."]


def test_extract_body_lines_stops_before_scholar_footnotes() -> None:
    config = import_wikisource_sbe.TEXTS["mundaka"]
    lines = [
        "preamble",
        "MUNDAKA-UPANISHAD.",
        "First Mundaka.",
        "1. Verse.",
        "↑ A scholar footnote.",
        "ignored",
    ]

    body = import_wikisource_sbe.extract_body_lines(lines, config)

    assert body == ["MUNDAKA-UPANISHAD.", "First Mundaka.", "1. Verse."]


def test_render_translation_body_formats_section_headings() -> None:
    config = import_wikisource_sbe.TEXTS["katha"]
    body_lines = [
        "KATHA-UPANISHAD.",
        "FIRST ADHYÂYA.",
        "SECOND Vallî",
        "1. Verse.",
    ]

    rendered = import_wikisource_sbe.render_translation_body(body_lines, config)

    assert "KATHA-UPANISHAD." not in rendered
    assert "### FIRST ADHYÂYA." in rendered
    assert "### SECOND Vallî" in rendered
    assert "1. Verse." in rendered


def test_render_translation_body_splits_embedded_verse_markers() -> None:
    config = import_wikisource_sbe.TEXTS["katha"]
    body_lines = [
        "KATHA-UPANISHAD.",
        '(A narrative note ends here:) 7. "Fire enters into the houses."',
    ]

    rendered = import_wikisource_sbe.render_translation_body(body_lines, config)

    assert "(A narrative note ends here:)" in rendered
    assert '7. "Fire enters into the houses."' in rendered
