ROOT_CAUSES = {
    "DATABASE": [
        ("Database unavailable", 0.85, ["database unavailable", "connection timeout", "database connection"]),
        ("SQL or query error", 0.75, ["sql error", "query error", "deadlock"]),
        ("Connection pool exhausted", 0.70, ["connection pool", "repeated database connection"]),
        ("Database latency", 0.50, ["timeout to database", "slow query"]),
    ],
    "NETWORK": [
        ("DNS resolution failure", 0.90, ["dns failure", "dns"]),
        ("Downstream service unavailable", 0.85, ["connection refused", "downstream service", "503"]),
        ("Network instability", 0.65, ["connection reset", "network error", "packet loss"]),
        ("Gateway timeout", 0.75, ["gateway timeout", "502", "504"]),
    ],
    "MEMORY": [
        ("Memory exhaustion", 0.90, ["out of memory", "memory limit", "oom"]),
        ("Heap exhaustion", 0.90, ["heap exhausted"]),
        ("Memory leak", 0.70, ["memory leak"]),
        ("GC pressure", 0.65, ["gc overhead"]),
    ],
    "AUTHENTICATION": [
        ("Invalid or expired token", 0.90, ["invalid token", "expired token"]),
        ("Unauthorized access attempt", 0.90, ["unauthorized", "access denied"]),
        ("Invalid credentials", 0.85, ["authentication failed", "invalid credentials"]),
    ],
}

def analyze_root_cause(category: str, message: str = "") -> list:
    text = message.lower()
    results = []
    for cause, base_score, keywords in ROOT_CAUSES.get(category, []):
        matches = [k for k in keywords if k in text]
        score = min(base_score + (0.10 if matches else 0), 0.99)
        results.append({
            "cause": cause,
            "score": score,
            "matched_keywords": matches,
            "evidence": f"Matched evidence: {', '.join(matches)}" if matches else f"Category signal: {category}",
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)
