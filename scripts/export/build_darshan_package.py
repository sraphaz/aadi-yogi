"""Build the distributable Darshan package zip.

Assembles the Sky-Forge session artifacts and the narrative design documents
into a single zip ready to import into a Sky-Forge checkout
(.sky/sessions/darshan/) or to hand to any design tool.

Usage:
    python scripts/export/build_darshan_package.py
Output:
    docs/skyforge/darshan-package.zip
"""

from __future__ import annotations

import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SESSION_DIR = REPO_ROOT / "docs" / "skyforge" / "darshan"
NARRATIVE_GLOB = "darshan_*.md"
OUTPUT = REPO_ROOT / "docs" / "skyforge" / "darshan-package.zip"

MANIFEST = """Darshan - Sky-Forge session package
====================================

Contents
--------
session/       Sky-Forge session artifacts. Copy this folder to
               .sky/sessions/darshan/ inside a sky-forge checkout, then:
                 ./scripts/sky/sky.ps1 status  -Slug darshan
                 ./scripts/sky/sky.ps1 export  -Slug darshan
cloud-design/  Cloud Design handoffs (.dc.html, <x-dc> format) ready for
               entry into Claude/Cloud Design:
                 handoff-app.dc.html            the Darshan PWA (track: mobile)
                 handoff-institucional.dc.html  the institutional site
narrative/     The design documents behind the artifacts (concept, spec,
               library depth design, becoming path, sky map, house of nature,
               reuse map, passage-id scheme).
decisions/     ADRs taken from the repository's consciousness core
               (sustaining model, natal boundary, health gate, editorial
               policy, passage-id scheme).

Source repository: https://github.com/sraphaz/aadi-yogi
"""


def main() -> int:
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr("darshan-package/README.txt", MANIFEST)
        for path in sorted(SESSION_DIR.iterdir()):
            if path.is_file() and path.suffix in (".yaml", ".md"):
                bundle.write(path, f"darshan-package/session/{path.name}")
        for path in sorted((SESSION_DIR / "cloud-design").glob("*.dc.html")):
            bundle.write(path, f"darshan-package/cloud-design/{path.name}")
        for path in sorted((REPO_ROOT / "docs").glob(NARRATIVE_GLOB)):
            bundle.write(path, f"darshan-package/narrative/{path.name}")
        scheme = REPO_ROOT / "docs" / "passage_id_scheme.md"
        if scheme.exists():
            bundle.write(scheme, f"darshan-package/narrative/{scheme.name}")
        for path in sorted((REPO_ROOT / "docs" / "decisions").glob("*.md")):
            bundle.write(path, f"darshan-package/decisions/{path.name}")

    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Built {OUTPUT.relative_to(REPO_ROOT)} ({size_kb:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
