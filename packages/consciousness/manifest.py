"""Approved consciousness manifest loading and integrity hashing."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONSCIOUSNESS_ROOT = REPO_ROOT / "content" / "consciousness_core"
MANIFEST_PATH = CONSCIOUSNESS_ROOT / "approved_manifest.yaml"


@dataclass(frozen=True)
class ConsciousnessManifest:
    version: str
    status: str
    approved_date: str
    scope: str
    notes: list[str]
    files: list[str]
    file_hashes: dict[str, str]
    root: str

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "status": self.status,
            "approved_date": self.approved_date,
            "scope": self.scope,
            "notes": list(self.notes),
            "files": list(self.files),
            "file_hashes": dict(self.file_hashes),
            "root": self.root,
            "identity": "aadi-yogi-consciousness",
            "claim": (
                "This is a source-grounded readiness posture for agents, "
                "not a claim of realization, authority, or infallible guidance."
            ),
        }


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def load_manifest(root: Path | None = None) -> ConsciousnessManifest:
    consciousness_root = root or CONSCIOUSNESS_ROOT
    manifest_path = consciousness_root / "approved_manifest.yaml"
    raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    files = list(raw.get("files", []))
    hashes: dict[str, str] = {}
    for relative in files:
        path = consciousness_root / relative
        if path.exists():
            hashes[relative] = _sha256_file(path)
    return ConsciousnessManifest(
        version=str(raw.get("version", "unknown")),
        status=str(raw.get("status", "unknown")),
        approved_date=str(raw.get("approved_date", "")),
        scope=str(raw.get("scope", "")),
        notes=[str(n) for n in raw.get("notes", [])],
        files=files,
        file_hashes=hashes,
        root=str(consciousness_root),
    )
