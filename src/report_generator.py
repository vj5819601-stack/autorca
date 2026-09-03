import json
from pathlib import Path
from src.xai_explainer import explain_incident

def save_incident_report(result: dict, path="reports/incident_report.json"):
    output = dict(result)
    output["explanation"] = explain_incident(result)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, indent=2, default=str), encoding="utf-8")
    return target
