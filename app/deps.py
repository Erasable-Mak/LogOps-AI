from .settings import Settings
from core.ingest import Ingestor
from core.featurize import TextFeaturizer
from core.anomaly_iforest import IFServiceModel
from core.events import EventStore
from llm.explain_ollama import OllamaExplainer
from llm.prompts import SYSTEM_PROMPT, user_prompt
from model_registry import ModelRegistry
from datapaths import DATA_DIR, DB_PATH
import duckdb  # type: ignore
import sqlite3
from datetime import datetime

class Pipeline:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.ingestor = Ingestor()
        self.featurizer = TextFeaturizer()
        self.registry = ModelRegistry(DATA_DIR / "models")
        self.events = EventStore(DB_PATH)  # Pass path, not connection
        # Fix: OllamaExplainer doesn't take parameters
        self.explainer = OllamaExplainer()
        self.conn = duckdb.connect(str(DATA_DIR / "lake.duckdb"))
        self.conn.execute("CREATE TABLE IF NOT EXISTS logs(ts TIMESTAMP, service VARCHAR, level VARCHAR, msg VARCHAR, host VARCHAR, source VARCHAR, pod VARCHAR, trace_id VARCHAR)")

    def ingest(self, records: list[dict]) -> int:
        # Convert Pydantic models to dicts if needed
        if records and hasattr(records[0], 'model_dump'):
            records = [r.model_dump() for r in records]
        
        # persist to duckdb
        if not records:
            return 0
        df = self.ingestor.normalize(records)
        self.conn.register("df", df)
        self.conn.execute("INSERT INTO logs SELECT * FROM df")
        return len(df)

    def train_iforest(self):
        # train per service simple model
        services = [r[0] for r in self.conn.execute("SELECT DISTINCT service FROM logs").fetchall() if r[0]]
        stats = {}
        for svc in services:
            df = self.conn.execute("SELECT msg FROM logs WHERE service = ?", [svc]).df()
            if len(df) < 50:
                stats[svc] = {"skipped": True, "reason": "not_enough_data"}
                continue
            X = self.featurizer.transform(df["msg"].tolist())
            model = IFServiceModel().fit(X)
            self.registry.save_iforest(svc, model, self.featurizer)
            stats[svc] = {"trained": True, "samples": len(df)}
        return stats

    def detect(self, records: list[dict]):
        # Convert Pydantic models to dicts if needed
        if records and hasattr(records[0], 'model_dump'):
            records = [r.model_dump() for r in records]
        
        # on-the-fly detection for a batch (no write to lake to keep simple)
        df = self.ingestor.normalize(records)
        out = []
        by_service = {}
        for _, row in df.iterrows():
            by_service.setdefault(row.service, []).append(row.msg)
        for svc, msgs in by_service.items():
            model_bundle = self.registry.load_iforest(svc)
            if not model_bundle:
                continue
            model, feat = model_bundle
            X = feat.transform(msgs)
            scores = model.score(X)
            for i, s in enumerate(scores):
                if s > 2.0:  # simple threshold
                    anomaly_id = self.events.write(
                        ts=str(datetime.utcnow()),
                        service=svc,
                        score=float(s),
                        severity="HIGH" if s > 3.0 else "MEDIUM",
                        reason="anomalous_log_line",
                        context_path="",
                        start_offset=0,
                        end_offset=0
                    )
                    out.append({"id": anomaly_id, "service": svc, "score": float(s)})
        return out

    def list_anomalies(self, since: str | None, service: str | None):
        return self.events.list(since=since, service=service)

    def explain(self, anomaly_id: int):
        ev = self.events.get(anomaly_id)
        if not ev:
            return {"root_cause": "", "impact": "", "remediation": [], "confidence": 0.0}
        # fetch minimal context from lake
        ctx = self.conn.execute("SELECT ts, service, level, msg FROM logs WHERE service = ? ORDER BY ts DESC LIMIT 30", [ev["service"]]).df()
        bullets = "\n".join(f"- [{r['ts']}] {r['level']}: {r['msg']}" for _, r in ctx.iterrows())
        up = user_prompt(service=ev["service"], t0="N/A", t1="N/A", th=2.0, bullets=bullets, context="")
        return self.explainer.explain(SYSTEM_PROMPT, up)

_settings = Settings()
_pipeline = Pipeline(_settings)

def get_pipeline():
    return _pipeline
