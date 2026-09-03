import networkx as nx
from collections import Counter

def build_service_graph(parsed_logs):
    """Build a lightweight dependency graph from explicit 'calls/depends on' phrases."""
    graph = nx.DiGraph()
    for log in parsed_logs:
        service = log.get("service")
        graph.add_node(service)
        message = log.get("message", "")
        lower = message.lower()
        marker = "calls "
        if marker in lower:
            target = message[lower.index(marker) + len(marker):].split()[0]
            graph.add_edge(service, target)
        marker = "depends on "
        if marker in lower:
            target = message[lower.index(marker) + len(marker):].split()[0]
            graph.add_edge(service, target)
    return graph

def service_impact(parsed_logs):
    counts = Counter(log.get("service") for log in parsed_logs if log.get("service"))
    return dict(counts)

def dependency_scores(graph):
    if not graph.nodes:
        return {}
    centrality = nx.betweenness_centrality(graph)
    return {node: round(float(score), 4) for node, score in centrality.items()}
