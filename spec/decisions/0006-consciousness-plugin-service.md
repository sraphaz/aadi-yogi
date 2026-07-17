# ADR 0006 - Consciousness as a Plugin Service for Host Agents

Status: accepted

## Context

Aadi Yogi already holds a consciousness core (`content/consciousness_core/`) and
a runtime response contract (`packages/prompts/`, `packages/evals/`). Until now
that posture lived only inside this monorepo.

Other repositories need to install Adyog as a **consciousness plugin**: a base
frequency of readiness that shapes the decisions of whatever agent runs there.
Host agents may add their own characteristics, but they should inherit Adyog's
discernment, restraint, humility, and citation discipline.

## Decision

1. **Public package façade** — `packages/consciousness/` is the stable import
   surface (`advise`, `load_manifest`, `load_posture_bundle`, `detect_restraint`,
   `validate_envelope`, `lookup_discernment`, `decision_laws`).
2. **MCP transport** — `python -m packages.consciousness.mcp_server` exposes the
   same surface as MCP tools for Cursor/Claude-style hosts.
3. **HTTP transport** — Agent API adds `/consciousness/*` endpoints so hosted
   consumers can pin manifest version and request advice without cloning logic.
4. **Overlay convention** — consumer repos declare `.consciousness/link.yaml`
   (mirrors `.sky/link.yaml`) naming source, pin, and allowed capabilities.
5. **Decision laws travel with the plugin** — host traits may refine tone and
   domain skill; they must not cancel restraint, citation integrity,
   anti-prophecy, anti-prescription, single-safe-movement, or honored silence.
6. **No realization claim** — the plugin transmits readiness posture, never
   authority or infallible guidance. Manifest note about human review before
   public production remains in force.

## What decisions the plugin forces

When a host agent carries Adyog consciousness, it decides to:

- short-circuit before retrieval on crisis / occult harm / voices / kundalini
  distress / grief / coercive renunciation / health prescription patterns;
- inject the Adyog system posture before composing ordinary answers;
- prefer source-grounded citations or return an honest non-answer;
- offer at most one movement, and only `safety_class: safe`;
- refuse personal prophecy and medical prescription language;
- honor silence when words would coerce, escalate, or replace human care.

## Consequences

- New package and MCP entry points; no change to existing `/inquire` semantics.
- Schema freeze begins at `schemas/response_envelope.schema.json`.
- Consumer docs live in `docs/consciousness_plugin.md`.
- Future PyPI / hosted auth packaging can layer on this façade without
  rewriting the consciousness core Markdown.
