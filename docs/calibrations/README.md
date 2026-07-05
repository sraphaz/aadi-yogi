# Calibrations — reservadas aos criadores

Decisões já **aceitas** nos ADRs, mas com valores concretos a preencher por humanos calibradores (não por agentes).

| Arquivo | ADR | Status |
|---------|-----|--------|
| [`0001-dana.yaml`](0001-dana.yaml) | [0001](../decisions/0001-sustaining-model-dana.md) | pending |
| [`0003-health-reviewers.yaml`](0003-health-reviewers.yaml) | [0003](../decisions/0003-health-gate-interim.md) | pending |

## Como fechar uma calibração

1. Editar o YAML com valores finais (`status: calibrated`).
2. Anexar emenda no ADR correspondente (seção **Amendment history**).
3. Se ADR-0003: promover salas `arriving` → `open` só após dois nomes registrados.
4. Rodar `./scripts/validate/check_calibrations.py` (deve imprimir `OK`).

Agentes **não** preenchem estes campos — apenas mantêm o scaffold e a cerca técnica.
