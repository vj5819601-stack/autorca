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
def identify_affected_services(log_lines: list) -> list:
    """
    Identify services that appear most frequently
    in the provided logs.
    """

    parsed_logs = [parse_log(log) for log in log_lines]

    service_counts = Counter(
        log["service"]
        for log in parsed_logs
        if log["service"]
    )

    return [
        {
            "service": service,
            "error_count": count
        }
        for service, count in service_counts.most_common()
    ]
def generate_incident_summary(log_lines: list) -> dict:
    """
    Generate a high-level incident summary from multiple logs.
    """

    analysis = analyze_multiple_logs(log_lines)
    affected_services = identify_affected_services(log_lines)

    return {
        "total_logs": analysis["total_logs"],
        "most_common_category": analysis["most_common_category"],
        "category_counts": analysis["category_counts"],
        "most_affected_service": (
            affected_services[0]["service"]
            if affected_services
            else "UNKNOWN"
        ),
        "service_error_count": (
            affected_services[0]["error_count"]
            if affected_services
            else 0
        ),
    }
def identify_likely_root_cause(log_lines: list) -> dict:
    """
    Identify the most likely root cause from multiple logs
    using the dominant error category.
    """

    analysis = analyze_multiple_logs(log_lines)

    category = analysis["most_common_category"]

    category_counts = analysis["category_counts"]

    if category == "UNKNOWN":
        return {
            "root_cause": "Unknown",
            "reason": "No recognized error pattern was found."
        }

    root_cause_map = {
        "DATABASE": "Database-related failure",
        "NETWORK": "Network or downstream service failure",
        "MEMORY": "Memory exhaustion or resource pressure",
        "AUTHENTICATION": "Authentication or authorization failure",
    }

    root_cause = root_cause_map.get(
        category,
        "Unknown root cause"
    )

    return {
        "root_cause": root_cause,
        "category": category,
        "category_count": category_counts.get(category, 0),
        "reason": (
            f"The {category} category appears most frequently "
            f"in the analyzed logs."
        )
    }