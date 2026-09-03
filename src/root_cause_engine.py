ROOT_CAUSES = {
    "DATABASE": [
        {
            "cause": "Database unavailable",
            "score": 0.85,
            "keywords": ["database unavailable", "connection timeout"],
            "evidence": "Database connection failure or timeout detected.",
        },
        {
            "cause": "SQL or query error",
            "score": 0.75,
            "keywords": ["sql error", "query error"],
            "evidence": "SQL or database query error detected.",
        },
        {
            "cause": "Connection pool exhausted",
            "score": 0.70,
            "keywords": ["connection pool", "repeated database connection"],
            "evidence": "Repeated database connection failures detected.",
        },
        {
            "cause": "Network latency affecting database",
            "score": 0.45,
            "keywords": ["timeout to database"],
            "evidence": "Database request exceeded the expected timeout.",
        },
    ],
    "NETWORK": [
        {
            "cause": "DNS resolution failure",
            "score": 0.90,
            "keywords": ["dns failure", "dns"],
            "evidence": "DNS resolution failure detected.",
        },
        {
            "cause": "Downstream service unavailable",
            "score": 0.85,
            "keywords": ["connection refused", "downstream service"],
            "evidence": "Connection refused or downstream service failure detected.",
        },
        {
            "cause": "Network instability",
            "score": 0.65,
            "keywords": ["connection reset", "network error"],
            "evidence": "Connection reset or network error detected.",
        },
    ],
    "MEMORY": [
        {
            "cause": "Memory exhaustion",
            "score": 0.90,
            "keywords": ["out of memory", "memory limit"],
            "evidence": "Out-of-memory or memory-limit condition detected.",
        },
        {
            "cause": "Heap exhaustion",
            "score": 0.90,
            "keywords": ["heap exhausted"],
            "evidence": "Heap exhaustion detected during request processing.",
        },
        {
            "cause": "Memory leak",
            "score": 0.70,
            "keywords": ["memory leak"],
            "evidence": "Possible memory leak detected.",
        },
    ],
    "AUTHENTICATION": [
        {
            "cause": "Invalid or expired token",
            "score": 0.90,
            "keywords": ["invalid token", "expired token"],
            "evidence": "Token validation failure detected.",
        },
        {
            "cause": "Unauthorized access attempt",
            "score": 0.90,
            "keywords": ["unauthorized", "access denied"],
            "evidence": "Unauthorized or denied access detected.",
        },
        {
            "cause": "Invalid credentials",
            "score": 0.85,
            "keywords": ["authentication failed", "invalid credentials"],
            "evidence": "Authentication failure detected.",
        },
    ],
}


def analyze_root_cause(category: str, message: str = "") -> list:
    """Rank possible root causes for a single log message.

    The score is a rule-based ranking score, not a calibrated probability.
    """
    causes = ROOT_CAUSES.get(category, [])
    message_lower = message.lower()
    ranked_causes = []

    for cause in causes:
        matched_keywords = [
            keyword
            for keyword in cause["keywords"]
            if keyword in message_lower
        ]

        score = cause["score"]
        if matched_keywords:
            score = min(score + 0.10, 0.99)

        if matched_keywords:
            explanation = (
                f"The log contains '{matched_keywords[0]}', "
                f"which supports the root cause '{cause['cause']}'."
            )
        else:
            explanation = (
                f"The error category '{category}' is associated "
                f"with this possible root cause."
            )

        ranked_causes.append(
            {
                "cause": cause["cause"],
                "score": score,
                "evidence": cause["evidence"],
                "matched_keywords": matched_keywords,
                "explanation": explanation,
            }
        )

    return sorted(
        ranked_causes,
        key=lambda item: item["score"],
        reverse=True,
    )
