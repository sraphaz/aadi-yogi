from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GITA_ROOT = REPO_ROOT / "content" / "sources" / "bhagavad_gita"
USER_AGENT = "AadiYogi Gutenberg Importer/1.0"
GUTENBERG_URL = "https://www.gutenberg.org/ebooks/2388.txt.utf-8"
START_MARKER = "*** START OF THE PROJECT GUTENBERG EBOOK"
END_MARKER = "*** END OF THE PROJECT GUTENBERG EBOOK"

CHAPTER_THEMES: dict[int, tuple[str, ...]] = {
    1: ("grief", "crisis", "dharma", "war"),
    2: ("self_knowledge", "dharma", "karma_yoga", "discernment"),
    3: ("karma_yoga", "action", "desirelessness"),
    4: ("jnana_yoga", "renunciation", "knowledge"),
    5: ("renunciation", "action", "equanimity"),
    6: ("meditation", "dhyana", "self_mastery"),
    7: ("bhakti", "divine_knowledge", "manifestation"),
    8: ("brahman", "death", "imperishable"),
    9: ("raja_yoga", "knowledge", "devotion"),
    10: ("vibhuti", "manifestation", "glory"),
    11: ("universal_form", "vision", "devotion"),
    12: ("bhakti_yoga", "devotion", "surrender"),
    13: ("kshetra", "purusha", "discrimination"),
    14: ("gunas", "nature", "transcendence"),
    15: ("purushottama", "supreme_self", "tree_of_life"),
    16: ("virtue", "vice", "discrimination"),
    17: ("faith", "shraddha", "sattva"),
    18: ("moksha", "renunciation", "synthesis"),
}

CHAPTER_CONCEPTS: dict[int, tuple[str, ...]] = {
    1: ("dharma", "arjuna", "krishna"),
    2: ("atman", "dharma", "karma_yoga", "purusha"),
    3: ("karma_yoga", "yajna", "action"),
    4: ("jnana_yoga", "avatar", "knowledge"),
    5: ("sannyasa", "karma_yoga", "equanimity"),
    6: ("dhyana", "yoga", "mind"),
    7: ("ishwara", "maya", "bhakti"),
    8: ("brahman", "akshara", "devotion"),
    9: ("bhakti", "knowledge", "grace"),
    10: ("vibhuti", "ishwara", "manifestation"),
    11: ("vishvarupa", "bhakti", "awe"),
    12: ("bhakti", "devotion", "grace"),
    13: ("kshetra", "kshetrajna", "prakriti"),
    14: ("gunas", "sattva", "rajas", "tamas"),
    15: ("purushottama", "atman", "transcendence"),
    16: ("daivi", "asuri", "virtue"),
    17: ("shraddha", "sattva", "tapas"),
    18: ("moksha", "sannyasa", "dharma"),
}


@dataclass(frozen=True)
class ChapterSlice:
    number: int
    title: str
    body: str


def fetch_gutenberg_text() -> str:
    request = urllib.request.Request(GUTENBERG_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read().decode("utf-8")


def extract_main_text(raw: str) -> str:
    start = raw.find(START_MARKER)
    end = raw.find(END_MARKER)
    if start == -1 or end == -1:
        raise ValueError("Could not locate Gutenberg start/end markers.")
    return raw[start:end]


def split_chapters(text: str) -> list[ChapterSlice]:
    pattern = re.compile(r"^\s*CHAPTER ([IVXLC]+|\d+)\.?\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if not matches:
        raise ValueError("No chapter markers found.")

    roman_map = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
        "V": 5,
        "VI": 6,
        "VII": 7,
        "VIII": 8,
        "IX": 9,
        "X": 10,
        "XI": 11,
        "XII": 12,
        "XIII": 13,
        "XIV": 14,
        "XV": 15,
        "XVI": 16,
        "XVII": 17,
        "XVIII": 18,
    }

    chapters: list[ChapterSlice] = []
    for index, match in enumerate(matches[:18]):
        token = match.group(1)
        number = int(token) if token.isdigit() else roman_map[token]
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)
        chapters.append(ChapterSlice(number=number, title=f"Chapter {number}", body=body))
    return chapters


def yaml_list(items: tuple[str, ...], indent: int = 0) -> list[str]:
    prefix = " " * indent
    return [f"{prefix}- {item}" for item in items]


def build_markdown(chapter: ChapterSlice) -> str:
    num = chapter.number
    chapter_id = f"{num:02d}"
    themes = CHAPTER_THEMES.get(num, ("gita",))
    concepts = CHAPTER_CONCEPTS.get(num, ("dharma",))
    frontmatter = [
        "---",
        f"id: bhagavad_gita/chapter_{chapter_id}",
        f"title: Bhagavad Gita - Chapter {num} (Edwin Arnold Translation)",
        "source_title: Bhagavad Gita",
        "source_type: primary_text",
        "tradition:",
        *yaml_list(("gita", "vedantic"), indent=2),
        "author: Vyasa",
        f"section: chapter_{chapter_id}",
        "language_original: sanskrit",
        "language_current: english",
        "translator: Sir Edwin Arnold",
        "themes:",
        *yaml_list(themes, indent=2),
        "concepts:",
        *yaml_list(concepts, indent=2),
        "use_for:",
        *yaml_list(("source_grounded_guidance", "philosophical_grounding"), indent=2),
        "avoid_for:",
        "  - isolated_proof_texting",
        "related_sources:",
        "  - bhagavad_gita/index",
        "notes:",
        f"  - Public-domain translation from Project Gutenberg ebook #2388 ({GUTENBERG_URL})",
        "  - The Song Celestial; Or, Bhagavad-Gita (1885/1900 edition text)",
        "copyright_status: public_domain",
        "status: imported_public_domain",
        f'citation: "Bhagavad Gita, Chapter {num}; translated by Sir Edwin Arnold (PD, Gutenberg #2388)"',
        "---",
        "",
    ]
    sections = [
        f"# Bhagavad Gita - Chapter {num}",
        "",
        "## Public-Domain Translation",
        "",
        chapter.body,
        "",
        "## Source Provenance",
        "",
        f"- Imported from Project Gutenberg ebook #2388: {GUTENBERG_URL}",
        "- Translator: Sir Edwin Arnold, *The Song Celestial* (public domain).",
        "",
    ]
    return "\n".join(frontmatter + sections)


def import_chapter(chapter: ChapterSlice) -> Path:
    chapter_id = f"{chapter.number:02d}"
    output_dir = GITA_ROOT / f"chapter_{chapter_id}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "full.public_domain.md"
    output_path.write_text(build_markdown(chapter), encoding="utf-8")
    return output_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import Bhagavad Gita chapters from Project Gutenberg (Edwin Arnold, PD)."
    )
    parser.add_argument(
        "chapters",
        nargs="*",
        type=int,
        help="Chapter numbers to import (1-18). Defaults to all.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    raw = fetch_gutenberg_text()
    text = extract_main_text(raw)
    all_chapters = split_chapters(text)
    if not args.chapters and len(all_chapters) < 18:
        raise ValueError(f"Expected 18 chapters, found {len(all_chapters)}.")
    selected = {num for num in args.chapters} if args.chapters else {c.number for c in all_chapters}

    for chapter in all_chapters:
        if chapter.number not in selected:
            continue
        path = import_chapter(chapter)
        print(path.relative_to(REPO_ROOT).as_posix())

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
