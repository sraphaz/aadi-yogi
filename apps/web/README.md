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

## Interface Darshan (design)

Esta interface mínima é um utilitário de consulta; a interface definitiva é o **Darshan**, cujo conceito e especificação estão em:

- `docs/darshan_interface_concept.md`: o conceito Darshan - princípios de design e os gestos.
- `docs/darshan_interface_spec.md`: telas, fluxos, contrato de resposta, métricas de presença, fases de construção.
- `docs/darshan_library_design.md`: a Biblioteca em camadas de profundidade (D0-D6, dial de profundidade, facetas, seis portas, salas de leitura).
- `docs/darshan_becoming_path.md`: o caminho de tornar-se - posturas, o dia como ashram, portas de situação, jornadas de leitura.
- `docs/darshan_sky_map_design.md`: gesto 8 - o Mapa do Céu (ritmo cósmico externo + céu interno dos cinco planos).
- `docs/darshan_nature_health_design.md`: gesto 9 - a Casa da Natureza (elementos, corpo, herança de saúde com cerca de responsabilidade).
- `docs/darshan_reuse_map.md`: mapa de reuso do oráculo implementado em github.com/sraphaz/darshan.
- `docs/skyforge/darshan/`: pacote de sessão Sky-Forge (brief, 39 RFs com critérios de aceitação, NFRs, UX spec, tokens de design, benchmark de mercado/MPI, modelo C4, índices SKY, maturidade).
