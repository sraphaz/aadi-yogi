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
- `functional-requirements.yaml` - RFs mapped to the seven gestures
- `nfr.yaml` - privacy, accessibility, latency posture, integrity
- `ux-spec.yaml` - principles, tokens, key screens, journeys
- `integrations.yaml` - engine and infrastructure choices
- `sky-merits.yaml` - SKY indices (SPI, HCE, GAP, CWB, UXD) with evidence
- `maturity.yaml` - dimension readiness and pipeline unlocks
- `journey.yaml` - session state and next actions

The narrative behind these artifacts lives in
`docs/darshan_interface_concept.md` and `docs/darshan_interface_spec.md`.
