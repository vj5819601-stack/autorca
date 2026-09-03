import csv

from log_parser import parse_log
from root_cause_engine import analyze_root_cause


def analyze_log(log_line: str) -> dict:
    parsed = parse_log(log_line)

    category = parsed["category"]
    message = parsed["message"]

    root_causes = analyze_root_cause(category, message)

    return {
        "log": parsed,
        "root_causes": root_causes,
    }


def display_report(result: dict) -> None:
    log = result["log"]
    root_causes = result["root_causes"]

    print("\n==============================")
    print("        AutoRCA Report")
    print("==============================")

    print(f"Service  : {log['service']}")
    print(f"Level    : {log['level']}")
    print(f"Message  : {log['message']}")
    print(f"Category : {log['category']}")

    print("\nPossible Root Causes")
    print("--------------------")

    if not root_causes:
        print("No known root cause found.")
        return

    for index, cause in enumerate(root_causes, start=1):
        print(
            f"{index}. {cause['cause']} "
            f"| Score: {cause['score']:.2f}"
        )

        print(f"   Evidence: {cause['evidence']}")

        if cause["matched_keywords"]:
            print(
                f"   Matched Keywords: "
                f"{', '.join(cause['matched_keywords'])}"
            )

        print(f"   Why: {cause['explanation']}")


def load_logs_from_csv(file_path: str) -> list:
    logs = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            log_line = (
                f"{row['timestamp']} "
                f"{row['level']} "
                f"{row['service']} "
                f"{row['message']}"
            )

            logs.append(log_line)

    return logs


if __name__ == "__main__":
    csv_file = "data/sample_logs.csv"

    logs = load_logs_from_csv(csv_file)

    print(f"\nLoaded {len(logs)} logs from dataset.")

    for log in logs:
        result = analyze_log(log)
        display_report(result)