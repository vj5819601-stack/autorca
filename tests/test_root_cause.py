from src.root_cause_engine import analyze_root_cause

def test_database_ranking():
    r = analyze_root_cause("DATABASE", "Database connection timeout")
    assert r[0]["cause"] == "Database unavailable"
    assert "connection timeout" in r[0]["matched_keywords"]

def test_network_ranking():
    r = analyze_root_cause("NETWORK", "Connection refused by downstream service")
    assert r[0]["cause"] == "Downstream service unavailable"
