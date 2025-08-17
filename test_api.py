import requests
import json

# Test health endpoint
response = requests.get("http://127.0.0.1:8000/health")
print("Health:", response.json())

# Test ingest endpoint
test_logs = [{"ts":"2025-01-01T00:00:00Z","service":"test","msg":"test log message"}]
response = requests.post("http://127.0.0.1:8000/ingest", json=test_logs)
print("Status Code:", response.status_code)
if response.status_code == 200:
    print("Ingest:", response.json())
else:
    print("Error:", response.text) 