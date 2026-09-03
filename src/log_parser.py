import re

ERROR_PATTERNS = {
    "DATABASE": [
        "database connection", "connection timeout", "sql error",
        "database unavailable", "connection pool", "query error",
        "timeout to database", "deadlock", "postgres", "mysql","slow query",
    ],
    "NETWORK": [
        "connection refused", "network error", "dns failure",
        "connection reset", "downstream service", "dns", "packet loss",
        "gateway timeout", "502", "503",
    ],
    "MEMORY": [
        "out of memory", "memory limit", "heap exhausted",
        "memory leak", "oom", "gc overhead",
    ],
    "AUTHENTICATION": [
        "authentication failed", "unauthorized", "invalid token",
        "access denied", "invalid credentials", "expired token",
    ],
}

def classify_error(message: str) -> str:
    text = message.lower()
    for category, patterns in ERROR_PATTERNS.items():
        if any(pattern in text for pattern in patterns):
            return category
    return "UNKNOWN"

def parse_log(log_line: str) -> dict:
    pattern = (
        r"(?P<timestamp>\S+\s+\S+)\s+"
        r"(?P<level>\w+)\s+"
        r"(?P<service>\S+)\s+"
        r"(?P<message>.+)"
    )
    match = re.match(pattern, log_line.strip())
    if not match:
        return {
            "timestamp": None, "level": None, "service": None,
            "message": log_line, "category": classify_error(log_line)
        }
    data = match.groupdict()
    return {
        "timestamp": data["timestamp"],
        "level": data["level"],
        "service": data["service"],
        "message": data["message"],
        "category": classify_error(data["message"]),
    }
