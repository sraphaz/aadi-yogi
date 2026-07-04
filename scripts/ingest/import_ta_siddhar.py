from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SIDDHA_ROOT = REPO_ROOT / "content" / "sources" / "siddha_texts"
USER_AGENT = "Codex AadiYogi Tamil Siddhar Importer/1.0"
CATEGORY_PATTERN = re.compile(r"^\[\[பகுப்பு:.*\]\]$")
HEADING_PATTERN = re.compile(r"^(=+)\s*(.*?)\s*\1$")
LINK_PATTERN = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]|\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class TextConfig:
    slug: str
    source_id: str
    source_title: str
    title: str
    page_title: str
    start_heading: str
    output_path: Path
    author: str
    section: str
    tradition: tuple[str, ...]
    themes: tuple[str, ...]
    concepts: tuple[str, ...]
    use_for: tuple[str, ...]
    related_sources: tuple[str, ...]
    notes: tuple[str, ...]

    @property
    def page_url(self) -> str:
        return f"https://ta.wikisource.org/wiki/{urllib.parse.quote(self.page_title, safe='/')}"

    @property
    def raw_url(self) -> str:
        return f"{self.page_url}?action=raw"


TEXTS: dict[str, TextConfig] = {
    "sivavakkiyar": TextConfig(
        slug="sivavakkiyar",
        source_id="siddha_texts/sivavakkiyar/full_public_domain",
        source_title="Sivavakkiyar",
        title="Sivavakkiyar - Tamil Public-Domain Witness",
        page_title="சிவவாக்கியார்",
        start_heading="சிவவாக்கியார்",
        output_path=SIDDHA_ROOT / "sivavakkiyar" / "full.public_domain.md",
        author="Sivavakkiyar",
        section="full_text",
        tradition=("siddha", "shaiva", "tamil"),
        themes=("non_dual", "devotion", "symbolism"),
        concepts=("shiva", "ego", "grace"),
        use_for=("siddha_source_grounding", "tamil_primary_text"),
        related_sources=("siddha_texts/index", "siddha_texts/sivavakkiyar/index"),
        notes=("Imported from Tamil Wikisource primary-text witness.",),
    ),
    "pattinathar": TextConfig(
        slug="pattinathar",
        source_id="siddha_texts/pattinathar/full_public_domain",
        source_title="Pattinathar",
        title="Pattinathar - Tamil Public-Domain Witness",
        page_title="பட்டினத்தார்",
        start_heading="பட்டினத்தார்",
        output_path=SIDDHA_ROOT / "pattinathar" / "full.public_domain.md",
        author="Pattinathar",
        section="full_text",
        tradition=("siddha", "shaiva", "tamil"),
        themes=("renunciation", "devotion", "symbolism"),
        concepts=("shiva", "renunciation", "grace"),
        use_for=("siddha_source_grounding", "tamil_primary_text"),
        related_sources=("siddha_texts/index", "siddha_texts/pattinathar/index"),
        notes=("Imported from Tamil Wikisource primary-text witness.",),
    ),
    "pambatti_siddhar": TextConfig(
        slug="pambatti_siddhar",
        source_id="siddha_texts/pambatti_siddhar/full_public_domain",
        source_title="Pambatti Siddhar",
        title="Pambatti Siddhar - Tamil Public-Domain Witness",
        page_title="பாம்பாட்டிச் சித்தர்",
        start_heading="பாம்பாட்டிச் சித்தர்",
        output_path=SIDDHA_ROOT / "pambatti_siddhar" / "full.public_domain.md",
        author="Pambatti Siddhar",
        section="full_text",
        tradition=("siddha", "shaiva", "tamil"),
        themes=("yoga", "symbolism", "transformation"),
        concepts=("kundalini", "shiva", "yoga"),
        use_for=("siddha_source_grounding", "tamil_primary_text"),
        related_sources=("siddha_texts/index", "siddha_texts/pambatti_siddhar/index"),
        notes=("Imported from Tamil Wikisource primary-text witness.",),
    ),
    "agathiyar_gnana_padalgal": TextConfig(
        slug="agathiyar_gnana_padalgal",
        source_id="siddha_texts/agathiyar_gnana_padalgal/full_public_domain",
        source_title="Agathiyar Gnana Padalgal",
        title="Agathiyar Gnana Padalgal - Tamil Public-Domain Witness",
        page_title="அகத்தியர் ஞானப் பாடல்கள்",
        start_heading="அகத்தியர்",
        output_path=SIDDHA_ROOT / "agathiyar_gnana_padalgal" / "full.public_domain.md",
        author="Agathiyar",
        section="full_text",
        tradition=("siddha", "shaiva", "tamil"),
        themes=("wisdom", "guru", "symbolism"),
        concepts=("agathiyar", "gnana", "grace"),
        use_for=("siddha_source_grounding", "tamil_primary_text"),
        related_sources=("siddha_texts/index", "siddha_texts/agathiyar_gnana_padalgal/index"),
        notes=("Imported from Tamil Wikisource primary-text witness.",),
    ),
    "kudhambai_siddhar": TextConfig(
        slug="kudhambai_siddhar",
        source_id="siddha_texts/kudhambai_siddhar/full_public_domain",
        source_title="Kudhambai Siddhar",
        title="Kudhambai Siddhar - Tamil Public-Domain Witness",
        page_title="குதம்பைச் சித்தர்",
        start_heading="குதம்பை",
        output_path=SIDDHA_ROOT / "kudhambai_siddhar" / "full.public_domain.md",
        author="Kudhambai Siddhar",
        section="full_text",
        tradition=("siddha", "shaiva", "tamil"),
        themes=("devotion", "symbolism", "renunciation"),
        concepts=("shiva", "grace", "renunciation"),
        use_for=("siddha_source_grounding", "tamil_primary_text"),
        related_sources=("siddha_texts/index", "siddha_texts/kudhambai_siddhar/index"),
        notes=("Imported from Tamil Wikisource primary-text witness.",),
    ),
    "idaikkattu_siddhar": TextConfig(
        slug="idaikkattu_siddhar",
        source_id="siddha_texts/idaikkattu_siddhar/full_public_domain",
        source_title="Idaikkattu Siddhar",
        title="Idaikkattu Siddhar - Tamil Public-Domain Witness",
        page_title="இடைக்காட்டுச் சித்தர்",
        start_heading="இடைக்காட்டு",
        output_path=SIDDHA_ROOT / "idaikkattu_siddhar" / "full.public_domain.md",
        author="Idaikkattu Siddhar",
        section="full_text",
        tradition=("siddha", "shaiva", "tamil"),
        themes=("forest_life", "symbolism", "devotion"),
        concepts=("shiva", "renunciation", "grace"),
        use_for=("siddha_source_grounding", "tamil_primary_text"),
        related_sources=("siddha_texts/index", "siddha_texts/idaikkattu_siddhar/index"),
        notes=("Imported from Tamil Wikisource primary-text witness.",),
    ),
}


def fetch_raw_wikitext(config: TextConfig) -> str:
    request = urllib.request.Request(config.raw_url, headers={"User-Agent": USER_AGENT})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            raise
    raise RuntimeError("Failed to fetch Tamil wikitext.")


def convert_wikilinks(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        if match.group(2):
            return match.group(2)
        return match.group(3) or match.group(1) or ""

    return LINK_PATTERN.sub(replace, text)


def normalize_inline_markup(text: str) -> str:
    text = text.replace("<br />", "\n").replace("<br/>", "\n").replace("<br>", "\n")
    text = convert_wikilinks(text)
    text = text.replace("'''", "").replace("''", "")
    text = re.sub(r"<[^>]+>", "", text)
    return text


def strip_leading_templates(lines: list[str]) -> list[str]:
    text = "\n".join(lines)
    text = re.sub(r"\{\{header.*?\}\}", "", text, count=1, flags=re.DOTALL)
    remaining = text.splitlines()
    result: list[str] = []
    for line in remaining:
        stripped = line.strip()
        if not stripped:
            if result:
                result.append(line)
            continue
        if stripped.startswith("{{") and stripped.endswith("}}"):
            continue
        result.append(line)
    return result


def normalize_wikitext(raw_text: str, start_heading: str) -> list[str]:
    lines = strip_leading_templates(raw_text.splitlines())
    output: list[str] = []
    started = False

    for raw_line in lines:
        line = raw_line.strip()
        if not line or CATEGORY_PATTERN.match(line):
            output.append("")
            continue
        line = normalize_inline_markup(line).strip()
        if not line:
            output.append("")
            continue

        heading_match = HEADING_PATTERN.match(line)
        if heading_match:
            heading_text = heading_match.group(2).strip()
            if not started and (start_heading in heading_text or heading_text in start_heading):
                started = True
            if not started:
                continue
            depth = len(heading_match.group(1))
            output.append(f"{'#' * min(depth, 4)} {heading_text}")
            output.append("")
            continue

        if not started:
            if len(line) > 20:
                started = True
            else:
                continue

        output.extend(segment.strip() for segment in line.splitlines())
        output.append("")

    normalized: list[str] = []
    blank_pending = False
    for line in output:
        if line:
            if blank_pending and normalized:
                normalized.append("")
            normalized.append(line)
            blank_pending = False
        else:
            blank_pending = True

    while normalized and not normalized[-1]:
        normalized.pop()

    if not normalized:
        raise ValueError("No text extracted from raw Wikisource witness.")
    return normalized


def yaml_list(items: tuple[str, ...], indent: int = 0) -> list[str]:
    prefix = " " * indent
    return [f"{prefix}- {item}" for item in items]


def build_markdown(config: TextConfig, body_lines: list[str]) -> str:
    frontmatter = [
        "---",
        f"id: {config.source_id}",
        f"title: {config.title}",
        f"source_title: {config.source_title}",
        "source_type: primary_text",
        "tradition:",
        *yaml_list(config.tradition, indent=2),
        f"author: {config.author}",
        f"section: {config.section}",
        "language_original: tamil",
        "language_current: tamil",
        "themes:",
        *yaml_list(config.themes, indent=2),
        "concepts:",
        *yaml_list(config.concepts, indent=2),
        "use_for:",
        *yaml_list(config.use_for, indent=2),
        "avoid_for:",
        "  - decontextualized_technical_practice",
        "related_sources:",
        *yaml_list(config.related_sources, indent=2),
        "notes:",
        f"  - Public-domain page inspected at {config.page_url}",
        *(f"  - {note}" for note in config.notes),
        "copyright_status: public_domain",
        "status: imported_public_domain",
        f'citation: "{config.source_title}, Tamil Wikisource witness"',
        "---",
        "",
        f"# {config.source_title}",
        "",
        "## Tamil Primary Text",
        "",
        *body_lines,
        "",
        "## Source Provenance",
        "",
        f"- Imported from {config.page_url}.",
        "",
    ]
    return "\n".join(frontmatter)


def import_text(config: TextConfig) -> Path:
    raw_text = fetch_raw_wikitext(config)
    body_lines = normalize_wikitext(raw_text, config.start_heading)
    markdown = build_markdown(config, body_lines)
    config.output_path.parent.mkdir(parents=True, exist_ok=True)
    config.output_path.write_text(markdown, encoding="utf-8")
    return config.output_path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Import Tamil Siddhar corpora from Wikisource.")
    parser.add_argument("slugs", nargs="*", choices=sorted(TEXTS))
    args = parser.parse_args(argv)
    selected = args.slugs or sorted(TEXTS)
    for slug in selected:
        path = import_text(TEXTS[slug])
        print(path.relative_to(REPO_ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
