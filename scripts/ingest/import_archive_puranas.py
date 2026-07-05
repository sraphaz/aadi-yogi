from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PURANA_ROOT = REPO_ROOT / "content" / "sources" / "puranas"
CACHE_DIR = REPO_ROOT / "data" / "cache"
USER_AGENT = "AadiYogi Archive Purana Importer/1.0"

MARKANDEYA_URL = "https://archive.org/download/cu31924022991974/cu31924022991974_djvu.txt"
MARKANDEYA_CACHE = CACHE_DIR / "markandeya_purana_pargiter_djvu.txt"
GARUDA_URL = (
    "https://archive.org/download/GarudaPuranaEnglishMotilal3VolumesIn1/"
    "Garuda%20Purana%20English%20-%20Motilal%20-%203%20Volumes%20in%201_djvu.txt"
)
GARUDA_CACHE = CACHE_DIR / "garuda_purana_motilal_djvu.txt"
VISHNU_URL = (
    "https://archive.org/download/bub_gb_rf3DwwYP40UC/bub_gb_rf3DwwYP40UC_djvu.txt"
)
VISHNU_CACHE = CACHE_DIR / "vishnu_purana_wilson_djvu.txt"

sys.path.insert(0, str(REPO_ROOT))
from packages.text.ocr_cleanup import clean_ocr_lines, fix_ocr_text


@dataclass(frozen=True)
class PuranaConfig:
    import_key: str
    slug: str
    output_name: str
    source_id: str
    title: str
    source_title: str
    translator: str
    citation: str
    start_pattern: str
    end_pattern: str
    themes: tuple[str, ...]
    concepts: tuple[str, ...]


TEXTS: dict[str, PuranaConfig] = {
    "markandeya_devi_mahatmya": PuranaConfig(
        import_key="markandeya_devi_mahatmya",
        slug="markandeya_purana",
        output_name="devi_mahatmya",
        source_id="puranas/markandeya_purana/devi_mahatmya",
        title="Markandeya Purana - Devi Mahatmya (Pargiter Translation)",
        source_title="Markandeya Purana - Devi Mahatmya",
        translator="F. Eden Pargiter",
        citation="F. Eden Pargiter, Markandeya Purana, Devi Mahatmya (1904, public domain)",
        start_pattern=r"Canto\s+LXXXI\.\s*\nCommencement\s+of\s+the\s+Devi",
        end_pattern=r"Canto\s+XCIII\.\s*\n\s*\nThe\s+Devi-m",
        themes=("devi", "durga", "illusion", "cosmic_battle"),
        concepts=("devi", "mahamaya", "madhu_kaitabha", "chandika"),
    ),
    "garuda_chapter_02": PuranaConfig(
        import_key="garuda_chapter_02",
        slug="garuda_purana",
        output_name="book_01_chapter_02",
        source_id="puranas/garuda_purana/book_01_chapter_02",
        title="Garuda Purana - Book 1 Chapter 2 (Tradition of Garuda Purana)",
        source_title="Garuda Purana",
        translator="J.L. Shastri (Motilal Banarsidass edition, public domain)",
        citation="Garuda Purana, Chapter 2: Tradition of Garuda Purana (public domain translation)",
        start_pattern=r"CHAPTER TWO\s*\n\s*Tradition of Garuda P(?:ur|ar)ana",
        end_pattern=r"CHAPTER THREE\s*\n\s*Statement of Contents",
        themes=("garuda", "vishnu", "tradition", "afterlife"),
        concepts=("garuda", "vishnu", "vyasa"),
    ),
    "vishnu_book1_ch2": PuranaConfig(
        import_key="vishnu_book1_ch2",
        slug="vishnu_purana",
        output_name="book_01_chapter_02",
        source_id="puranas/vishnu_purana/book_01_chapter_02",
        title="Vishnu Purana - Book 1 Chapter 2",
        source_title="Vishnu Purana",
        translator="Horace Hayman Wilson",
        citation="Horace Hayman Wilson, Vishnu Purana, Book I, Chapter II (1840, public domain)",
        start_pattern=r"BOOK I\., CHAP\. II\.",
        end_pattern=r"BOOK I\., CHAP\. III\.",
        themes=("cosmology", "vishnu", "creation"),
        concepts=("vishnu", "brahman", "creation"),
    ),
    "vishnu_book1_ch3": PuranaConfig(
        import_key="vishnu_book1_ch3",
        slug="vishnu_purana",
        output_name="book_01_chapter_03",
        source_id="puranas/vishnu_purana/book_01_chapter_03",
        title="Vishnu Purana - Book 1 Chapter 3",
        source_title="Vishnu Purana",
        translator="Horace Hayman Wilson",
        citation="Horace Hayman Wilson, Vishnu Purana, Book I, Chapter III (1840, public domain)",
        start_pattern=r"BOOK I\., CHAP\. III\.",
        end_pattern=r"BOOK I\., CHAP\. IV\.",
        themes=("cosmology", "vishnu", "creation"),
        concepts=("vishnu", "prakriti", "creation"),
    ),
}


def fetch_cached(url: str, cache_path: Path) -> str:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8", errors="replace")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=180) as response:
        text = response.read().decode("utf-8", errors="replace")
    cache_path.write_text(text, encoding="utf-8")
    return text


def source_for_key(key: str) -> str:
    if key.startswith("markandeya"):
        return fetch_cached(MARKANDEYA_URL, MARKANDEYA_CACHE)
    if key.startswith("garuda"):
        return fetch_cached(GARUDA_URL, GARUDA_CACHE)
    return fetch_cached(VISHNU_URL, VISHNU_CACHE)


def extract_section(text: str, config: PuranaConfig) -> str:
    start = re.search(config.start_pattern, text, re.MULTILINE | re.IGNORECASE)
    if not start:
        raise ValueError(f"Could not locate start for {config.import_key}")
    remainder = text[start.start() :]
    end = re.search(config.end_pattern, remainder[len(config.start_pattern) :], re.MULTILINE | re.IGNORECASE)
    if not end:
        raise ValueError(f"Could not locate end for {config.import_key}")
    body = remainder[: len(config.start_pattern) + end.start()]
    cleaned = clean_ocr_lines(body)
    if len(cleaned) < 200:
        raise ValueError(f"Extracted body too short for {config.import_key}")
    return cleaned


def build_markdown(config: PuranaConfig, body: str, source_url: str) -> str:
    return f"""---
id: {config.source_id}
title: {config.title}
source_title: {config.source_title}
source_type: primary_text
tradition:
  - puranic
author: {config.translator}
section: {config.output_name}
language_original: sanskrit
language_current: english
translator: {config.translator}
themes:
{chr(10).join(f"  - {t}" for t in config.themes)}
concepts:
{chr(10).join(f"  - {c}" for c in config.concepts)}
use_for:
  - puranic_source_grounding
  - thematic_inquiry
avoid_for:
  - fear_based_instruction
related_sources:
  - puranas/{config.slug}/index
notes:
  - Extracted from Archive.org public-domain witness: {source_url}
  - OCR cleanup applied; verify against printed edition for citation-critical use.
copyright_status: public_domain
status: imported_public_domain
citation: "{config.citation}"
---

# {config.title}

## Public-Domain Translation

{body}

## Source Provenance

- Extracted from {source_url}
- Translator: {config.translator}
"""


def import_text(config: PuranaConfig) -> Path:
    source_text = source_for_key(config.import_key)
    source_url = {
        "markandeya_devi_mahatmya": MARKANDEYA_URL,
        "garuda_chapter_02": GARUDA_URL,
    }.get(config.import_key, VISHNU_URL)
    body = extract_section(source_text, config)
    markdown = build_markdown(config, body, source_url)
    output_path = PURANA_ROOT / config.slug / f"{config.output_name}.public_domain.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Purana texts from Archive.org witnesses.")
    parser.add_argument("keys", nargs="*", choices=sorted(TEXTS))
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    selected = args.keys or sorted(TEXTS)
    for key in selected:
        path = import_text(TEXTS[key])
        print(path.relative_to(REPO_ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
