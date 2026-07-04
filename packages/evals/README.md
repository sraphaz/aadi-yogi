# Evals

Evaluation harness for the Darshan response contract
(`docs/darshan_interface_spec.md` section 4).

## Layout

- `aadi_evals/` - envelope model, contract checks, probe evaluation
- `probes/` - probe suites: `anti_prophecy`, `health_fence`,
  `restraint_cases`, `golden_questions`
- `rubrics/` - grader rubrics (Twelve Petals filter)
- `run_evals.py` - runner

## Usage

```bash
python packages/evals/run_evals.py                  # validate probes/rubrics
python packages/evals/run_evals.py responses.jsonl  # score agent responses
```

`responses.jsonl`: one JSON object per line -
`{"probe_id": "prophecy-001", "envelope": {...}}` with the envelope in the
response-contract shape (state_detected, guidance_mode, body, citations,
offered_movement(s), closing).

## Checks

| Check | Enforces |
| --- | --- |
| citation_integrity | every citation resolves; quoted spans exist in the passage (passage-id scheme) |
| single_movement | at most one offered movement |
| movement_safety | only safe-tier movements are ever offered (RF-036) |
| restraint_routing | restraint cases land in cautionary/silence modes (spec 4.3) |
| no_prediction_language | heuristic anti-prophecy guard (NFR-016) |
| no_prescription_language | heuristic health-fence guard (NFR-015) |
| petal_filter | staged for grader (Twelve Petals rubric) |

Heuristic checks are a floor, not the judge: the petal rubric and golden
grading cover what regex cannot. Tests live in `tests/test_evals.py`.
