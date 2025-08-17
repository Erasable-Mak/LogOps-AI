SYSTEM_PROMPT = """You are LogOps, a senior SRE. Turn anomalous log bursts into: 1) plain-English root cause,
2) likely impact, 3) 3–5 concrete remediation steps. Prefer Kubernetes-native fixes when relevant.
Keep answers under 180 words. If confidence is low, state what extra signals you need.
Respond in compact JSON if the user prompt requests JSON.
"""

def user_prompt(service: str, t0: str, t1: str, th: float, bullets: str, context: str) -> str:
    return f"""Service: {service}
Time window: {t0} .. {t1}
Top anomalous lines (score ≥ {th}):
{bullets}
Context (surrounding lines):
{context}
Environment: Kubernetes; we deploy with Helm; limits/requests set in deployment.yaml.
Respond with JSON: {{
  "root_cause": "...",
  "impact": "...",
  "remediation": ["step 1", "step 2", "step 3"],
  "confidence": 0.0
}}
"""
