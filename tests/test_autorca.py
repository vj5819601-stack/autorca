from src.log_parser import parse_log
from src.root_cause_engine import analyze_root_cause


def test_database_error_classification():
    log = (
        "2026-08-26 10:31:22 ERROR "
        "PaymentService Database connection timeout"
    )

    result = parse_log(log)

    assert result["category"] == "DATABASE"


def test_network_error_classification():
    log = (
        "2026-08-26 10:32:10 ERROR "
        "APIGateway Connection refused"
    )

    result = parse_log(log)

    assert result["category"] == "NETWORK"


def test_memory_error_classification():
    log = (
        "2026-08-26 10:33:10 ERROR "
        "UserService Out of memory"
    )

    result = parse_log(log)

    assert result["category"] == "MEMORY"


def test_root_cause_ranking():
    causes = analyze_root_cause("DATABASE")

    assert len(causes) > 0
    assert causes[0]["score"] >= causes[-1]["score"]