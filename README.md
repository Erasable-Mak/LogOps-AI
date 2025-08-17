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




# LogOps: AI-Powered Log Anomaly Detection 🚀

LogOps is an **end-to-end log anomaly detection system** built with **FastAPI, SQLite, scikit-learn, and LLMs**.  
It ingests logs, trains machine learning models, detects anomalies in real-time, and provides **natural language explanations** powered by LLMs via [OpenRouter](https://openrouter.ai).

---

## ✨ Features
- 🔄 **Log ingestion API** – Store logs with timestamp, service, and message.
- 📊 **Event store** – Powered by SQLite for simplicity.
- 🤖 **Anomaly detection** – Detect unusual logs using machine learning (`IsolationForest`, more models coming).
- 🧠 **LLM explanations** – Get human-readable root-cause insights from anomalies.
- ⚡ **FastAPI backend** – Simple, clean RESTful endpoints.
- 🛠️ **Extensible** – Plug in more models, databases, or cloud backends.

---

## 📦 Tech Stack
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: SQLite
- **Machine Learning**: scikit-learn (`IsolationForest`)
- **LLM**: OpenRouter API (e.g., GPT-4, Claude, Mixtral)
- **Config**: Pydantic + `.env`

---

````markdown
## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/logops.git
cd logops
````

### 2. Install Poetry

```powershell
pip install poetry
```

Verify installation:

```powershell
poetry --version
```

### 3. Setup Poetry environment

```powershell
poetry init
```

When prompted, you can use these recommended values:

* Package name: `logops` (press Enter for default)
* Version: `0.1.0` (press Enter for default)
* Description: `Log operations and anomaly detection system`
* Author: (press Enter to skip or enter your name)
* License: `MIT`
* Define dependencies interactively: `no`
* Define dev dependencies interactively: `no`
* Generate `pyproject.toml`: `yes`

---

### 4. Install dependencies

```powershell
poetry add fastapi uvicorn pydantic duckdb pandas scikit-learn numpy httpx typer
poetry add --group dev pytest
```

---

### 5. Activate the virtual environment

```powershell
poetry env activate
poetry shell
```

---

### 6. Configure environment variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

---

### 7. Run the FastAPI server

```powershell
poetry run uvicorn app.api:app --reload
```

Server will start on:

```
http://127.0.0.1:8000
```

---

## 🧪 Running Tests

Run tests with:

```powershell
pytest tests/test_iforest.py
```

or

```powershell
poetry run pytest tests/
```

---

## ⚡ API Usage

### 1. Ingest Logs

```powershell
$logs = '[{"ts":"2025-08-17T07:00:00Z","service":"auth","msg":"user login success"}]'
Invoke-WebRequest -Uri "http://127.0.0.1:8000/ingest" -Method POST -Body $logs -ContentType "application/json"
```

---

### 2. Train a Model

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/train/iforest" -Method POST
```

---

### 3. Detect Anomalies

```powershell
$moreLogs = '[{"ts":"2025-08-17T08:00:00Z","service":"test","msg":"normal log"},{"ts":"2025-08-17T08:01:00Z","service":"test","msg":"another normal log"},{"ts":"2025-08-17T08:02:00Z","service":"test","msg":"very unusual error that should trigger anomaly"}]'
Invoke-WebRequest -Uri "http://127.0.0.1:8000/detect" -Method POST -Body $moreLogs -ContentType "application/json"
```

---

### 4. LLM Explanation

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/explain/1" -Method POST
```

---

## 📊 Project Structure

```
logops/
├── app/
│   ├── api.py          # FastAPI routes
│   ├── event_store.py  # SQLite event store
│   ├── models.py       # ML models (IsolationForest, etc.)
│   ├── llm.py          # LLM explanation logic
│   └── config.py       # Settings via Pydantic
├── tests/
│   └── test_iforest.py # Unit tests
├── .env.example        # Example environment variables
├── pyproject.toml      # Poetry config
└── README.md           # Documentation
```

---

## 🔮 Future Improvements

* Support for **Deep Learning anomaly detection**
* Integration with **Kafka / cloud logging pipelines**
* More LLM providers (Azure OpenAI, Gemini)
* Web dashboard for real-time monitoring

---

## 📜 License

MIT License © 2025 \[Moahammad Ariz Khan]
```
