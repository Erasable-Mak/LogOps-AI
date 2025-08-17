import pandas as pd

NORMALIZE_FIELDS = ["ts","service","level","msg","host","source","pod","trace_id"]

class Ingestor:
    def normalize(self, records: list[dict]) -> pd.DataFrame:
        rows = []
        for r in records:
            row = {k: r.get(k) for k in NORMALIZE_FIELDS}
            rows.append(row)
        df = pd.DataFrame(rows, columns=NORMALIZE_FIELDS)
        # cast ts to datetime for duckdb
        if not df.empty:
            df["ts"] = pd.to_datetime(df["ts"], errors="coerce")
        return df

def read_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            import json
            yield json.loads(line)
