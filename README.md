# Factory Compliance & Alert Escalation System

## Overview
This repository contains an end-to-end automated compliance system designed to ingest raw factory video feeds, parse an unstructured regulatory policy document, detect behavioral violations, classify them by severity, and route alerts to a live operations dashboard.

## Architecture
The system is divided into five functional modules:
1. **Module 1 — Detection Engine** (`src/detection/engine.py`): Ingests video clips and generates behavioral violation detection events based on the observable indicators extracted from the compliance policy.
2. **Module 2 — Severity Categorization Matrix** (`src/severity/matrix.py`): Evaluates the context of each detection and assigns a risk severity tier (LOW/MEDIUM/HIGH/CRITICAL) derived strictly from the compliance policy's hazard language.
3. **Module 3 — Escalation Pipeline** (`src/escalation/router.py`): Executes routing workflows, sending LOW/MEDIUM events to the database and HIGH/CRITICAL events to a real-time notification queue.
4. **Module 4 — Automated Report Generation** (`src/reports/database.py`): Autonomously produces structured, immutable SQLite database records for every detected violation, serving as the facility's audit trail.
5. **Module 5 — Operations Dashboard** (`src/dashboard/app.py`): A Streamlit web application providing a live feed monitor, active alert timeline stream, and filterable historical log with CSV export functionality.

## Policy Parsing Approach
An automated NLP parser (`src/policy_parser.py`) was developed to bridge the gap between unstructured text and structured data. It reads `Compliance_Policy_Manual.txt` and uses string analysis/regex to extract the four defined behavioral domains. 
It analyzes contextual warning tags (e.g., matching "CRITICAL SAFETY NOTICE" vs "WARNING") to infer severity schemas. The output is saved to `data/policy_rules.json`, serving as the single source of truth for the entire pipeline.

## Severity Mapping Rationale
Severity mappings were derived strictly from the text of the `Compliance_Policy_Manual.txt`:
- **Safe Walkway Violation** → HIGH (Warning + high frequency / proximity to hazard).
- **Unauthorized Intervention** → CRITICAL (Explicitly flagged under 'CRITICAL SAFETY NOTICE').
- **Opened Panel Cover** → LOW (Condition observed but no immediate personnel proximity; flagged as 'WARNING').
- **Carrying Overload with Forklift** → CRITICAL (Explicitly flagged under 'CRITICAL SAFETY NOTICE').

## Setup & Run Instructions
1. Install Python 3.11+.
2. Install dependencies:
   ```bash
   pip install opencv-python streamlit pandas
   ```
3. Run the Policy Parser to generate rules:
   ```bash
   python src/policy_parser.py
   ```
4. Start the Operations Dashboard:
   ```bash
   streamlit run src/dashboard/app.py
   ```

*Documentation for the step-by-step implementation of this project can be found in the `docs/` folder.*
