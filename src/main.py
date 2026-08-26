from log_parser import parse_log
from root_cause_engine import analyze_root_cause


def analyze_log(log_line: str) -> dict:
    """
    Run the complete AutoRCA analysis pipeline.
    """

    parsed = parse_log(log_line)

    category = parsed["category"]

    root_causes = analyze_root_cause(category)

    return {
        "log": parsed,
        "root_causes": root_causes,
    }


def display_report(result: dict) -> None:
    """Display the AutoRCA diagnosis."""

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


if __name__ == "__main__":

    sample_log = (
        "2026-08-26 10:31:22 ERROR "
        "PaymentService Database connection timeout"
    )

    result = analyze_log(sample_log)

    display_report(result)