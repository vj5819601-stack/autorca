from src.log_parser import classify_error, parse_log


def test_parse_log_fields():
    result = parse_log(
        "2026-08-26 10:31:22 ERROR PaymentService Database connection timeout"
    )

    assert result["timestamp"] == "2026-08-26 10:31:22"
    assert result["level"] == "ERROR"
    assert result["service"] == "PaymentService"
    assert result["message"] == "Database connection timeout"


def test_case_insensitive_classification():
    assert classify_error("OUT OF MEMORY while processing") == "MEMORY"
