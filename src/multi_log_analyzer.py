from collections import Counter

from src.log_parser import parse_log
from src.root_cause_engine import analyze_root_cause


def _parse_logs(log_lines: list) -> list:
    return [parse_log(log) for log in log_lines]


def analyze_multiple_logs(log_lines: list) -> dict:
    """Analyze categories and services across multiple logs."""
    parsed_logs = _parse_logs(log_lines)

    category_counts = Counter(
        log["category"]
        for log in parsed_logs
        if log["category"] != "UNKNOWN"
    )

    service_counts = Counter(
        log["service"]
        for log in parsed_logs
        if log["service"]
    )

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
    """Rank services by number of observed errors."""
    parsed_logs = _parse_logs(log_lines)

    service_counts = Counter(
        log["service"]
        for log in parsed_logs
        if log["service"]
    )

    return [
        {"service": service, "error_count": count}
        for service, count in service_counts.most_common()
    ]


def correlate_evidence(log_lines: list) -> list:
    """Find repeated RCA keywords across an incident."""
    parsed_logs = _parse_logs(log_lines)
    evidence_counts = Counter()

    for log in parsed_logs:
        category = log["category"]
        message = log["message"]

        for cause in analyze_root_cause(category, message):
            for keyword in cause["matched_keywords"]:
                evidence_counts[keyword] += 1

    return [
        {"evidence": evidence, "count": count}
        for evidence, count in evidence_counts.most_common()
    ]


def identify_likely_root_cause(log_lines: list) -> dict:
    """Identify the dominant incident-level root cause."""
    analysis = analyze_multiple_logs(log_lines)
    category = analysis["most_common_category"]

    if category == "UNKNOWN":
        return {
            "root_cause": "Unknown",
            "category": "UNKNOWN",
            "category_count": 0,
            "reason": "No recognized error pattern was found.",
        }

    parsed_logs = _parse_logs(log_lines)
    candidate_scores = Counter()

    for log in parsed_logs:
        if log["category"] == category:
            for cause in analyze_root_cause(category, log["message"]):
                candidate_scores[cause["cause"]] += cause["score"]

    ranked = candidate_scores.most_common()

    root_cause = ranked[0][0] if ranked else "Unknown"
    category_count = analysis["category_counts"].get(category, 0)

    evidence = correlate_evidence(log_lines)
    evidence_text = (
        evidence[0]["evidence"]
        if evidence
        else "No repeated keyword evidence found."
    )

    return {
        "root_cause": root_cause,
        "category": category,
        "category_count": category_count,
        "reason": (
            f"The {category} category appears most frequently "
            f"and the strongest matching RCA candidate is '{root_cause}'."
        ),
        "supporting_evidence": evidence_text,
    }


def generate_incident_summary(log_lines: list) -> dict:
    """Generate a complete incident-level RCA summary."""
    analysis = analyze_multiple_logs(log_lines)
    affected_services = identify_affected_services(log_lines)
    likely_root_cause = identify_likely_root_cause(log_lines)
    evidence = correlate_evidence(log_lines)

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
        "likely_root_cause": likely_root_cause["root_cause"],
        "root_cause_reason": likely_root_cause["reason"],
        "supporting_evidence": (
            evidence[:5]
        ),
    }
