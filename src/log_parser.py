import re

ERROR_PATTERNS = {
    "DATABASE": [
        "database connection",
        "connection timeout",
        "sql error",
        "database unavailable",
        "connection pool",
        "query error",
        "timeout to database",
    ],
    "NETWORK": [
        "connection refused",
        "network error",
        "dns failure",
        "connection reset",
        "downstream service",
        "dns",
    ],
    "MEMORY": [
        "out of memory",
        "memory limit",
        "heap exhausted",
        "memory leak",
    ],
    "AUTHENTICATION": [
        "authentication failed",
        "unauthorized",
        "invalid token",
        "access denied",
        "invalid credentials",
        "expired token",
    ],
}


def classify_error(message: str) -> str:
    """Classify a log message into a high-level error category."""
    message_lower = message.lower()

    for category, patterns in ERROR_PATTERNS.items():
        for pattern in patterns:
            if pattern in message_lower:
                return category

    return "UNKNOWN"


def parse_log(log_line: str) -> dict:
    """Parse a log line into timestamp, level, service, message and category."""
    pattern = (
        r"(?P<timestamp>\S+\s+\S+)\s+"
        r"(?P<level>\w+)\s+"
        r"(?P<service>\S+)\s+"
        r"(?P<message>.+)"
    )

    match = re.match(pattern, log_line.strip())

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
