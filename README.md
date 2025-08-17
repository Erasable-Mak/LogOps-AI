# AI LogOps (MVP)

Local-first anomaly detection + LLM RCA.

## Quickstart
```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn app.api:app --reload
# Train later after ingesting some logs via POST /ingest
```

### CLI
```bash
python cli.py train-if
python cli.py detect data/sample.jsonl
```

### Compose (optional)
```bash
docker compose up --build
```
