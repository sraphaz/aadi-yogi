from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
UPANISHAD_ROOT = REPO_ROOT / "content" / "sources" / "upanishads"
USER_AGENT = "AadiYogi Wikisource Upanishad Importer/1.0"
SKIP_LINE_PATTERNS = (
    re.compile(r"^\.mw-parser-output", re.I),
    re.compile(r"^Public domain", re.I),
    re.compile(r"^This work (is|was)", re.I),
    re.compile(r"^Please see this document", re.I),
    re.compile(r"^Layout \d+$", re.I),
    re.compile(r"^Source means", re.I),
    re.compile(r"^←", re.I),
    re.compile(r"^→", re.I),
    re.compile(r"^\[edit\]$", re.I),
)
HEADING_PATTERN = re.compile(
    r"^(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+"
    r"(?:khanda|vallî|valli|adhyâya|adhyaya|prapâthaka|prapathaka|mundaka)\.?$",
    re.IGNORECASE,
)
CHANDOGYA_ORDINALS = {
    1: "First",
    2: "Second",
    3: "Third",
    4: "Fourth",
    5: "Fifth",
    6: "Sixth",
    7: "Seventh",
    8: "Eighth",
}
CHANDOGYA_START_MARKERS: dict[int, tuple[str, ...]] = {
    1: ("1. Let a man meditate on the syllable", "Khandas (not listed in original)"),
    2: ("1. Meditation on the whole", "Khandas (not listed in original)"),
    3: ("1. The sun is indeed the honey", "Khandas (not listed in original)"),
    4: ("1. There lived once upon a time Gânasruti", "Khandas (not listed in original)"),
    5: ("1. He who knows the oldest and the best", "Khandas (not listed in original)"),
    6: ("1. Harih, Om. There lived once Svetaketu", "Khandas (not listed in original)"),
    7: ("1. Nârada approached Sanatkumâra", "Khandas (not listed in original)"),
    8: ("1. Harih, Om. There is this city of Brahman", "Khandas (not listed in original)"),
}
CHANDOGYA_THEMES = ("om", "brahman", "self_knowledge", "teacher_student_dialogue")
CHANDOGYA_CONCEPTS = ("brahman", "atman", "om", "speech")
CHANDOGYA_USE_FOR = (
    "source_grounded_nondual_reflection",
    "om_contemplation",
    "teacher_student_dialogue",
)


@dataclass(frozen=True)
class TextConfig:
    import_key: str
    slug: str
    output_name: str
    source_id_suffix: str
    source_title: str
    title: str
    page_title: str
    start_markers: tuple[str, ...]
    page_url: str
    citation: str
    section: str = "full_text"
    author: str = "Friedrich Max Muller"
    translator: str = "Friedrich Max Muller"
    themes: tuple[str, ...] = ()
    concepts: tuple[str, ...] = ()
    use_for: tuple[str, ...] = ()
    related_sources: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def output_path(self) -> Path:
        return UPANISHAD_ROOT / self.slug / f"{self.output_name}.public_domain.md"


def build_chandogya_config(prapathaka_num: int) -> TextConfig:
    ordinal = CHANDOGYA_ORDINALS[prapathaka_num]
    prapathaka_name = f"{ordinal} Prapâthaka"
    page_title = f"Sacred Books of the East/Volume 1/Khândogya-upanishad/{prapathaka_name}"
    wiki_suffix = prapathaka_name.replace(" ", "_")
    page_url = (
        "https://en.wikisource.org/wiki/"
        f"Sacred_Books_of_the_East/Volume_1/Kh%C3%A2ndogya-upanishad/{wiki_suffix}"
    )
    output_name = f"prapathaka_{prapathaka_num:02d}"
    return TextConfig(
        import_key=f"chandogya_prapathaka_{prapathaka_num:02d}",
        slug="chandogya",
        output_name=output_name,
        source_id_suffix=f"{output_name}_public_domain_translation",
        source_title="Chandogya Upanishad",
        title=(
            f"Chandogya Upanishad - {ordinal} Prapathaka "
            "(Max Muller Public Domain Translation)"
        ),
        page_title=page_title,
        start_markers=CHANDOGYA_START_MARKERS[prapathaka_num],
        page_url=page_url,
        citation=(
            f"Friedrich Max Muller, Chandogya Upanishad, {ordinal} Prapathaka "
            "(Sacred Books of the East, Volume 1, public domain)"
        ),
        section=output_name,
        themes=CHANDOGYA_THEMES,
        concepts=CHANDOGYA_CONCEPTS,
        use_for=CHANDOGYA_USE_FOR,
        related_sources=("upanishads/chandogya/index",),
        notes=(
            f"Partial import of the {ordinal} Prapathaka from English Wikisource SBE Volume 1.",
        ),
    )


def build_text_catalog() -> dict[str, TextConfig]:
    catalog: dict[str, TextConfig] = {
        "taittiriya": TextConfig(
            import_key="taittiriya",
            slug="taittiriya",
            output_name="full",
            source_id_suffix="full_public_domain_translation",
            source_title="Taittiriya Upanishad",
            title="Taittiriya Upanishad - Max Muller Public Domain Translation",
            page_title="Taittiriya Upanishad",
            start_markers=("Taittiryaka Upanishad", "1. HARIH, OM!"),
            page_url="https://en.wikisource.org/wiki/Taittiriya_Upanishad",
            citation="Friedrich Max Muller, Taittiriya Upanishad (public domain, SBE lineage)",
            themes=("brahman", "self_knowledge", "speech", "food", "bliss"),
            concepts=("brahman", "atman", "annamaya", "pranamaya", "ananda"),
            use_for=("source_grounded_nondual_reflection", "brahman_contemplation", "sheath_inquiry"),
            related_sources=("upanishads/taittiriya/index",),
            notes=("Imported from English Wikisource standalone witness.",),
        ),
    }
    for prapathaka_num in range(1, 9):
        config = build_chandogya_config(prapathaka_num)
        catalog[config.import_key] = config
    return catalog


TEXTS = build_text_catalog()


class TextExtractor(HTMLParser):
    BLOCK_TAGS = {"blockquote", "br", "div", "h1", "h2", "h3", "h4", "li", "p", "tr"}
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


def fetch_html(page_title: str) -> str:
    query = urllib.parse.urlencode(
        {
            "action": "parse",
            "format": "json",
            "formatversion": "2",
            "prop": "text",
            "page": page_title,
        }
    )
    url = f"https://en.wikisource.org/w/api.php?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            raise
    else:
        raise RuntimeError(f"Failed to fetch {page_title}")

    parse_payload = payload.get("parse")
    if not isinstance(parse_payload, dict) or "text" not in parse_payload:
        raise ValueError(f"Unexpected Wikisource payload for {page_title}")
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


def should_skip_line(line: str) -> bool:
    if any(pattern.search(line) for pattern in SKIP_LINE_PATTERNS):
        return True
    if line.startswith("Retrieved from "):
        return True
    if "copyright status" in line.lower():
        return True
    return False


def extract_body_lines(lines: list[str], config: TextConfig) -> list[str]:
    start_index = None
    for marker in config.start_markers:
        for index, line in enumerate(lines):
            if marker.lower() in line.lower():
                start_index = index
                break
        if start_index is not None:
            break
    if start_index is None:
        raise ValueError(f"Could not locate start marker for {config.import_key}")

    body: list[str] = []
    for line in lines[start_index:]:
        if line.startswith("Footnotes") or line.startswith("Retrieved from "):
            break
        if should_skip_line(line):
            continue
        body.append(line)
    if not body:
        raise ValueError(f"No body extracted for {config.import_key}")
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
        normalized = line.removesuffix("[edit]").strip()
        if normalized in {"Taittiryaka Upanishad", "Taittiriya Upanishad"}:
            continue
        if line.endswith("[edit]") and any(marker.lower() in line.lower() for marker in config.start_markers):
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
    frontmatter = [
        "---",
        f"id: upanishads/{config.slug}/{config.source_id_suffix}",
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
        "  - technical_ritual_instruction",
        "related_sources:",
        *yaml_list(config.related_sources, indent=2),
        "notes:",
        f"  - Public-domain translation inspected at {config.page_url}",
        *(f"  - {note}" for note in config.notes),
        "copyright_status: public_domain",
        "status: imported_public_domain",
        f'citation: "{config.citation}"',
        "---",
        "",
        f"# {config.source_title}",
        "",
        "## Public-Domain Translation",
        "",
        translation_body,
        "",
        "## Source Provenance",
        "",
        f"- Imported from {config.page_url}.",
        "",
    ]
    return "\n".join(frontmatter)


def import_text(config: TextConfig) -> Path:
    html = fetch_html(config.page_title)
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
        description="Import additional Upanishad witnesses from English Wikisource."
    )
    parser.add_argument(
        "slugs",
        nargs="*",
        choices=sorted(TEXTS),
        help="Configured import keys. Use chandogya_prapathaka_* for partial Chandogya imports.",
    )
    parser.add_argument(
        "--chandogya-all",
        action="store_true",
        help="Import all eight Chandogya prapathakas.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.chandogya_all:
        selected = [key for key in sorted(TEXTS) if key.startswith("chandogya_prapathaka_")]
    else:
        selected = args.slugs or sorted(TEXTS)
    for index, slug in enumerate(selected):
        if index:
            time.sleep(1.5)
        path = import_text(TEXTS[slug])
        print(path.relative_to(REPO_ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
