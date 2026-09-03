from src.log_parser import parse_log
from src.root_cause_engine import analyze_root_cause
from src.multi_log_analyzer import (
    analyze_multiple_logs,
    identify_affected_services,
    identify_likely_root_cause,
    generate_incident_summary,
)


def test_database_error_classification():
    result = parse_log(
        "2026-08-26 10:31:22 ERROR "
        "PaymentService Database connection timeout"
    )
    assert result["category"] == "DATABASE"


def test_network_error_classification():
    result = parse_log(
        "2026-08-26 10:32:10 ERROR "
        "APIGateway Connection refused"
    )
    assert result["category"] == "NETWORK"


def test_memory_error_classification():
    result = parse_log(
        "2026-08-26 10:33:10 ERROR "
        "UserService Out of memory"
    )
    assert result["category"] == "MEMORY"


def test_unknown_error_classification():
    result = parse_log(
        "2026-08-26 10:34:10 ERROR "
        "SearchService Unexpected failure"
    )
    assert result["category"] == "UNKNOWN"


def test_root_cause_ranking():
    causes = analyze_root_cause(
        "DATABASE",
        "Database connection timeout",
    )
    assert len(causes) > 0
    assert causes[0]["score"] >= causes[-1]["score"]
    assert "connection timeout" in causes[0]["matched_keywords"]


def sample_logs():
    return [
        "2026-08-26 10:31:22 ERROR PaymentService Database connection timeout",
        "2026-08-26 10:32:10 ERROR APIGateway Connection refused by downstream service",
        "2026-08-26 10:35:42 ERROR PaymentService SQL error while executing transaction",
    ]


def test_multi_log_analysis():
    result = analyze_multiple_logs(sample_logs())
    assert result["total_logs"] == 3
    assert result["most_common_category"] == "DATABASE"
    assert result["category_counts"]["DATABASE"] == 2


def test_affected_services():
    result = identify_affected_services(sample_logs())
    assert result[0]["service"] == "PaymentService"
    assert result[0]["error_count"] == 2


def test_likely_root_cause():
    result = identify_likely_root_cause(sample_logs())
    assert result["category"] == "DATABASE"
    assert result["root_cause"] in {
        "Database unavailable",
        "SQL or query error",
        "Connection pool exhausted",
        "Network latency affecting database",
    }


def test_incident_summary():
    result = generate_incident_summary(sample_logs())
    assert result["most_common_category"] == "DATABASE"
    assert result["most_affected_service"] == "PaymentService"
    assert result["service_error_count"] == 2
    assert result["likely_root_cause"] != "Unknown"
