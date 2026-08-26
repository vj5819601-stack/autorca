import re


ERROR_PATTERNS = {
    "DATABASE": [
        "database connection",
        "connection timeout",
        "sql error",
        "database unavailable",
    ],
    "NETWORK": [
        "connection refused",
        "network error",
        "dns failure",
        "connection reset",
    ],
    "MEMORY": [
        "out of memory",
        "memory limit",
        "heap exhausted",
    ],
    "AUTHENTICATION": [
        "authentication failed",
        "unauthorized",
        "invalid token",
        "access denied",
    ],
}


def classify_error(message: str) -> str:
    """Classify a production error into a high-level category."""

    message_lower = message.lower()

    for category, patterns in ERROR_PATTERNS.items():
        for pattern in patterns:
            if pattern in message_lower:
                return category

    return "UNKNOWN"


def parse_log(log_line: str) -> dict:
    """Parse a production log line."""

    pattern = (
        r"(?P<timestamp>\S+\s+\S+)\s+"
        r"(?P<level>\w+)\s+"
        r"(?P<service>\S+)\s+"
        r"(?P<message>.+)"
    )

    match = re.match(pattern, log_line)

    if not match:
        return {
            "timestamp": None,
            "level": None,
            "service": None,
            "message": log_line,
            "category": classify_error(log_line),
        }

    data = match.groupdict()

    return {
        "timestamp": data["timestamp"],
        "level": data["level"],
        "service": data["service"],
        "message": data["message"],
        "category": classify_error(data["message"]),
    }


if __name__ == "__main__":

    sample_log = (
        "2026-08-26 10:31:22 ERROR "
        "PaymentService Database connection timeout"
    )

    result = parse_log(sample_log)

    print("\nAutoRCA Log Analysis")
    print("--------------------")

    for key, value in result.items():
        print(f"{key}: {value}")