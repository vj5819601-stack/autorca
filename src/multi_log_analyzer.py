from collections import Counter

from src.log_parser import parse_log


def analyze_multiple_logs(log_lines: list) -> dict:
    """
    Analyze multiple logs and identify the most common
    error category and affected services.
    """

    parsed_logs = [parse_log(log) for log in log_lines]

    categories = [
        log["category"]
        for log in parsed_logs
        if log["category"] != "UNKNOWN"
    ]

    services = [
        log["service"]
        for log in parsed_logs
        if log["service"]
    ]

    category_counts = Counter(categories)
    service_counts = Counter(services)

    most_common_category = (
        category_counts.most_common(1)[0][0]
        if category_counts
        else "UNKNOWN"
    )

    return {
        "total_logs": len(parsed_logs),
        "category_counts": dict(category_counts),
        "service_counts": dict(service_counts),
        "most_common_category": most_common_category,
    }