import csv
from pathlib import Path

try:
    from src.log_parser import parse_log
    from src.root_cause_engine import analyze_root_cause
    from src.multi_log_analyzer import generate_incident_summary
except ModuleNotFoundError:
    from log_parser import parse_log
    from root_cause_engine import analyze_root_cause
    from multi_log_analyzer import generate_incident_summary


def analyze_log(log_line: str) -> dict:
    """Analyze one log and return structured RCA results."""
    parsed = parse_log(log_line)
    root_causes = analyze_root_cause(
        parsed["category"],
        parsed["message"],
    )

    return {
        "log": parsed,
        "root_causes": root_causes,
    }


def load_logs_from_csv(file_path: str) -> list:
    """Load logs from the sample CSV dataset."""
    logs = []

    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            logs.append(
                f"{row['timestamp']} "
                f"{row['level']} "
                f"{row['service']} "
                f"{row['message']}"
            )

    return logs


def display_report(result: dict) -> None:
    """Print the RCA report for a single log."""
    log = result["log"]

    print("\n==============================")
    print("        AutoRCA Report")
    print("==============================")
    print(f"Service  : {log['service']}")
    print(f"Level    : {log['level']}")
    print(f"Message  : {log['message']}")
    print(f"Category : {log['category']}")

    print("\nPossible Root Causes")
    print("--------------------")

    if not result["root_causes"]:
        print("No known root cause found.")
        return

    for index, cause in enumerate(result["root_causes"], start=1):
        print(
            f"{index}. {cause['cause']} "
            f"| Ranking Score: {cause['score']:.2f}"
        )
        print(f"   Evidence: {cause['evidence']}")

        if cause["matched_keywords"]:
            print(
                "   Matched Keywords: "
                + ", ".join(cause["matched_keywords"])
            )

        print(f"   Why: {cause['explanation']}")


def display_incident_summary(summary: dict) -> None:
    """Print the incident-level RCA summary."""
    print("\n================================")
    print("      AutoRCA Incident Summary")
    print("================================")
    print(f"Total Logs           : {summary['total_logs']}")
    print(f"Dominant Category    : {summary['most_common_category']}")
    print(f"Most Affected Service: {summary['most_affected_service']}")
    print(f"Service Error Count  : {summary['service_error_count']}")
    print(f"Likely Root Cause    : {summary['likely_root_cause']}")
    print(f"Reason               : {summary['root_cause_reason']}")

    print("\nSupporting Evidence")
    print("-------------------")

    if not summary["supporting_evidence"]:
        print("No repeated evidence found.")
        return

    for item in summary["supporting_evidence"]:
        print(f"- {item['evidence']} ({item['count']} occurrence(s))")


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    csv_file = project_root / "data" / "sample_logs.csv"

    logs = load_logs_from_csv(csv_file)

    print(f"\nLoaded {len(logs)} logs from dataset.")

    for log in logs:
        display_report(analyze_log(log))

    display_incident_summary(generate_incident_summary(logs))


if __name__ == "__main__":
    main()
