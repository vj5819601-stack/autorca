def explain_incident(result: dict) -> list:
    """Convert model/rule signals into human-readable RCA evidence."""
    explanations = []
    category = result["dominant_category"]
    service = result["most_affected_service"]
    cause = result["likely_root_cause"]

    explanations.append(
        f"Dominant failure category is {category}, so RCA candidates were restricted to that failure family."
    )
    explanations.append(
        f"{service} has the highest observed error count and is therefore the most affected service."
    )
    explanations.append(
        f"The selected root cause '{cause}' has the strongest combined rule, anomaly, frequency, temporal and dependency score."
    )
    if result["temporal_burst_score"] >= 0.5:
        explanations.append(
            "Errors are temporally concentrated, supporting a common incident rather than unrelated isolated events."
        )
    for item in result["supporting_evidence"][:5]:
        explanations.append(
            f"{item['service']}: evidence {', '.join(item['keywords'])}; anomaly score {item['anomaly_score']}."
        )
    return explanations
