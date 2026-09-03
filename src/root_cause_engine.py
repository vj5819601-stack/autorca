ROOT_CAUSES = {
    "DATABASE": [
        {
            "cause": "Database unavailable",
            "score": 0.85,
            "keywords": ["database unavailable", "connection timeout"],
            "evidence": "Database connection failure or timeout detected"
        },
        {
            "cause": "Connection pool exhausted",
            "score": 0.70,
            "keywords": ["connection pool", "repeated database connection"],
            "evidence": "Repeated database connection failures detected"
        },
        {
            "cause": "SQL or query error",
            "score": 0.75,
            "keywords": ["sql error", "query error"],
            "evidence": "SQL or database query error detected"
        },
        {
            "cause": "Network latency affecting database",
            "score": 0.45,
            "keywords": ["timeout to database"],
            "evidence": "Database request exceeded expected timeout"
        }
    ],

    "NETWORK": [
        {
            "cause": "Downstream service unavailable",
            "score": 0.85,
            "keywords": ["connection refused", "downstream service"],
            "evidence": "Connection refused or downstream service failure detected"
        },
        {
            "cause": "Network instability",
            "score": 0.65,
            "keywords": ["connection reset", "network error"],
            "evidence": "Connection reset or network error detected"
        },
        {
            "cause": "DNS resolution failure",
            "score": 0.90,
            "keywords": ["dns failure", "dns"],
            "evidence": "DNS resolution failure detected"
        }
    ],

    "MEMORY": [
        {
            "cause": "Memory exhaustion",
            "score": 0.90,
            "keywords": ["out of memory", "memory limit"],
            "evidence": "Out of memory or memory limit condition detected"
        },
        {
            "cause": "Memory leak",
            "score": 0.70,
            "keywords": ["memory leak"],
            "evidence": "Possible memory leak detected"
        },
        {
            "cause": "Heap exhaustion",
            "score": 0.90,
            "keywords": ["heap exhausted"],
            "evidence": "Heap exhaustion detected during request processing"
        }
    ],

    "AUTHENTICATION": [
        {
            "cause": "Invalid credentials",
            "score": 0.85,
            "keywords": ["authentication failed", "invalid credentials"],
            "evidence": "Authentication failure detected"
        },
        {
            "cause": "Invalid or expired token",
            "score": 0.90,
            "keywords": ["invalid token", "expired token"],
            "evidence": "Token validation failure detected"
        },
        {
            "cause": "Unauthorized access attempt",
            "score": 0.90,
            "keywords": ["unauthorized", "access denied"],
            "evidence": "Unauthorized or denied access detected"
        }
    ]
}


def analyze_root_cause(category: str, message: str = "") -> list:
    """
    Analyze possible root causes using both error category
    and keywords found in the log message.
    """

    causes = ROOT_CAUSES.get(category, [])
    message_lower = message.lower()

    ranked_causes = []

    for cause in causes:
        score = cause["score"]
        matched_keywords = []

        for keyword in cause["keywords"]:
            if keyword in message_lower:
                matched_keywords.append(keyword)

        if matched_keywords:
            score = min(score + 0.10, 0.99)

        ranked_causes.append(
            {
                "cause": cause["cause"],
                "score": score,
                "evidence": cause["evidence"],
                "matched_keywords": matched_keywords
            }
        )

    return sorted(
        ranked_causes,
        key=lambda item: item["score"],
        reverse=True
    )


if __name__ == "__main__":
    category = "DATABASE"
    message = "Database connection timeout"

    results = analyze_root_cause(category, message)

    print("\nAutoRCA Root Cause Analysis")
    print("---------------------------")

    for index, result in enumerate(results, start=1):
        print(
            f"{index}. {result['cause']} "
            f"| Score: {result['score']:.2f}"
        )
        print(f"   Evidence: {result['evidence']}")

        if result["matched_keywords"]:
            print(
                f"   Matched Keywords: "
                f"{', '.join(result['matched_keywords'])}"
            )