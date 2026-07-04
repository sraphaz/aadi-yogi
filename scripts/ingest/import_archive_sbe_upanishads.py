from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
UPANISHAD_ROOT = REPO_ROOT / "content" / "sources" / "upanishads"
CACHE_DIR = REPO_ROOT / "data" / "cache"
USER_AGENT = "AadiYogi Archive SBE Upanishad Importer/1.0"
SBE15_URL = (
    "https://archive.org/download/SacredBooksEastVariousOrientalScholarsWithIndex."
    "50VolsMaxMuller/15.SacredBooksEast.VarOrSch.v15.Muller.Hindu.Mull."
    "Upanishads.p2.KathMundTait..Mait.Oxf.1884._djvu.txt"
)
SBE15_CACHE = CACHE_DIR / "sbe15_upanishads_part2_djvu.txt"


@dataclass(frozen=True)
class TextConfig:
    import_key: str
    slug: str
    output_name: str
    source_id_suffix: str
    source_title: str
    title: str
    start_pattern: str
    end_pattern: str
    citation: str
    section: str = "full_text"
    themes: tuple[str, ...] = ()
    concepts: tuple[str, ...] = ()
    use_for: tuple[str, ...] = ()
    related_sources: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


TEXTS: dict[str, TextConfig] = {
    "shvetashvatara": TextConfig(
        import_key="shvetashvatara",
        slug="shvetashvatara",
        output_name="full",
        source_id_suffix="full_public_domain_translation",
        source_title="Shvetashvatara Upanishad",
        title="Shvetashvatara Upanishad - Max Muller Public Domain Translation",
        start_pattern=(
            r"SVETASVATARA-\s*\nUPANISHAD\.\s*\n\s*_?\s*FIRST ADHYAYA"
        ),
        end_pattern=r"\nPRASNA-UPANISHAD",
        citation=(
            "Friedrich Max Muller, Shvetashvatara Upanishad "
            "(Sacred Books of the East, Volume 15, public domain)"
        ),
        themes=("brahman", "devotion", "self_knowledge", "lord"),
        concepts=("brahman", "atman", "shiva", "devotion"),
        use_for=("source_grounded_nondual_reflection", "devotional_inquiry", "lord_contemplation"),
        related_sources=("upanishads/shvetashvatara/index",),
        notes=(
            "Extracted from Archive.org OCR witness of SBE Volume 15.",
            "Witness aligned with Max Muller translation lineage.",
        ),
    ),
    "brihadaranyaka": TextConfig(
        import_key="brihadaranyaka",
        slug="brihadaranyaka",
        output_name="full",
        source_id_suffix="full_public_domain_translation",
        source_title="Brihadaranyaka Upanishad",
        title="Brihadaranyaka Upanishad - Max Muller Public Domain Translation",
        start_pattern=(
            r"BRIHADARANYAKA-\s*\nUPANISHAD\.\s*\n\s*\nFIRST ADHYAYA"
        ),
        end_pattern=r"\nSVETASVATARA-",
        citation=(
            "Friedrich Max Muller, Brihadaranyaka Upanishad "
            "(Sacred Books of the East, Volume 15, public domain)"
        ),
        themes=("brahman", "self_knowledge", "yajna", "dialogue"),
        concepts=("brahman", "atman", "yajnavalkya", "death"),
        use_for=("source_grounded_nondual_reflection", "teacher_student_dialogue", "brahman_inquiry"),
        related_sources=("upanishads/brihadaranyaka/index",),
        notes=(
            "Full text extracted from Archive.org OCR witness of SBE Volume 15.",
            "OCR artifacts may remain; suitable as historical public-domain witness.",
        ),
    ),
}


def fetch_sbe15_text(cache_path: Path = SBE15_CACHE) -> str:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8", errors="replace")
    request = urllib.request.Request(SBE15_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        text = response.read().decode("utf-8", errors="replace")
    cache_path.write_text(text, encoding="utf-8")
    return text


def clean_ocr_body(body: str) -> str:
    lines: list[str] = []
    skip_patterns = (
        re.compile(r"^Digitized by Google$", re.I),
        re.compile(r"^\d+\s+[A-Z\- ]+UPANISHAD\.?$"),
        re.compile(r"^[IVXLC]+\s+ADHYAYA", re.I),
        re.compile(r"^PAGE\s*$", re.I),
    )
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            if lines and lines[-1]:
                lines.append("")
            continue
        if any(pattern.search(line) for pattern in skip_patterns):
            continue
        line = re.sub(r"\s+", " ", line)
        lines.append(line)
    while lines and not lines[-1]:
        lines.pop()
    return "\n\n".join(lines).strip()


def render_line(line: str) -> str | None:
    heading = re.match(
        r"^(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH)\s+"
        r"(ADHYAYA|BRAHMANA|VALL[IÎ]|KHAMDA)\.?$",
        line,
        re.IGNORECASE,
    )
    if heading:
        return f"### {line}"
    return line


def extract_section(text: str, config: TextConfig) -> str:
    start = re.search(config.start_pattern, text, re.MULTILINE | re.IGNORECASE)
    if not start:
        raise ValueError(f"Could not locate start section for {config.import_key}")
    remainder = text[start.end() :]
    end = re.search(config.end_pattern, remainder, re.MULTILINE | re.IGNORECASE)
    if not end:
        raise ValueError(f"Could not locate end section for {config.import_key}")
    body = clean_ocr_body(remainder[: end.start()])
    rendered = []
    for line in body.split("\n\n"):
        line = line.strip()
        if not line:
            continue
        output = render_line(line)
        if output:
            rendered.append(output)
    if not rendered:
        raise ValueError(f"No body extracted for {config.import_key}")
    return "\n\n".join(rendered)


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
        "author: Friedrich Max Muller",
        f"section: {config.section}",
        "language_original: sanskrit",
        "language_current: english",
        "translator: Friedrich Max Muller",
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
        f"  - Extracted from {SBE15_URL}",
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
        f"- Extracted from Archive.org witness of Sacred Books of the East, Volume 15.",
        f"- Source file: {SBE15_URL}",
        "",
    ]
    return "\n".join(frontmatter)


def import_text(config: TextConfig, source_text: str) -> Path:
    translation_body = extract_section(source_text, config)
    markdown = build_markdown(config, translation_body)
    output_path = UPANISHAD_ROOT / config.slug / f"{config.output_name}.public_domain.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import Upanishads from Archive.org SBE Volume 15 OCR witness."
    )
    parser.add_argument("slugs", nargs="*", choices=sorted(TEXTS))
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    selected = args.slugs or sorted(TEXTS)
    source_text = fetch_sbe15_text()
    for slug in selected:
        path = import_text(TEXTS[slug], source_text)
        print(path.relative_to(REPO_ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
