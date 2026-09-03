# AutoRCA — Production Failure Root Cause Analysis Engine

AutoRCA is an explainable, rule-based Root Cause Analysis engine for production failure logs.

## What it does

AutoRCA converts raw production logs into an incident-level RCA report:

**Logs → Error Classification → Root Cause Ranking → Evidence → Affected Service → Incident Summary**

### Features

- Production log parsing
- Database, network, memory and authentication error classification
- Explainable root-cause ranking
- Matched-keyword evidence
- Multi-log incident analysis
- Affected-service ranking
- Likely root-cause identification
- Evidence correlation across logs
- CSV dataset processing
- Automated tests with pytest

> The ranking score is a rule-based heuristic score. It is not a calibrated probability or a guarantee of the actual production root cause.

## Project structure

```text
autorca/
├── data/
│   └── sample_logs.csv
├── src/
│   ├── __init__.py
│   ├── log_parser.py
│   ├── root_cause_engine.py
│   ├── multi_log_analyzer.py
│   └── main.py
├── tests/
│   ├── test_autorca.py
│   └── test_log_parser.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Run

From the project root:

```bash
python -m src.main
```

The application loads `data/sample_logs.csv`, analyzes each log, and prints an incident-level RCA summary.

## Test

```bash
python -m pytest -q
```

## Example incident conclusion

```text
Dominant Category    : DATABASE
Most Affected Service: PaymentService
Likely Root Cause    : Database unavailable
Supporting Evidence  : connection timeout
```

## Limitations

This version is a research/demo prototype. It uses deterministic rules and keyword matching. Production deployment would require richer telemetry, distributed tracing, metrics, historical incidents, and validated ML/statistical models.
