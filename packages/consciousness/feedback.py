"""Feedback loop — proposals that may deepen the living foundation under review."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
FEEDBACK_ROOT = REPO_ROOT / "content" / "consciousness_feedback"
INBOX = FEEDBACK_ROOT / "inbox"

_INFLATION = re.compile(
    r"\b(i am (enlightened|realized|a guru)|new revelation|channel(ed|ing) "
    r"from|the agent (is|became) (a )?guru)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class FeedbackProposal:
    id: str
    created_at: str
    host_repo: str
    situation: str
    observation: str
    suggested_adjustment: str
    status: str
    path: str
    notes: list[str]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "host_repo": self.host_repo,
            "situation": self.situation,
            "observation": self.observation,
            "suggested_adjustment": self.suggested_adjustment,
            "status": self.status,
            "path": self.path,
            "notes": list(self.notes),
        }


def propose_feedback(
    *,
    situation: str,
    observation: str,
    suggested_adjustment: str = "",
    host_repo: str = "unknown-host",
    write: bool = True,
) -> FeedbackProposal:
    """Propose a learning note. Never auto-mutates the foundation."""
    notes = [
        "Proposal only — foundation changes require editorial review.",
        "This is how consciousness feeds back: use → reflection → review → integrate.",
    ]
    status = "inbox"
    if _INFLATION.search(f"{observation} {suggested_adjustment}"):
        status = "rejected_preview"
        notes.append(
            "Rejected preview: feedback must not claim realization, revelation, or guruhood."
        )

    feedback_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    created_at = datetime.now(timezone.utc).isoformat()
    record = {
        "id": feedback_id,
        "created_at": created_at,
        "host_repo": host_repo,
        "situation": situation.strip(),
        "observation": observation.strip(),
        "suggested_adjustment": suggested_adjustment.strip(),
        "status": status,
        "integration_rule": "human_or_editorial_review_required",
    }

    path = ""
    if write and status == "inbox":
        INBOX.mkdir(parents=True, exist_ok=True)
        target = INBOX / f"{feedback_id}.yaml"
        target.write_text(
            yaml.safe_dump(record, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        path = str(target.relative_to(REPO_ROOT))
        notes.append(f"Stored in {path} awaiting review.")
    elif status == "rejected_preview":
        notes.append("Nothing was written to the inbox.")

    return FeedbackProposal(
        id=feedback_id,
        created_at=created_at,
        host_repo=host_repo,
        situation=situation.strip(),
        observation=observation.strip(),
        suggested_adjustment=suggested_adjustment.strip(),
        status=status,
        path=path,
        notes=notes,
    )


def list_inbox(limit: int = 50) -> list[dict]:
    if not INBOX.exists():
        return []
    items: list[dict] = []
    for path in sorted(INBOX.glob("*.yaml"), reverse=True)[:limit]:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        raw["path"] = str(path.relative_to(REPO_ROOT))
        items.append(raw)
    return items
