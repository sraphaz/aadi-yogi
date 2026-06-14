from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "ingest"
    / "import_ta_wikisource.py"
)
SPEC = importlib.util.spec_from_file_location("import_ta_wikisource", MODULE_PATH)
assert SPEC and SPEC.loader
import_ta_wikisource = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = import_ta_wikisource
SPEC.loader.exec_module(import_ta_wikisource)


def test_normalize_wikitext_strips_header_and_categories() -> None:
    raw_text = """{{header
 | title = Test
}}
{{featured download}}
==Skip==
[[பகுப்பு:Foo]]
==திருமூலர் அருளிய திருமந்திரம்==
Intro line
[[பகுப்பு:Bar]]
"""

    lines = import_ta_wikisource.normalize_wikitext(
        raw_text,
        start_heading="திருமூலர் அருளிய திருமந்திரம்",
    )

    assert "Skip" not in "\n".join(lines)
    assert "பகுப்பு" not in "\n".join(lines)
    assert lines[0] == "## திருமூலர் அருளிய திருமந்திரம்"
    assert "Intro line" in lines


def test_normalize_wikitext_converts_links_headings_and_breaks() -> None:
    raw_text = """{{header
 | title = Test
}}
==திருமூலர் அருளிய திருமந்திரம்==
===1.கடவுள் வாழ்த்து===
1.<br />[[திருமந்திரம்|ஒன்றவன்]]<br />இரண்டவன்
"""

    lines = import_ta_wikisource.normalize_wikitext(
        raw_text,
        start_heading="திருமூலர் அருளிய திருமந்திரம்",
    )

    assert "## திருமூலர் அருளிய திருமந்திரம்" in lines
    assert "### 1.கடவுள் வாழ்த்து" in lines
    assert "1." in lines
    assert "ஒன்றவன்" in lines
    assert "இரண்டவன்" in lines
