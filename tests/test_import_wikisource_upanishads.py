from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "ingest"
    / "import_wikisource_upanishads.py"
)
SPEC = importlib.util.spec_from_file_location("import_wikisource_upanishads", MODULE_PATH)
assert SPEC and SPEC.loader
import_wikisource_upanishads = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = import_wikisource_upanishads
SPEC.loader.exec_module(import_wikisource_upanishads)


def test_extract_body_lines_skips_boilerplate_without_stopping_early() -> None:
    config = import_wikisource_upanishads.TEXTS["taittiriya"]
    lines = [
        "Public domainPublic domainfalsefalse",
        "Taittiryaka Upanishad[edit]",
        "1. HARIH, OM! May Mitra be propitious to us.",
        "Footnotes",
        "ignored",
    ]

    body = import_wikisource_upanishads.extract_body_lines(lines, config)

    assert "1. HARIH, OM! May Mitra be propitious to us." in body
    assert "Footnotes" not in body


def test_render_translation_body_drops_title_heading() -> None:
    config = import_wikisource_upanishads.TEXTS["taittiriya"]
    body_lines = [
        "Taittiryaka Upanishad[edit]",
        "1. Adoration to Brahman!",
    ]

    rendered = import_wikisource_upanishads.render_translation_body(body_lines, config)

    assert "Taittiryaka Upanishad" not in rendered
    assert "1. Adoration to Brahman!" in rendered
