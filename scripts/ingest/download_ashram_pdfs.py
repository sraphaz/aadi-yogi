"""Download the Sri Aurobindo Ashram PDF libraries described by ingestion manifests.

Usage:
    python scripts/ingest/download_ashram_pdfs.py [manifest ...]

Without arguments, every manifest in scripts/ingest/manifests/ is processed.
PDFs are stored under the manifest's raw_dir (inside data/raw/, which is
gitignored). Existing files are skipped unless --force is passed.
"""

from __future__ import annotations

import argparse
import sys
import time
import urllib.request
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_DIR = Path(__file__).resolve().parent / "manifests"
USER_AGENT = "aadi-yogi-ingestion/0.1 (personal study archive)"


def load_manifest(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def download(url: str, destination: Path, retries: int = 3) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                destination.write_bytes(response.read())
            return
        except OSError as exc:
            if attempt == retries:
                raise
            wait = 4 * attempt
            print(f"  retry {attempt}/{retries} after error: {exc} (waiting {wait}s)")
            time.sleep(wait)


def process_manifest(manifest_path: Path, force: bool) -> int:
    manifest = load_manifest(manifest_path)
    url_template = manifest["download_url_template"]
    raw_dir = REPO_ROOT / manifest["raw_dir"]
    raw_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for volume in manifest["volumes"]:
        destination = raw_dir / f"{volume['slug']}.pdf"
        if destination.exists() and not force:
            print(f"  skip (exists): {destination.relative_to(REPO_ROOT)}")
            continue
        url = url_template.format(id=volume["id"])
        print(f"  downloading volume {volume['volume']}: {volume['title']}")
        try:
            download(url, destination)
        except OSError as exc:
            failures += 1
            print(f"  FAILED: {url} ({exc})")
            continue
        size_mb = destination.stat().st_size / (1024 * 1024)
        print(f"    -> {destination.relative_to(REPO_ROOT)} ({size_mb:.1f} MB)")
    return failures


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", nargs="*", help="manifest YAML files to process")
    parser.add_argument("--force", action="store_true", help="re-download existing files")
    args = parser.parse_args(argv[1:])

    manifest_paths = (
        [Path(m) for m in args.manifests]
        if args.manifests
        else sorted(MANIFEST_DIR.glob("*.yaml"))
    )

    total_failures = 0
    for manifest_path in manifest_paths:
        print(f"Manifest: {manifest_path.name}")
        total_failures += process_manifest(manifest_path, force=args.force)

    if total_failures:
        print(f"Completed with {total_failures} failed downloads.")
        return 1
    print("All downloads completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
