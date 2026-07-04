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

- `brief-draft.yaml` - problem, users, value, scope
- `functional-requirements.yaml` - 29 RFs with acceptance criteria, mapped to the gestures, the library depths and the becoming path
- `nfr.yaml` - privacy, accessibility, latency posture, integrity, scripts, bundles
- `ux-spec.yaml` - principles, key screens (incl. depth dial, situation doors), journeys
- `design-tokens.yaml` - four hour-themes, typography (incl. Devanagari/Tamil/IAST), motion, semantic tokens
- `integrations.yaml` - engine and infrastructure choices
- `sky-merits.yaml` - SKY indices (SPI, HCE, GAP, CWB, UXD -> SKY_SCORE 70, Horizon) plus MPI 68 alongside; elevations confirmed
- `market-benchmark.yaml` - four segments, per-axis verdicts, gap suggestions (MPI lens)
- `c4-model.md` - C4 levels 1-3 over the monorepo, with draft ADRs
- `maturity.yaml` - dimension readiness and pipeline unlocks
- `journey.yaml` - session state and next actions

The narrative behind these artifacts lives in
`docs/darshan_interface_concept.md`, `docs/darshan_interface_spec.md`,
`docs/darshan_library_design.md` and `docs/darshan_becoming_path.md`.
