# AutoRCA

AI-powered Production Failure Reproduction and Root Cause Analysis Engine.

## 📌 Overview

AutoRCA is a lightweight Root Cause Analysis (RCA) engine designed to analyze production failure logs and identify possible causes of system failures.

The system parses production logs, classifies errors, analyzes possible root causes, and generates a structured RCA report with confidence scores and supporting evidence.

## 🚀 Features

- Production log parsing
- Error classification
- Automated root cause analysis
- Root cause confidence scoring
- Evidence-based analysis
- Automated test suite
- Modular Python architecture

## 🏗️ Project Structure

```text
autorca/
│
├── data/
│
├── docs/
│
├── src/
│   ├── __init__.py
│   ├── log_parser.py
│   ├── root_cause_engine.py
│   └── main.py
│
├── tests/
│   ├── test_autorca.py
│   └── test_log_parser.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md