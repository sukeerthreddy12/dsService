# Finance Tracker — DS Service

Python Flask service for message / LLM processing. Part of the Finance Tracker application (Kafka + Kong).

## Stack

- Python / Flask
- Kafka producer
- Mistral (via `OPENAI_API_KEY` env name used by the client)

## Setup

```bash
cp .env.example src/app/.env
# put your API key and Kafka broker in src/app/.env
uv sync
# run from src/ so app imports resolve
cd src && uv run python -m app
```

Or use the included `Dockerfile`.

## Env

Copy `.env.example` → `src/app/.env`. Never commit `.env`.
