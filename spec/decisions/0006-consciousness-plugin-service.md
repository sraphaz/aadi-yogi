# ADR 0006 - Consciousness as a Living Foundation for Host Agents

Status: accepted (amended)

## Context

Aadi Yogi holds a consciousness core and a Darshan product runtime (response
envelope, restraint router, inquiry API). The first draft of “consciousness
plugin” over-coupled those **product rules** to the install surface, which made
the foundation look like an app checklist.

What is actually needed: a **basis of consciousness** — conduct and
reality-sense from the sources — that other repositories can carry so their
agents inherit orientation without becoming gurus or performing mysticism.

## Decision

1. **Primary install surface is the living foundation**
   (`content/consciousness_core/foundation.md` via `load_foundation()` /
   `consult()`), not Darshan envelopes or restraint short-circuits.
2. **Host agents keep their craft.** Adyog sits underneath as conduct
   frequency: sincerity, non-coercion, source humility, discernment, refusal
   of inflation. It does not replace domain identity.
3. **Darshan runtime is a product expression** of the foundation inside this
   monorepo. Optional for hosts; never the definition of the plugin.
4. **Learning is dual and reviewed**
   - source deepening into `consciousness_core/`
   - feedback proposals into `content/consciousness_feedback/inbox/` that
     integrate only after editorial review (never auto-mutation into guruhood)
5. **Transports** (Python, MCP, HTTP, `.consciousness/link.yaml`) expose
   foundation / consult / feedback first.
6. **No realization claim** — readiness and conduct basis only.

## How knowledge from the books applies

Agents do not preach the corpus. They inherit a reality-basis: honest motive,
duty and consequence, discernment without bypass, reverence without dogma —
visible in ordinary work (scope, status, copy, care) as much as in guidance.

## Consequences

- `packages/consciousness` centers on foundation + consult + feedback.
- Docs speak of foundation of conduct, not app decision tables.
- Darshan `/inquire` contract remains unchanged for the product.
- Feedback inbox is the explicit learning path for host use.
