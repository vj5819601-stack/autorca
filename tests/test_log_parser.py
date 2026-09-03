from src.log_parser import classify_error, parse_log

def test_parse_fields():
    r = parse_log("2026-08-26 10:31:22 ERROR PaymentService Database connection timeout")
    assert r["service"] == "PaymentService"
    assert r["category"] == "DATABASE"

def test_case_insensitive():
    assert classify_error("OUT OF MEMORY") == "MEMORY"

def test_unknown():
    assert classify_error("something unexpected happened") == "UNKNOWN"
