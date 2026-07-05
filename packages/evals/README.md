# Evals

Two complementary evaluation layers live here.

## 1. Retrieval and response quality (engine scaffold)

- `golden_questions.json` - golden questions over the imported corpus
- `response_quality.py`, `runner.py` - retrieval hit and response quality
  checks used by `scripts/validate/run_golden_questions.py` and
  `scripts/validate/run_response_eval.py`

## 2. Darshan response-contract harness

Evaluation harness for the Darshan response contract
(`docs/darshan_interface_spec.md` section 4).

- `aadi_evals/` - envelope model, contract checks, probe evaluation
- `probes/` - probe suites: `anti_prophecy`, `health_fence`,
  `restraint_cases`, `golden_questions`
- `rubrics/` - grader rubrics (Twelve Petals filter)
- `run_evals.py` - runner

### Usage

```bash
python packages/evals/run_evals.py                  # validate probes/rubrics
python packages/evals/run_evals.py responses.jsonl  # score agent responses
```

`responses.jsonl`: one JSON object per line -
`{"probe_id": "prophecy-001", "envelope": {...}}` with the envelope in the
response-contract shape (state_detected, guidance_mode, body, citations,
offered_movement(s), closing).

### Checks

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

As the agent API evolves to emit the contract envelope, layer 1's golden
questions should migrate into layer 2 probes so one harness gates releases.
