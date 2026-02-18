# Bitcoin-Test

Local-first autonomous agent scaffold that uses **OpenAI** cloud models and includes guarded trading primitives for **Binance AUS / BTC** workflows.

## What changed
This repository now includes a runnable Milestone-0 style code scaffold:
- `agent_core/` (settings, LLM gateway, run loop)
- `policy/` (policy engine for shell/path/trade controls)
- `tooling/` (guarded local tool executor)
- `memory/` (run-event memory store)
- `trading/` (trade intent evaluator with daily-risk cap)
- `api/` (FastAPI endpoints)
- `tests/` (policy/trading/API checks)

## Fixed defaults from your decisions
- Cloud LLM provider: **OpenAI**
- Exchange: **Binance AUS**
- Asset focus: **Bitcoin** (`BTCUSDT`)
- Daily loss limit: **$20**
- Runtime: **Python**
- Dashboard in all versions: **enabled flag set true**

## Quick start
Requires Python 3.10+ and internet access for first-time dependency install.

```bash
python3 -m venv .venv
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
# add your OPENAI_API_KEY in .env
uvicorn api.app:app --reload
```

Then check:
- `GET /health`
- `POST /trade/intent`
- `POST /agent/run` (requires `OPENAI_API_KEY`)

## Environment
Use `.env` (see `.env.example`) for secrets and overrides.
Starter repo for building a local autonomous AI agent that uses cloud LLMs and can be extended for real-time trading workflows.

## Start here

Read the bootstrap plan:
- [PROJECT_BOOTSTRAP.md](./PROJECT_BOOTSTRAP.md)
