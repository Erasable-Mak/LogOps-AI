import requests

BASE = "http://127.0.0.1:8000"

# 1. Health check
print("Health:", requests.get(f"{BASE}/health").json())

# 2. Ingest logs
logs = [{"timestamp":"2025-08-17T12:00:00Z","service":"api","message":"Error connecting to DB"}]
print("Ingest:", requests.post(f"{BASE}/ingest", json=logs).json())

# 3. Train model
print("Train:", requests.post(f"{BASE}/train/iforest").json())

# 4. Detect anomalies
test_logs = [{"timestamp":"2025-08-17T12:05:00Z","service":"api","message":"Timeout in DB query"}]
print("Detect:", requests.post(f"{BASE}/detect", json=test_logs).json())

# 5. RCA explain
print("Explain:", requests.post(f"{BASE}/explain/1").json())
