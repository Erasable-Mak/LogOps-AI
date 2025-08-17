from pydantic import BaseModel

class LogRecord(BaseModel):
    ts: str
    service: str
    level: str | None = None
    msg: str
    host: str | None = None
    source: str | None = None
    pod: str | None = None
    trace_id: str | None = None
    raw: str | None = None

class AnomalyOut(BaseModel):
    id: int
    ts: str
    service: str
    score: float
    severity: str
    reason: str

class RCAOut(BaseModel):
    root_cause: str
    impact: str
    remediation: list[str]
    confidence: float
