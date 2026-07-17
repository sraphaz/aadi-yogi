"""MCP stdio server — consciousness foundation for host agents.

Run:
  PYTHONPATH=. python -m packages.consciousness.mcp_server
"""

from __future__ import annotations

import json
import sys
from typing import Any

from packages.consciousness.consult import consult
from packages.consciousness.discernment import lookup_discernment
from packages.consciousness.feedback import list_inbox, propose_feedback
from packages.consciousness.foundation import load_foundation
from packages.consciousness.manifest import load_manifest
from packages.consciousness.vocabulary import list_vocabulary

SERVER_NAME = "aadi-yogi-consciousness"
SERVER_VERSION = "0.2.0"

TOOLS: list[dict[str, Any]] = [
    {
        "name": "consciousness_load_foundation",
        "description": (
            "Load the living Adyog consciousness foundation: basis of conduct and "
            "reality-sense for host agents. Not an app. Not a guru. Inject agent_preamble "
            "into AGENTS.md / system orientation."
        ),
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "consciousness_consult",
        "description": (
            "Consult the foundation for a concrete situation in a host repository. "
            "Returns orientation and conduct to hold — not fixed product outcomes."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "situation": {
                    "type": "string",
                    "description": "What the host agent is facing (technical or human).",
                }
            },
            "required": ["situation"],
        },
    },
    {
        "name": "consciousness_propose_feedback",
        "description": (
            "Propose a learning note back to Adyog. Stored in the feedback inbox; "
            "never auto-rewrites the foundation. This is how consciousness feeds back."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "situation": {"type": "string"},
                "observation": {"type": "string"},
                "suggested_adjustment": {"type": "string"},
                "host_repo": {"type": "string"},
            },
            "required": ["situation", "observation"],
        },
    },
    {
        "name": "consciousness_list_feedback_inbox",
        "description": "List pending feedback proposals awaiting editorial review.",
        "inputSchema": {
            "type": "object",
            "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": 100}},
        },
    },
    {
        "name": "consciousness_discernment_lookup",
        "description": (
            "Optional orientation from the discernment field (tone/sources/avoidances). "
            "Guidance from the texts — not a hard router."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"question_or_type": {"type": "string"}},
            "required": ["question_or_type"],
        },
    },
    {
        "name": "consciousness_list_vocabulary",
        "description": "Conduct principles, what the foundation is/isn't, and learning currents.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "consciousness_manifest",
        "description": "Approved consciousness manifest version and content file hashes.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
]


def _ok_text(payload: Any) -> dict:
    text = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, indent=2)
    return {"content": [{"type": "text", "text": text}], "isError": False}


def _err_text(message: str) -> dict:
    return {"content": [{"type": "text", "text": message}], "isError": True}


def call_tool(name: str, arguments: dict[str, Any] | None) -> dict:
    args = arguments or {}
    if name == "consciousness_load_foundation":
        return _ok_text(load_foundation().to_dict())
    if name == "consciousness_consult":
        situation = str(args.get("situation", "")).strip()
        if not situation:
            return _err_text("situation is required")
        return _ok_text(consult(situation).to_dict())
    if name == "consciousness_propose_feedback":
        situation = str(args.get("situation", "")).strip()
        observation = str(args.get("observation", "")).strip()
        if not situation or not observation:
            return _err_text("situation and observation are required")
        proposal = propose_feedback(
            situation=situation,
            observation=observation,
            suggested_adjustment=str(args.get("suggested_adjustment", "")),
            host_repo=str(args.get("host_repo", "unknown-host")),
            write=True,
        )
        return _ok_text(proposal.to_dict())
    if name == "consciousness_list_feedback_inbox":
        limit = int(args.get("limit") or 50)
        return _ok_text({"inbox": list_inbox(limit=limit)})
    if name == "consciousness_discernment_lookup":
        key = str(args.get("question_or_type", "")).strip()
        entry = lookup_discernment(key)
        return _ok_text({"entry": entry.to_dict() if entry else None})
    if name == "consciousness_list_vocabulary":
        return _ok_text(list_vocabulary())
    if name == "consciousness_manifest":
        return _ok_text(load_manifest().to_dict())
    # Backward-compatible aliases
    if name == "consciousness_load_posture":
        return _ok_text(load_foundation().to_dict())
    if name == "consciousness_advise":
        situation = str(args.get("question") or args.get("situation") or "").strip()
        if not situation:
            return _err_text("situation/question is required")
        return _ok_text(consult(situation).to_dict())
    return _err_text(f"Unknown tool: {name}")


def _write(message: dict) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _handle(message: dict) -> dict | None:
    method = message.get("method")
    msg_id = message.get("id")
    params = message.get("params") or {}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        }

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}

    if method == "tools/call":
        name = str(params.get("name", ""))
        arguments = params.get("arguments") or {}
        result = call_tool(name, arguments if isinstance(arguments, dict) else {})
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}

    if method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    if msg_id is not None:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }
    return None


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(message, dict):
            continue
        response = _handle(message)
        if response is not None:
            _write(response)


if __name__ == "__main__":
    main()
