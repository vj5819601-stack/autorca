# AutoRCA Pro Max — Explainable Production Root Cause Analysis Engine

AutoRCA Pro Max is an advanced, explainable AIOps/RCA prototype that combines deterministic rules, ML-based anomaly detection, incident correlation, service dependency analysis, temporal reasoning, and an interactive dashboard.

## Pipeline

Logs + Metrics
→ Parsing
→ Error Classification
→ ML Anomaly Detection
→ Temporal Correlation
→ Service Dependency Graph
→ Root Cause Ranking
→ Explainable Evidence
→ Incident Report / Dashboard

## Pro features

- Production-style structured log parsing
- Database / Network / Memory / Authentication classification
- TF-IDF + Isolation Forest anomaly detection
- Multi-log incident correlation
- Temporal burst detection
- Service dependency graph with NetworkX
- Root-cause candidate scoring
- Explainable evidence: keywords, anomaly score, frequency, temporal and dependency signals
- CSV-driven demo dataset
- Streamlit dashboard
- Automated tests
- JSON incident report export
- Clear distinction between heuristic score and calibrated probability

> This is a research/engineering prototype, not a claim of guaranteed production root-cause identification. Real production RCA should ingest validated telemetry, traces, metrics, topology and historical incidents.

## Quick start

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python -m src.main
streamlit run dashboard.py
```

Open the Streamlit URL shown in the terminal.

## Project structure

```text
autorca/
├── data/
│   └── sample_logs.csv
├── reports/
├── src/
│   ├── __init__.py
│   ├── log_parser.py
│   ├── root_cause_engine.py
│   ├── ml_anomaly_detector.py
│   ├── dependency_graph.py
│   ├── incident_engine.py
│   ├── xai_explainer.py
│   ├── report_generator.py
│   └── main.py
├── tests/
│   ├── test_log_parser.py
│   ├── test_root_cause.py
│   └── test_incident_engine.py
├── dashboard.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Technical approach

### 1. ML anomaly detection
TF-IDF converts log messages into numerical features. Isolation Forest estimates how unusual each message is relative to the incident dataset.

### 2. RCA ranking
Candidate causes are ranked using a weighted combination of:
- rule/evidence match
- anomaly signal
- category frequency
- temporal concentration
- service impact
- dependency impact

The final score is a ranking score, not a probability.

### 3. Explainability
Every incident conclusion includes human-readable evidence:
- matched log phrases
- anomalous-message signal
- dominant category
- affected service
- repeated evidence
- dependency relationships

## Evaluation

For the included demo dataset, automated tests verify parsing, classification, anomaly detection, dependency analysis and incident-level RCA behavior.

A real research evaluation should use a labeled benchmark and report precision, recall, F1, top-k RCA accuracy and false-positive rate.

## Future research upgrades

- OpenTelemetry trace ingestion
- Prometheus metrics correlation
- Kubernetes topology
- Historical incident retrieval
- Transformer-based log embeddings
- Graph neural networks for service dependency reasoning
- SHAP/LIME analysis for learned models
- Streaming Kafka ingestion
- Docker/Kubernetes deployment
- Human feedback loop for RCA correction
