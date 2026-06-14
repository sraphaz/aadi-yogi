from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SIDDHA_ROOT = REPO_ROOT / "content" / "sources" / "siddha_texts"
USER_AGENT = "Codex AadiYogi Tamil Wikisource Importer/1.0"
CATEGORY_PATTERN = re.compile(r"^\[\[பகுப்பு:.*\]\]$")
HEADING_PATTERN = re.compile(r"^(=+)\s*(.*?)\s*\1$")
LINK_PATTERN = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]|\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class TextConfig:
    slug: str
    source_id: str
    source_title: str
    title: str
    raw_url: str
    page_url: str
    citation: str
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


TEXTS: dict[str, TextConfig] = {
    "tirumandiram_payiram": TextConfig(
        slug="tirumandiram_payiram",
        source_id="siddha_texts/tirumandiram/payiram/full_public_domain",
        source_title="Tirumandiram",
        title="Tirumandiram - Payiram Tamil Public-Domain Witness",
        raw_url=(
            "https://ta.wikisource.org/w/index.php?title="
            "%E0%AE%A4%E0%AE%BF%E0%AE%B0%E0%AF%81%E0%AE%AE%E0%AE%A8%E0%AF%8D"
            "%E0%AE%A4%E0%AE%BF%E0%AE%B0%E0%AE%AE%E0%AF%8D/"
            "%E0%AE%AA%E0%AE%BE%E0%AE%AF%E0%AE%BF%E0%AE%B0%E0%AE%AE%E0%AF%8D"
            "&action=raw"
        ),
        page_url=(
            "https://ta.wikisource.org/wiki/"
            "%E0%AE%A4%E0%AE%BF%E0%AE%B0%E0%AF%81%E0%AE%AE%E0%AE%A8%E0%AF%8D"
            "%E0%AE%A4%E0%AE%BF%E0%AE%B0%E0%AE%AE%E0%AF%8D/"
            "%E0%AE%AA%E0%AE%BE%E0%AE%AF%E0%AE%BF%E0%AE%B0%E0%AE%AE%E0%AF%8D"
        ),
        citation="Tirumular, Tirumandiram, Payiram, Tamil Wikisource witness",
        start_heading="திருமூலர் அருளிய திருமந்திரம்",
        output_path=(
            SIDDHA_ROOT
            / "tirumandiram"
            / "payiram"
            / "full.public_domain.md"
        ),
        author="Tirumular",
        section="payiram",
        tradition=("siddha", "shaiva", "tamil"),
        themes=("shiva", "mantra", "guru", "yoga"),
        concepts=("shiva", "mantra", "grace", "yoga"),
        use_for=("siddha_source_grounding", "shaiva_devotional_source", "tamil_primary_text"),
        related_sources=(
            "siddha_texts/index",
            "siddha_texts/tirumandiram/index",
            "siddha_texts/tirumandiram/payiram/index",
        ),
        notes=(
            "Ancient Tamil primary text imported from the Tamil Wikisource witness.",
            "The visible online page includes editorial presentation by Wikisource; repository intake preserves the core text with explicit provenance.",
        ),
    )
}


def fetch_raw_wikitext(config: TextConfig) -> str:
    request = urllib.request.Request(config.raw_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


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
    result = list(lines)
    while result:
        first = result[0].strip()
        if not first:
            result.pop(0)
            continue
        if first.startswith("{{header"):
            result.pop(0)
            while result:
                line = result.pop(0)
                if line.strip() == "}}":
                    break
            continue
        if first.startswith("{{") and first.endswith("}}"):
            result.pop(0)
            continue
        break
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
            depth = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            if not started and heading_text == start_heading:
                started = True
            if not started:
                continue
            prefix = "#" * min(depth, 4)
            output.append(f"{prefix} {heading_text}")
            output.append("")
            continue

        if not started:
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
    frontmatter: list[str] = [
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
        f"  - Raw witness inspected at {config.raw_url}",
        *(f"  - {note}" for note in config.notes),
        "copyright_status: public_domain",
        "status: imported_public_domain",
        f'citation: "{config.citation}"',
        "---",
        "",
    ]
    sections = [
        "# Tirumandiram - Payiram",
        "",
        "## Tamil Primary Text",
        "",
        *body_lines,
        "",
        "## Source Provenance",
        "",
        f"- Imported from {config.page_url}.",
        f"- Raw wikitext witness fetched from {config.raw_url}.",
        "",
        "## Notes",
        "",
        "This import captures an initial public-domain Tamil witness for the Tirumandiram. Later work can split the payiram into smaller reviewable units and compare alternate editions.",
        "",
    ]
    return "\n".join(frontmatter + sections)


def import_text(config: TextConfig) -> Path:
    raw_text = fetch_raw_wikitext(config)
    body_lines = normalize_wikitext(raw_text, config.start_heading)
    markdown = build_markdown(config, body_lines)
    config.output_path.parent.mkdir(parents=True, exist_ok=True)
    config.output_path.write_text(markdown, encoding="utf-8")
    return config.output_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import selected Tamil Wikisource primary-text witnesses."
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
