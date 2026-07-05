# Sky-Forge Session Package - Darshan

Maturity package for the Darshan interface, formatted as a
[Sky-Forge](https://github.com/sraphaz/sky-forge) session so it can be dropped
into `.sky/sessions/darshan/` of a Sky-Forge checkout and continued with the
intake/elevation/export pipeline:

```powershell
# inside a sky-forge checkout
Copy-Item -Recurse path/to/aadi-yogi/docs/skyforge/darshan .sky/sessions/darshan
./scripts/sky/sky.ps1 status -Slug darshan
./scripts/sky/sky.ps1 elevate -Slug darshan
./scripts/sky/sky.ps1 export -Slug darshan -Completeness partial
```

Artifacts follow the session template of `templates/sessions/example-horta`:

Artifacts (regenerated against Sky-Forge spec v1.2 and its published schemas in `docs/schemas/`):

- `brief-draft.yaml` - problem, users, value, scope
- `functional-requirements.yaml` - 41 RFs with acceptance criteria, mapped to the gestures, the library depths, the becoming path, the Sky Map, the House of Nature and the evidenced elevations
- `nfr.yaml` - schema-conformant (category/statement/target/tier_minimum): privacy, accessibility, latency posture, integrity, scripts, bundles, health fence, anti-prophecy
- `ux-spec.yaml` - principles, key screens (incl. depth dial, situation doors, sky map, nature house), journeys, Cloud Design tracks
- `design-tokens.yaml` - four hour-themes, typography (incl. Devanagari/Tamil/IAST), motion, semantic tokens
- `integrations.yaml` - engine, infrastructure, local ephemeris and observance calendar choices
- `alternatives.yaml` - resolved decisions (dana model, natal boundary) and open topics with recommendations
- `approvals.yaml` - session ledger: elevation review, consciousness decisions, pending creator calibrations
- `sky-merits.yaml` - spec v1.2: SKY_SCORE **72** (Horizon) with the elevation trail evidenced (RF-040/RF-029/RF-041); MPI 68 alongside
- `market-benchmark.yaml` - four segments, per-axis verdicts, gap suggestions (MPI lens)
- `c4-model.md` - C4 levels 1-3 over the monorepo, with draft ADRs
- `maturity.yaml` - dimension readiness and pipeline unlocks
- `journey.yaml` - session state and next actions

The repository root also carries `.sky/link.yaml` (sky link feature), binding this repo to the `darshan` session for forge-driven `status` / `pull-spec` / `export -ForAI` workflows.

The narrative behind these artifacts lives in
`docs/darshan_interface_concept.md`, `docs/darshan_interface_spec.md`,
`docs/darshan_library_design.md`, `docs/darshan_becoming_path.md`,
`docs/darshan_sky_map_design.md` and `docs/darshan_nature_health_design.md`.

Decisions taken from the consciousness core are recorded in
`docs/decisions/` (sustaining model, natal boundary, health gate, editorial
policy, passage-id scheme). The passage-id design is
`docs/passage_id_scheme.md`; the implemented eval harness is
`packages/evals/`.
