from collections import Counter
from datetime import datetime

from src.dependency_graph import build_service_graph, dependency_scores, service_impact
from src.ml_anomaly_detector import LogAnomalyDetector
from src.root_cause_engine import analyze_root_cause

def _temporal_burst(parsed_logs):
    times = []
    for log in parsed_logs:
        try:
            times.append(datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S"))
        except (TypeError, ValueError):
            pass
    if len(times) < 2:
        return 0.0
    span = (max(times) - min(times)).total_seconds()
    return 1.0 if span <= 120 else 0.5 if span <= 600 else 0.2

def analyze_incident(log_lines):
    parsed = []
    for line in log_lines:
        from src.log_parser import parse_log
        parsed.append(parse_log(line))

    messages = [x["message"] for x in parsed]
    detector = LogAnomalyDetector()
    anomalies = detector.score_messages(messages)

    for log, anomaly in zip(parsed, anomalies):
        log["anomaly_score"] = anomaly.score
        log["is_anomaly"] = anomaly.is_anomaly
        log["top_anomaly_terms"] = anomaly.top_terms

    category_counts = Counter(x["category"] for x in parsed if x["category"] != "UNKNOWN")
    service_counts = service_impact(parsed)
    dominant_category = category_counts.most_common(1)[0][0] if category_counts else "UNKNOWN"
    graph = build_service_graph(parsed)
    dep_scores = dependency_scores(graph)
    burst = _temporal_burst(parsed)

    candidates = Counter()
    evidence = []
    for log in parsed:
        if log["category"] != dominant_category:
            continue
        for cause in analyze_root_cause(log["category"], log["message"]):
            signal = (
                cause["score"] * 0.50
                + log["anomaly_score"] * 0.15
                + (category_counts[dominant_category] / max(len(parsed), 1)) * 0.20
                + burst * 0.10
                + dep_scores.get(log["service"], 0.0) * 0.05
            )
            candidates[cause["cause"]] += signal
            if cause["matched_keywords"]:
                evidence.append({
                    "service": log["service"],
                    "cause": cause["cause"],
                    "keywords": cause["matched_keywords"],
                    "anomaly_score": round(log["anomaly_score"], 3),
                })

    ranked = candidates.most_common()
    likely = ranked[0][0] if ranked else "Unknown"
    most_affected = max(service_counts, key=service_counts.get) if service_counts else "UNKNOWN"

    return {
        "total_logs": len(parsed),
        "logs": parsed,
        "category_counts": dict(category_counts),
        "service_counts": dict(service_counts),
        "dominant_category": dominant_category,
        "most_affected_service": most_affected,
        "dependency_scores": dep_scores,
        "temporal_burst_score": round(burst, 3),
        "likely_root_cause": likely,
        "root_cause_candidates": [
            {"cause": cause, "score": round(score, 4)}
            for cause, score in ranked
        ],
        "supporting_evidence": evidence[:10],
    }
