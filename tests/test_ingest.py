from core.ingest import Ingestor
def test_normalize_basic():
    df = Ingestor().normalize([{"ts":"2025-01-01T00:00:00Z","service":"svc","msg":"hello"}])
    assert len(df)==1 and df.iloc[0].service=="svc"
