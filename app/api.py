from fastapi import FastAPI, Depends
from .schemas import LogRecord, AnomalyOut, RCAOut
from .deps import get_pipeline

app = FastAPI(title="AI LogOps")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(records: list[LogRecord], pipe=Depends(get_pipeline)):
    n = pipe.ingest(records)
    return {"ingested": n}

@app.post("/train/iforest")
def train_if(pipe=Depends(get_pipeline)):
    stats = pipe.train_iforest()
    return stats

@app.post("/detect")
def detect(records: list[LogRecord], pipe=Depends(get_pipeline)):
    out = pipe.detect(records)
    return {"anomalies": out}

@app.get("/anomalies", response_model=list[AnomalyOut])
def list_anoms(since: str | None = None, service: str | None = None, pipe=Depends(get_pipeline)):
    return pipe.list_anomalies(since, service)

@app.post("/explain/{anomaly_id}", response_model=RCAOut)
def explain(anomaly_id: int, pipe=Depends(get_pipeline)):
    return pipe.explain(anomaly_id)
