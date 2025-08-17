import requests
from app.settings import settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class OllamaExplainer:
    def __init__(self):
        self.url = OPENROUTER_URL
        self.headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "LogOps RCA Assistant"
        }

    def explain(self, event_text: str) -> str:
        payload = {
            "model": "anthropic/claude-3-sonnet",
            "messages": [
                {"role": "system", "content": "You are a DevOps RCA assistant."},
                {"role": "user", "content": event_text}
            ]
        }
        resp = requests.post(self.url, headers=self.headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except KeyError:
            raise RuntimeError(f"Unexpected response format: {data}")
