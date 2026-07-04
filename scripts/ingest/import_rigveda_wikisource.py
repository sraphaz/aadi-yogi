from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RIGVEDA_ROOT = REPO_ROOT / "content" / "sources" / "vedas" / "rig_veda"
USER_AGENT = "AadiYogi Rigveda Wikisource Importer/1.0"
PAGE_TEMPLATE = "The Hymns of the Rigveda/Book {book}/Hymn {hymn}"


class TextExtractor(HTMLParser):
    BLOCK_TAGS = {"p", "div", "br", "h1", "h2", "h3", "h4", "li", "blockquote"}
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


@dataclass(frozen=True)
class HymnConfig:
    book: int
    hymn: int

    @property
    def page_title(self) -> str:
        return PAGE_TEMPLATE.format(book=self.book, hymn=self.hymn)

    @property
    def output_path(self) -> Path:
        return RIGVEDA_ROOT / f"mandala_{self.book:02d}_hymn_{self.hymn:03d}.public_domain.md"


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
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    parse_payload = payload.get("parse")
    if not isinstance(parse_payload, dict) or "text" not in parse_payload:
        raise ValueError(f"Unexpected payload for {page_title}")
    return str(parse_payload["text"])


def html_to_lines(html: str) -> list[str]:
    extractor = TextExtractor()
    extractor.feed(html)
    lines = [re.sub(r"\s+", " ", line).strip() for line in extractor.get_text().splitlines()]
    return [line for line in lines if line and not line.startswith("Retrieved from ")]


def extract_hymn_body(lines: list[str], config: HymnConfig) -> str:
    start_patterns = [
        f"Hymn {config.hymn}",
        f"HYMN {config.hymn}",
        f"Rigveda, Book {config.book}, Hymn {config.hymn}",
    ]
    start_index = 0
    for pattern in start_patterns:
        for index, line in enumerate(lines):
            if pattern.lower() in line.lower():
                start_index = index
                break
        else:
            continue
        break

    body_lines = lines[start_index:]
    rendered: list[str] = []
    for line in body_lines:
        if line.startswith("Footnotes") or "Navigation menu" in line:
            break
        if line.startswith("←") or line.startswith("→"):
            continue
        rendered.append(line)
    return "\n\n".join(rendered).strip()


def build_markdown(config: HymnConfig, body: str, page_url: str) -> str:
    hymn_id = f"mandala_{config.book:02d}_hymn_{config.hymn:03d}"
    return f"""---
id: vedas/rig_veda/{hymn_id}
title: Rig Veda - Mandala {config.book} Hymn {config.hymn}
source_title: Rig Veda
source_type: primary_text
tradition:
  - vedic
author: Ralph T. H. Griffith
section: {hymn_id}
language_original: sanskrit
language_current: english
translator: Ralph T. H. Griffith
themes:
  - vedic_hymn
  - invocation
concepts:
  - agni
  - yajna
use_for:
  - vedic_source_grounding
  - symbolic_reading
avoid_for:
  - ritual_instruction_without_context
related_sources:
  - vedas/rig_veda/index
notes:
  - Imported from English Wikisource: {page_url}
  - Griffith translation (public domain).
copyright_status: public_domain
status: imported_public_domain
citation: "Rig Veda, Mandala {config.book}, Hymn {config.hymn}; Ralph T. H. Griffith translation"
---

# Rig Veda - Mandala {config.book} Hymn {config.hymn}

## Public-Domain Translation

{body}

## Source Provenance

- Imported from {page_url}
- Translator: Ralph T. H. Griffith (public domain).
"""


def import_hymn(config: HymnConfig) -> Path:
    page_url = f"https://en.wikisource.org/wiki/{config.page_title.replace(' ', '_')}"
    html = fetch_html(config.page_title)
    lines = html_to_lines(html)
    body = extract_hymn_body(lines, config)
    markdown = build_markdown(config, body, page_url)
    config.output_path.parent.mkdir(parents=True, exist_ok=True)
    config.output_path.write_text(markdown, encoding="utf-8")
    return config.output_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Rig Veda hymns from English Wikisource.")
    parser.add_argument("--book", type=int, default=1)
    parser.add_argument("hymns", nargs="*", type=int, help="Hymn numbers to import.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    hymns = args.hymns or list(range(1, 11))
    for hymn in hymns:
        path = import_hymn(HymnConfig(book=args.book, hymn=hymn))
        print(path.relative_to(REPO_ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
