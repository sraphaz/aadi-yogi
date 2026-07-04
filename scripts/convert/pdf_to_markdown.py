"""Convert downloaded Ashram library PDFs into Markdown, following the manifests.

Usage:
    python scripts/convert/pdf_to_markdown.py [manifest ...] [--include-restricted]

For every volume in a manifest:

- full_text: true  -> the PDF text is extracted with pdftotext, lightly cleaned
  (running headers/footers removed, pages annotated) and written with YAML
  frontmatter to the manifest's content_dir (committed to the repository).
- full_text: false -> a metadata-only record (no source text) is written to the
  content_dir. With --include-restricted and a locally downloaded PDF, the full
  text is additionally extracted to the manifest's restricted_markdown_dir
  under data/markdown/, which is gitignored, for personal local study only.

Requires poppler-utils (pdftotext) on the PATH.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_DIR = REPO_ROOT / "scripts" / "ingest" / "manifests"

PAGE_NUMBER_PATTERN = re.compile(r"^[\divxlcIVXLC]+$")
HEADER_FREQUENCY_THRESHOLD = 0.08


def load_manifest(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def extract_pages(pdf_path: Path) -> list[str]:
    result = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", str(pdf_path), "-"],
        check=True,
        capture_output=True,
    )
    return result.stdout.decode("utf-8", errors="replace").split("\f")


def normalize_running_line(line: str) -> str:
    """Normalize a candidate header/footer line so repeats can be counted."""
    return re.sub(r"\d+", "#", line.strip()).lower()


def collect_running_lines(pages: list[str]) -> set[str]:
    """Find lines that repeat at page edges across many pages (running heads)."""
    counter: Counter[str] = Counter()
    for page in pages:
        lines = [line for line in page.splitlines() if line.strip()]
        for line in lines[:2] + lines[-2:]:
            normalized = normalize_running_line(line)
            if normalized and len(normalized) < 90:
                counter[normalized] += 1

    threshold = max(4, int(len(pages) * HEADER_FREQUENCY_THRESHOLD))
    return {line for line, count in counter.items() if count >= threshold}


def clean_page(page: str, running_lines: set[str]) -> str:
    lines = page.splitlines()

    def is_running(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        if PAGE_NUMBER_PATTERN.match(stripped):
            return True
        return normalize_running_line(stripped) in running_lines

    start, end = 0, len(lines)
    while start < end and (not lines[start].strip() or is_running(lines[start])):
        if lines[start].strip() and not is_running(lines[start]):
            break
        start += 1
    while end > start and (not lines[end - 1].strip() or is_running(lines[end - 1])):
        if lines[end - 1].strip() and not is_running(lines[end - 1]):
            break
        end -= 1

    body = "\n".join(lines[start:end]).strip("\n")
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body


def pdf_to_markdown_body(pdf_path: Path) -> str:
    pages = extract_pages(pdf_path)
    running_lines = collect_running_lines(pages)

    chunks: list[str] = []
    for index, page in enumerate(pages, start=1):
        cleaned = clean_page(page, running_lines)
        if not cleaned:
            continue
        chunks.append(f"<!-- pdf page {index} -->\n\n{cleaned}")
    return "\n\n".join(chunks) + "\n"


def build_frontmatter(manifest: dict, volume: dict, *, full_text: bool) -> dict:
    collection = manifest["collection"]
    author = manifest["author"]
    citation = (
        f"{author}, {volume['title']}, {manifest['collection_title']} "
        f"Vol. {volume['volume']}, {manifest['publisher']}. "
        f"Digital edition: {manifest['source_page']}"
    )
    frontmatter = {
        "id": f"{collection}/{volume['slug']}",
        "title": f"{volume['title']} ({manifest['collection_title']} Vol. {volume['volume']})",
        "source_title": volume["title"],
        "source_type": "primary_text",
        "tradition": list(manifest.get("tradition", [])),
        "author": author,
        "language_original": manifest.get("language", "english"),
        "language_current": manifest.get("language", "english"),
        "collection": manifest["collection_title"],
        "volume": volume["volume"],
        "themes": list(volume.get("themes", [])),
        "copyright_status": "public_domain" if full_text else "metadata_only",
        "status": "draft" if full_text else "metadata_only",
        "citation": citation,
        "source_url": manifest["download_url_template"].format(id=volume["id"]),
        "notes": (
            "Machine-converted from the official Ashram PDF with pdftotext; "
            "running headers and footers removed; pending editorial review."
            if full_text
            else "Metadata record only. "
            + volume.get(
                "metadata_reason",
                "The work remains under active copyright of the Sri Aurobindo "
                "Ashram Trust, so the full text is not stored in this repository.",
            ).strip()
        ),
    }
    if volume.get("title_french"):
        frontmatter["title_original"] = volume["title_french"]
    if not full_text:
        frontmatter["avoid_for"] = ["verbatim_reproduction_without_permission"]
    return frontmatter


def render_markdown(frontmatter: dict, heading: str, body: str) -> str:
    yaml_block = yaml.safe_dump(
        frontmatter, sort_keys=False, allow_unicode=True, width=88
    ).strip()
    return f"---\n{yaml_block}\n---\n\n# {heading}\n\n{body}"


def metadata_record_body(manifest: dict, volume: dict) -> str:
    description = volume.get("description", "").strip()
    url = manifest["download_url_template"].format(id=volume["id"])
    reason = volume.get(
        "metadata_reason",
        "This work remains under active copyright of the Sri Aurobindo Ashram "
        "Trust, so its full text is not stored in this public repository "
        "(see `docs/copyright_policy.md`).",
    ).strip()
    return (
        "## About This Volume\n\n"
        f"{description}\n\n"
        "## Access\n\n"
        f"{reason} For personal study, download the "
        f"official PDF from [the Ashram library]({url}) with "
        "`python scripts/ingest/download_ashram_pdfs.py` and convert it "
        "locally with `python scripts/convert/pdf_to_markdown.py "
        "--include-restricted` (output stays in the gitignored `data/` tree).\n\n"
        "## Agent Use\n\n"
        "Use this record for orientation and citation only. Do not present "
        "reconstructed passages as quotations from this volume.\n"
    )


def process_manifest(manifest_path: Path, include_restricted: bool) -> int:
    manifest = load_manifest(manifest_path)
    raw_dir = REPO_ROOT / manifest["raw_dir"]
    content_dir = REPO_ROOT / manifest["content_dir"]
    restricted_dir = REPO_ROOT / manifest["restricted_markdown_dir"]
    content_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for volume in manifest["volumes"]:
        slug = volume["slug"]
        full_text = bool(volume.get("full_text"))
        pdf_path = raw_dir / f"{slug}.pdf"
        heading = f"{volume['title']} ({manifest['collection_title']} Vol. {volume['volume']})"
        frontmatter = build_frontmatter(manifest, volume, full_text=full_text)

        if full_text:
            if not pdf_path.exists():
                print(f"  MISSING PDF for full-text volume: {pdf_path.relative_to(REPO_ROOT)}")
                failures += 1
                continue
            print(f"  converting volume {volume['volume']}: {volume['title']}")
            body = pdf_to_markdown_body(pdf_path)
            destination = content_dir / f"{slug}.md"
            destination.write_text(render_markdown(frontmatter, heading, body), encoding="utf-8")
        else:
            destination = content_dir / f"{slug}.md"
            destination.write_text(
                render_markdown(frontmatter, heading, metadata_record_body(manifest, volume)),
                encoding="utf-8",
            )
            print(f"  metadata record: {destination.relative_to(REPO_ROOT)}")
            if include_restricted and pdf_path.exists():
                restricted_dir.mkdir(parents=True, exist_ok=True)
                body = pdf_to_markdown_body(pdf_path)
                local_path = restricted_dir / f"{slug}.md"
                local_path.write_text(
                    render_markdown(frontmatter, heading, body), encoding="utf-8"
                )
                print(f"    local restricted text: {local_path.relative_to(REPO_ROOT)}")
    return failures


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", nargs="*", help="manifest YAML files to process")
    parser.add_argument(
        "--include-restricted",
        action="store_true",
        help="also convert restricted volumes into the gitignored data/markdown/ tree",
    )
    args = parser.parse_args(argv[1:])

    manifest_paths = (
        [Path(m) for m in args.manifests]
        if args.manifests
        else sorted(MANIFEST_DIR.glob("*.yaml"))
    )

    total_failures = 0
    for manifest_path in manifest_paths:
        print(f"Manifest: {manifest_path.name}")
        total_failures += process_manifest(manifest_path, args.include_restricted)

    if total_failures:
        print(f"Completed with {total_failures} problems.")
        return 1
    print("Conversion completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
