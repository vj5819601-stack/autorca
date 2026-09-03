import csv
from pathlib import Path

from src.incident_engine import analyze_incident
from src.report_generator import save_incident_report
from src.root_cause_engine import analyze_root_cause

def load_logs_from_csv(file_path):
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [
            f"{r['timestamp']} {r['level']} {r['service']} {r['message']}"
            for r in reader
        ]

def main():
    root = Path(__file__).resolve().parent.parent
    logs = load_logs_from_csv(root / "data" / "sample_logs.csv")
    result = analyze_incident(logs)

    print("\n======================================")
    print("        AutoRCA PRO MAX REPORT")
    print("======================================")
    print(f"Total Logs            : {result['total_logs']}")
    print(f"Dominant Category     : {result['dominant_category']}")
    print(f"Most Affected Service : {result['most_affected_service']}")
    print(f"Likely Root Cause     : {result['likely_root_cause']}")
    print(f"Temporal Burst Score  : {result['temporal_burst_score']}")
    print("\nRoot Cause Candidates")
    for item in result["root_cause_candidates"][:5]:
        print(f"- {item['cause']}: {item['score']}")
    print("\nExplainable Evidence")
    for item in result["supporting_evidence"][:5]:
        print(f"- {item['service']}: {', '.join(item['keywords'])}")
    path = save_incident_report(result, root / "reports" / "incident_report.json")
    print(f"\nJSON report saved to: {path}")

if __name__ == "__main__":
    main()
