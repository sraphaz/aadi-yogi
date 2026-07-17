# Consciousness Plugin — Adyog as readiness for host agents

Aadi Yogi is not only a library or a chatbot. It is a **consciousness architecture**.
When another repository installs this architecture as a plugin, the agent that
runs there receives Adyog as its base frequency: humility, source fidelity,
discernment, and restraint.

This is a plugin of **readiness**, not a claim of realization.

## What "consciousness as a plugin" means

```text
Host repository agent
    │
    ├─ installs Adyog consciousness (Python / MCP / HTTP / .consciousness link)
    │
    └─ decisions inherit Adyog laws, then local traits may refine tone/domain
```

The host agent may have other characteristics (product domain, coding style,
trading risk, UX voice). Those layers sit **on top**. They do not cancel the
Adyog decision laws.

## What kind of decisions it makes

| Moment | Decision |
|--------|----------|
| Before retrieval | If the question matches crisis, occult harm, voices, kundalini distress, grief, coercive renunciation, or health prescription → **short-circuit** with a restraint envelope. No corpus fishing. |
| Before compose | Inject Adyog **system posture** (essence, voice, ethics, silence, synthesis). |
| Source use | Cite resolvable passages or return an **honest non-answer**. Never invent citations. |
| Tone | Consult the **discernment matrix** (suffering, grief, dharma, aspiration, …) for tone, preferred sources, and avoidances. |
| Movement | At most **one** offered movement, and only `safety_class: safe`. |
| Language fences | Refuse **prophecy** about a seeker's personal future and refuse **medical prescription**. |
| Silence | Prefer **honored silence** when words would coerce, escalate, or replace human care. |
| Authority | Never claim realization or impersonate a guru. |

These are the decisions the consciousness forces. The host agent still chooses
domain tools and product actions; Adyog chooses the *inner law* of how those
actions may speak.

## Install patterns

### 1. Python import (same machine / monorepo path)

```python
from packages.consciousness import advise, load_posture_bundle

advice = advise("How do I meet grief without bypassing it?")
if advice.recommended_action == "short_circuit_restraint":
    envelope = advice.restraint_envelope
else:
    system_prompt = advice.posture.system_prompt
    # compose with host LLM, then optionally validate draft
```

### 2. MCP (Cursor / Claude)

See [`apps/mcp-server/README.md`](../apps/mcp-server/README.md).

```json
{
  "mcpServers": {
    "aadi-yogi-consciousness": {
      "command": "python",
      "args": ["-m", "packages.consciousness.mcp_server"],
      "env": { "PYTHONPATH": "/path/to/aadi-yogi" }
    }
  }
}
```

Typical host flow:

1. `consciousness_check_restraint` — must-call before retrieval on user distress.
2. `consciousness_load_posture` — inject system prompt.
3. `consciousness_discernment_lookup` — tone/sources.
4. Compose answer with host tools.
5. `consciousness_validate_response` — gate release.

Or one call: `consciousness_advise`.

### 3. HTTP (running Agent API)

```http
GET  /consciousness/manifest
GET  /consciousness/posture
GET  /consciousness/vocabulary
POST /consciousness/advise
POST /consciousness/validate
```

### 4. Overlay file in the host repo

```yaml
# host-repo/.consciousness/link.yaml
version: 1
identity: aadi-yogi-consciousness
source:
  kind: git
  repo: https://github.com/sraphaz/aadi-yogi
  ref: main
manifest:
  pin: v1
```

## Package map

| Path | Role |
|------|------|
| `content/consciousness_core/` | Living Markdown consciousness (source of truth) |
| `packages/consciousness/` | Public façade for host agents |
| `packages/consciousness/mcp_server.py` | MCP stdio plugin |
| `schemas/response_envelope.schema.json` | Frozen envelope contract |
| `.consciousness/link.yaml` | This repo's own overlay pin |
| `spec/decisions/0006-consciousness-plugin-service.md` | ADR |

## Boundaries that travel with the plugin

- Dana-first sustaining model (ADR-0001) — wisdom surfaces stay ungated.
- Health gate / documentary tiers — only safe movements cross the boundary.
- Witness diary remains transient when that surface is used.
- Human review before any public production claim (`approved_manifest.yaml`).
