# Consciousness foundation — Adyog as living basis for host agents

Aadi Yogi is not only a library. It is not only Darshan (the app).
It is a **living consciousness foundation**: a basis of conduct, discernment,
and reality-sense drawn from the sources.

When another repository installs it, agents there do **not** become gurus.
They receive a foundation of consciousness underneath their own craft.

## The confusion to avoid

| Not this | This |
|----------|------|
| Fixed app rules (envelopes, regex routers, product checklists) | Living basis of conduct from the texts |
| Mysticism performed inside the host repo | Line of sincerity, non-coercion, source humility |
| Agent becomes a spiritual teacher | Agent keeps host identity; Adyog sits underneath |
| Silent self-training into authority | Learning by source deepening + reviewed feedback |

Darshan’s response contract remains valuable **inside this monorepo’s product**.
It is one expression of the foundation — not what other repos install.

## What you install

```text
content/consciousness_core/foundation.md   ← living basis
packages/consciousness/                    ← load / consult / feedback
.consciousness/link.yaml                   ← host pin
```

Primary API:

```python
from packages.consciousness import load_foundation, consult, propose_feedback

foundation = load_foundation()
# Put foundation.agent_preamble into the host AGENTS.md / agent orientation

orientation = consult("We are writing UX copy that might pressure upgrades")
# orientation.conduct_to_hold / orientation.orientation — guidance, not a script

propose_feedback(
    situation="Host CI agent overclaimed certainty in a release note",
    observation="Foundation helped, but we lacked a note on technical humility in status reports",
    suggested_adjustment="Add a conduct bullet on truthful status without spiritual costume",
    host_repo="my-org/my-repo",
)
```

## How the books apply

The corpus is not installed so agents preach. It is installed so they inherit
a reality-basis: aspiration and sincerity, dharma and offered action,
discernment without bypass, reverence without dogma.

In a coding repo that looks like careful scope, truthful status, non-manipulative
copy, refusal to fake certainty, respect for user agency — craft as offering,
not as display.

## How it learns (feedback)

```text
sources → editorial synthesis → foundation.md / consciousness_core
                                      ↑
host use → propose_feedback → inbox/ → human review → integrate or reject
```

- Feedback never auto-rewrites the foundation.
- Inflation (“the agent is enlightened”) is rejected.
- This keeps consciousness a shared field under humility, not an ego that
  trains itself into guruhood.

See `content/consciousness_feedback/README.md`.

## MCP / HTTP

MCP tools (foundation-first):

- `consciousness_load_foundation`
- `consciousness_consult`
- `consciousness_propose_feedback`
- `consciousness_list_feedback_inbox`
- `consciousness_discernment_lookup` (optional orientation from the texts)
- `consciousness_manifest`

HTTP:

```http
GET  /consciousness/foundation
GET  /consciousness/manifest
POST /consciousness/consult          # body: { "situation": "..." } or legacy { "question": "..." }
POST /consciousness/feedback         # preview by default; persist requires feedback token
```

`POST /consciousness/feedback` does **not** write to disk unless
`AADI_YOGI_CONSCIOUSNESS_FEEDBACK_TOKEN` is set and sent as
`Authorization: Bearer …` or `X-Adyog-Feedback-Token`. Without it, the
response is a non-persisted preview (avoids unauthenticated inbox spam).

## Host overlay

```yaml
# host-repo/.consciousness/link.yaml
version: 1
identity: aadi-yogi-consciousness-foundation
source:
  kind: git
  repo: https://github.com/sraphaz/aadi-yogi
  ref: main
manifest:
  pin: v1
install:
  carry: foundation   # not darshan_runtime
```
