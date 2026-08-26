ROOT_CAUSES = {
    "DATABASE": [
        {
            "cause": "Database unavailable",
            "score": 0.85,
            "evidence": "Connection timeout detected"
        },
        {
            "cause": "Connection pool exhausted",
            "score": 0.70,
            "evidence": "Repeated database connection failures"
        },
        {
            "cause": "Network latency",
            "score": 0.45,
            "evidence": "Database request exceeded timeout"
        }
    ],
    "NETWORK": [
        {
            "cause": "Downstream service unavailable",
            "score": 0.85,
            "evidence": "Connection refused"
        },
        {
            "cause": "Network instability",
            "score": 0.65,
            "evidence": "Connection reset detected"
        }
    ],
    "MEMORY": [
        {
            "cause": "Memory exhaustion",
            "score": 0.90,
            "evidence": "Out of memory condition detected"
        },
        {
            "cause": "Memory leak",
            "score": 0.70,
            "evidence": "Repeated memory limit violations"
        }
    ],
}


def analyze_root_cause(category: str) -> list:
    """
    Return ranked possible root causes for an error category.
    """

    causes = ROOT_CAUSES.get(category, [])

    return sorted(
        causes,
        key=lambda item: item["score"],
        reverse=True
    )


if __name__ == "__main__":

    category = "DATABASE"

    results = analyze_root_cause(category)

    print("\nAutoRCA Root Cause Analysis")
    print("---------------------------")

    for index, result in enumerate(results, start=1):
        print(
            f"{index}. {result['cause']} "
            f"| Score: {result['score']:.2f}"
        )

        print(f"   Evidence: {result['evidence']}")