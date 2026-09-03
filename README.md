# AutoRCA Pro Max — Explainable Root Cause Analysis Engine

AutoRCA Pro Max is a research/engineering prototype for analyzing production-style application logs and ranking possible root causes of incidents.

It combines rule-based evidence, machine-learning anomaly detection, temporal incident analysis, service dependency information, and explainable evidence generation.

## Architecture

```mermaid
flowchart TD
    A[Application Logs] --> B[Log Parser]
    B --> C[Error Classification]

    C --> D[ML Anomaly Detection]
    C --> E[Incident & Temporal Analysis]
    C --> F[Service Dependency Analysis]

    D --> G[RCA Ranking Engine]
    E --> G
    F --> G
    C --> G

    G --> H[Explainable Evidence]
    H --> I[JSON Incident Report]
    H --> J[Streamlit Dashboard]