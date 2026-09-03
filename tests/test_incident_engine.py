from src.incident_engine import analyze_incident

def sample():
    return [
        "2026-08-26 10:31:22 ERROR PaymentService Database connection timeout",
        "2026-08-26 10:31:40 ERROR PaymentService Database unavailable",
        "2026-08-26 10:32:10 ERROR APIGateway Connection refused by downstream service",
        "2026-08-26 10:32:30 ERROR UserService Out of memory while processing request",
    ]

def test_incident_summary():
    r = analyze_incident(sample())
    assert r["total_logs"] == 4
    assert r["dominant_category"] == "DATABASE"
    assert r["most_affected_service"] == "PaymentService"
    assert r["likely_root_cause"] != "Unknown"

def test_anomaly_fields():
    r = analyze_incident(sample())
    assert all("anomaly_score" in x for x in r["logs"])
    assert all(0 <= x["anomaly_score"] <= 1 for x in r["logs"])
