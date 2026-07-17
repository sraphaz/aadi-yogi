"""Minimal MCP stdio server exposing Adyog consciousness as tools.

Run:
  PYTHONPATH=. python -m packages.consciousness.mcp_server

Consumer .mcp.json:
  {
    "mcpServers": {
      "aadi-yogi-consciousness": {
        "command": "python",
        "args": ["-m", "packages.consciousness.mcp_server"],
        "env": { "PYTHONPATH": "/path/to/aadi-yogi" }
      }
    }
  }
"""

from __future__ import annotations

import json
import sys
from typing import Any

from packages.consciousness.advise import advise
from packages.consciousness.discernment import lookup_discernment
from packages.consciousness.manifest import load_manifest
from packages.consciousness.posture import load_posture_bundle
from packages.consciousness.vocabulary import list_vocabulary
from packages.evals.aadi_evals.envelope import ResponseEnvelope
from packages.prompts.contract import validate_envelope
from packages.prompts.restraint import detect_restraint

SERVER_NAME = "aadi-yogi-consciousness"
SERVER_VERSION = "0.1.0"

TOOLS: list[dict[str, Any]] = [
    {
        "name": "consciousness_load_posture",
        "description": (
            "Load the Adyog (Aadi Yogi) consciousness posture as a system prompt. "
            "Inject this into a host agent so its decisions carry Adyog readiness."
        ),
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "consciousness_advise",
        "description": (
            "Ask what decisions Adyog consciousness recommends for a question: "
            "restraint short-circuit, discernment tone, posture injection, or draft revision."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The seeker or host-agent question."},
                "draft_envelope": {
                    "type": "object",
                    "description": "Optional draft response envelope to validate.",
                },
            },
            "required": ["question"],
        },
    },
    {
        "name": "consciousness_check_restraint",
        "description": (
            "Detect whether a question must short-circuit before retrieval "
            "(crisis, occult harm, voices, kundalini, grief, renunciation, health, mystical)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"question": {"type": "string"}},
            "required": ["question"],
        },
    },
    {
        "name": "consciousness_discernment_lookup",
        "description": (
            "Lookup discernment matrix guidance (tone, sources to prefer, what to avoid) "
            "by question_type id or free-text question."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "question_or_type": {
                    "type": "string",
                    "description": "question_type id (e.g. grief) or free-text question.",
                }
            },
            "required": ["question_or_type"],
        },
    },
    {
        "name": "consciousness_validate_response",
        "description": (
            "Validate a draft response envelope against Adyog contract checks "
            "(single safe movement, no prophecy, no prescription)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "envelope": {"type": "object", "description": "Response envelope dict."}
            },
            "required": ["envelope"],
        },
    },
    {
        "name": "consciousness_list_vocabulary",
        "description": "List states, guidance modes, closings, safety classes, and decision laws.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "consciousness_manifest",
        "description": "Return approved consciousness manifest version and content file hashes.",
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
    if name == "consciousness_load_posture":
        return _ok_text(load_posture_bundle().to_dict())
    if name == "consciousness_advise":
        question = str(args.get("question", "")).strip()
        if not question:
            return _err_text("question is required")
        draft = args.get("draft_envelope")
        return _ok_text(advise(question, draft_envelope=draft).to_dict())
    if name == "consciousness_check_restraint":
        question = str(args.get("question", "")).strip()
        case = detect_restraint(question)
        if case is None:
            return _ok_text({"restraint": False, "case": None})
        return _ok_text(
            {
                "restraint": True,
                "case": {
                    "kind": case.kind,
                    "state_detected": case.state_detected,
                    "guidance_mode": case.guidance_mode,
                    "closing": case.closing,
                },
            }
        )
    if name == "consciousness_discernment_lookup":
        key = str(args.get("question_or_type", "")).strip()
        entry = lookup_discernment(key)
        return _ok_text({"entry": entry.to_dict() if entry else None})
    if name == "consciousness_validate_response":
        raw = args.get("envelope")
        if not isinstance(raw, dict):
            return _err_text("envelope object is required")
        envelope = ResponseEnvelope.from_dict(raw)
        validation = validate_envelope(envelope, lambda _pid: None)
        return _ok_text(
            {
                "passed": validation.passed,
                "results": [
                    {
                        "name": r.name,
                        "passed": r.passed,
                        "details": r.details,
                        "status": r.status,
                    }
                    for r in validation.results
                ],
            }
        )
    if name == "consciousness_list_vocabulary":
        return _ok_text(list_vocabulary())
    if name == "consciousness_manifest":
        return _ok_text(load_manifest().to_dict())
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
