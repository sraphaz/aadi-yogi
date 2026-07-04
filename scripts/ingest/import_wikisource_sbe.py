from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
UPANISHAD_ROOT = REPO_ROOT / "content" / "sources" / "upanishads"
USER_AGENT = "Codex AadiYogi Wikisource Importer/1.0"
FOOTNOTE_MARKER = "Footnotes"
SCHOLAR_FOOTNOTE_MARKER = "↑"
HEADING_PATTERN = re.compile(
    r"^(?:first|second|third|fourth|fifth|sixth|seventh)\s+"
    r"(?:khanda|vallî|valli|adhyâya|adhyaya|mundaka)\.?$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class TextConfig:
    slug: str
    source_title: str
    title: str
    title_line: str
    page_url: str
    volume_url: str
    citation: str
    source_locator: dict[str, str]
    section: str = "full_text"
    author: str = "Friedrich Max Muller"
    translator: str = "Friedrich Max Muller"
    themes: tuple[str, ...] = ()
    concepts: tuple[str, ...] = ()
    use_for: tuple[str, ...] = ()
    avoid_for: tuple[str, ...] = ("technical_ritual_instruction",)
    related_sources: tuple[str, ...] = ()
    historical_note: str = (
        "This is a historical public-domain translation imported as a stable witness for "
        "intake, citation, and later comparison against additional editions."
    )

    @property
    def output_path(self) -> Path:
        return UPANISHAD_ROOT / self.slug / "full.public_domain.md"


TEXTS: dict[str, TextConfig] = {
    "kena": TextConfig(
        slug="kena",
        source_title="Kena Upanishad",
        title="Kena Upanishad - Max Muller 1879 Public Domain Translation",
        title_line="TALAVAKARA-UPANISHAD.",
        page_url=(
            "https://en.wikisource.org/wiki/"
            "Sacred_Books_of_the_East/Volume_1/Talavak%C3%A2ra-upanishad"
        ),
        volume_url="https://en.wikisource.org/wiki/Sacred_Books_of_the_East/Volume_1",
        citation=(
            "Friedrich Max Muller, The Upanishads, Part 1 (SBE 1), "
            "Talavakara-Upanishad (Kena Upanishad), 1879"
        ),
        source_locator={"pageid": "1371607"},
        themes=("self_knowledge", "brahman", "divine_agency", "immortality"),
        concepts=("brahman", "atman", "knowledge", "mind"),
        use_for=("source_grounded_nondual_reflection", "brahman_inquiry", "teacher_student_dialogue"),
        related_sources=("upanishads/kena/index",),
    ),
    "katha": TextConfig(
        slug="katha",
        source_title="Katha Upanishad",
        title="Katha Upanishad - Max Muller 1884 Public Domain Translation",
        title_line="KATHA-UPANISHAD.",
        page_url=(
            "https://en.wikisource.org/wiki/"
            "Sacred_Books_of_the_East/Volume_15/Katha-upanishad"
        ),
        volume_url="https://en.wikisource.org/wiki/Sacred_Books_of_the_East/Volume_15",
        citation=(
            "Friedrich Max Muller, The Upanishads, Part 2 (SBE 15), "
            "Katha Upanishad, 1884"
        ),
        source_locator={"page": "Sacred Books of the East/Volume 15/Katha-upanishad"},
        themes=("death", "self_knowledge", "renunciation", "discernment"),
        concepts=("atman", "brahman", "yama", "immortality"),
        use_for=("source_grounded_nondual_reflection", "discernment_of_good_and_pleasant", "death_dialogue"),
        related_sources=("upanishads/katha/index",),
    ),
    "mundaka": TextConfig(
        slug="mundaka",
        source_title="Mundaka Upanishad",
        title="Mundaka Upanishad - Max Muller 1884 Public Domain Translation",
        title_line="MUNDAKA-UPANISHAD.",
        page_url=(
            "https://en.wikisource.org/wiki/"
            "Sacred_Books_of_the_East/Volume_15/Mundaka-upanishad"
        ),
        volume_url="https://en.wikisource.org/wiki/Sacred_Books_of_the_East/Volume_15",
        citation=(
            "Friedrich Max Muller, The Upanishads, Part 2 (SBE 15), "
            "Mundaka Upanishad, 1884"
        ),
        source_locator={"page": "Sacred Books of the East/Volume 15/Mundaka-upanishad"},
        themes=("higher_knowledge", "brahman", "renunciation", "self_knowledge"),
        concepts=("brahman", "atman", "knowledge", "renunciation"),
        use_for=("source_grounded_nondual_reflection", "higher_and_lower_knowledge", "brahman_contemplation"),
        related_sources=("upanishads/mundaka/index",),
    ),
}


class TextExtractor(HTMLParser):
    BLOCK_TAGS = {
        "blockquote",
        "br",
        "div",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "li",
        "ol",
        "p",
        "section",
        "table",
        "tr",
        "ul",
    }
    SKIP_TAGS = {"script", "style"}

    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
            return
        if not self._skip_depth and tag in self.BLOCK_TAGS:
            self._parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS:
            if self._skip_depth:
                self._skip_depth -= 1
            return
        if not self._skip_depth and tag in self.BLOCK_TAGS:
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            self._parts.append(data.replace("\r", " ").replace("\n", " "))

    def get_text(self) -> str:
        return "".join(self._parts)


def fetch_wikisource_html(config: TextConfig) -> str:
    query = {
        "action": "parse",
        "format": "json",
        "formatversion": "2",
        "prop": "text",
        **config.source_locator,
    }
    url = "https://en.wikisource.org/w/api.php?" + urllib.parse.urlencode(query)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    parse_payload = payload.get("parse")
    if not isinstance(parse_payload, dict) or "text" not in parse_payload:
        raise ValueError(f"Unexpected Wikisource payload for {config.slug}")
    return str(parse_payload["text"])


def normalize_line(line: str) -> str:
    line = line.replace("\xa0", " ").replace("\u200b", "")
    line = re.sub(r"\[\s*\d+\s*\]", "", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def html_to_lines(html: str) -> list[str]:
    extractor = TextExtractor()
    extractor.feed(html)
    lines = [normalize_line(line) for line in extractor.get_text().splitlines()]
    return [line for line in lines if line]


def matches_title_line(line: str, title_line: str) -> bool:
    normalized = unicodedata.normalize("NFKD", line)
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    target = unicodedata.normalize("NFKD", title_line)
    target = "".join(char for char in target if not unicodedata.combining(char))
    return normalized == target


def extract_body_lines(lines: list[str], config: TextConfig) -> list[str]:
    start_index = next(
        (index for index, line in enumerate(lines) if matches_title_line(line, config.title_line)),
        None,
    )
    if start_index is None:
        raise ValueError(f"Could not locate title marker for {config.slug}")

    body: list[str] = []
    for line in lines[start_index:]:
        if (
            line.startswith(FOOTNOTE_MARKER)
            or line.startswith(SCHOLAR_FOOTNOTE_MARKER)
            or line.startswith("Retrieved from ")
        ):
            break
        body.append(line)

    if not body:
        raise ValueError(f"No body extracted for {config.slug}")
    return body


def render_line(line: str) -> str | None:
    if HEADING_PATTERN.match(line):
        return f"### {line}"
    return line


def split_embedded_verse_marker(line: str) -> list[str]:
    match = re.search(r"(?<!^)\s+(\d+\.\s)", line)
    if not match:
        return [line]

    prefix = line[: match.start(1)].rstrip()
    suffix = line[match.start(1) :].lstrip()
    if prefix.endswith(('"', ")", ":", ";")):
        return [prefix, suffix]
    return [line]


def render_translation_body(body_lines: list[str], config: TextConfig) -> str:
    rendered: list[str] = []
    for line in body_lines:
        if matches_title_line(line, config.title_line):
            continue
        for fragment in split_embedded_verse_marker(line):
            output = render_line(fragment)
            if output is None:
                continue
            rendered.append(output)

    return "\n\n".join(rendered).strip()


def yaml_list(items: tuple[str, ...], indent: int = 0) -> list[str]:
    prefix = " " * indent
    return [f"{prefix}- {item}" for item in items]


def build_markdown(config: TextConfig, translation_body: str) -> str:
    frontmatter: list[str] = [
        "---",
        f"id: upanishads/{config.slug}/full_public_domain_translation",
        f"title: {config.title}",
        f"source_title: {config.source_title}",
        "source_type: primary_text",
        "tradition:",
        *yaml_list(("upanishadic",), indent=2),
        f"author: {config.author}",
        f"section: {config.section}",
        "language_original: sanskrit",
        "language_current: english",
        f"translator: {config.translator}",
        "themes:",
        *yaml_list(config.themes, indent=2),
        "concepts:",
        *yaml_list(config.concepts, indent=2),
        "use_for:",
        *yaml_list(config.use_for, indent=2),
        "avoid_for:",
        *yaml_list(config.avoid_for, indent=2),
        "related_sources:",
        *yaml_list(config.related_sources, indent=2),
        "notes:",
        f"  - Public-domain translation inspected at {config.page_url}",
        f"  - Volume page inspected at {config.volume_url}",
        "  - Imported from the English Wikisource witness of Sacred Books of the East.",
        "copyright_status: public_domain",
        "status: imported_public_domain",
        f'citation: "{config.citation}"',
        "---",
        "",
    ]
    sections = [
        f"# {config.source_title} - Max Muller Translation",
        "",
        "## Public-Domain Translation",
        "",
        translation_body,
        "",
        "## Source Provenance",
        "",
        f"- Imported from {config.page_url}.",
        f"- Volume witness inspected at {config.volume_url}.",
        "",
        "## Notes",
        "",
        config.historical_note,
        "",
    ]
    return "\n".join(frontmatter + sections)


def import_text(config: TextConfig) -> Path:
    html = fetch_wikisource_html(config)
    lines = html_to_lines(html)
    body_lines = extract_body_lines(lines, config)
    translation_body = render_translation_body(body_lines, config)
    markdown = build_markdown(config, translation_body)
    output_path = config.output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import public-domain SBE Upanishad witnesses from English Wikisource."
    )
    parser.add_argument(
        "slugs",
        nargs="*",
        choices=sorted(TEXTS),
        help="Configured text slugs to import. Defaults to all configured texts.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    selected = args.slugs or sorted(TEXTS)

    for slug in selected:
        path = import_text(TEXTS[slug])
        print(path.relative_to(REPO_ROOT).as_posix())

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
