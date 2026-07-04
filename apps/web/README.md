# Web App

Interface web mínima para consultar o agente Aadi Yogi.

## Como usar

1. Suba a API:

```bash
pnpm api:dev
# ou
PYTHONPATH=. uvicorn apps.agent-api.main:app --reload --host 0.0.0.0 --port 8000
```

2. Abra `http://localhost:8000/` no navegador.

## Endpoints

- `GET /` — interface web
- `POST /ask` — resposta completa (LLM se configurado, fallback caso contrário)
- `POST /retrieve` — apenas trechos recuperados
- `POST /prompt` — prompt montado para inspeção

## LLM opcional

Configure uma API compatível com OpenAI:

```bash
export AADI_YOGI_LLM_API_KEY=...
export AADI_YOGI_LLM_BASE_URL=https://api.openai.com/v1
export AADI_YOGI_LLM_MODEL=gpt-4o-mini
```

Sem chave, o sistema responde em modo fallback compondo trechos recuperados.
