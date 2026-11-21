# Finance Tracker — DS Service

Python Flask service for **data-science / NLP expense extraction**. Clients send a free-text message (e.g. “coffee 5 dollars yesterday”); this service uses an LLM (Mistral) to extract a structured expense, then **publishes it to Kafka** so Expense Service can save it.

Part of the Finance Tracker microservices app (Kong + Kafka).

**System map:** see [ARCHITECTURE.md in Auth](https://github.com/sukeerthreddy12/FinanceTrackerApplication/blob/main/ARCHITECTURE.md)

## What this service does

- Accept `POST /v1/ds/message` with `message` + `user_id`
- Run LLM structured extraction into an `Expense` model
- Produce a Kafka message on topic `expense_service`
- Return a simple success/error HTTP response (persistence happens asynchronously in Expense Service)

It does **not** write to MySQL itself — Expense Service is the store.

## Main HTTP API

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/v1/ds/message` | Parse NL message → Kafka expense event |
| GET | `/` | Health / hello |

Expose this path through Kong in production (dedicated route to DS port **8010**).

## Kafka

| Direction | Topic | Meaning |
|-----------|-------|---------|
| Produce | `expense_service` | Extracted expense for Expense Service |

## Stack

- Python / Flask
- LangChain + Mistral (`OPENAI_API_KEY` env name used by the client)
- Kafka producer
- Optional Docker image (`Dockerfile`)

## Setup

```bash
cp .env.example src/app/.env
# put API key + Kafka broker in src/app/.env
uv sync
cd src && uv run python -m app
```

Default port: **8010**.

## Env

Copy `.env.example` → `src/app/.env`. Never commit `.env`.

## Related repos

- [Expense Service](https://github.com/sukeerthreddy12/FinanceTrackerExpenseService) (consumes this service’s events)
- [Auth](https://github.com/sukeerthreddy12/FinanceTrackerApplication) · [User](https://github.com/sukeerthreddy12/FinanceTrackerUserService) · [Frontend](https://github.com/sukeerthreddy12/FinanceTrackerFrontend)
