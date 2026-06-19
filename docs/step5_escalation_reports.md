# Step 5: Module 3 & 4 — Escalation Pipeline & Automated Reports

## Overview
These two modules handle the backend workflow of what to do with a compliance event once it has been detected and severity-classified. They fulfill the requirement of autonomous record generation and programmatic escalation routing.

## Module 3 — Escalation Pipeline
The `EscalationRouter` (`src/escalation/router.py`) executes the routing rules exactly as required:
1. It reads the severity assigned by Module 2.
2. If `LOW` or `MEDIUM`, it quietly logs the event to the database.
3. If `HIGH` or `CRITICAL`, it logs the event to the database AND pushes the event to an in-memory alert queue. This queue serves as our real-time notification trigger which the Dashboard will poll.
4. It attaches an `escalation_action` field to the event detailing exactly what it did.

## Module 4 — Automated Report Generation
The `ReportGenerator` (`src/reports/database.py`) acts as the single source of truth for historical audits.
1. It initializes a persistent SQLite database (`outputs/reports.db`).
2. It generates an immutable compliance record containing all explicitly required fields: `event_id`, `timestamp` (ISO 8601), `clip_id`, `zone`, `behavior_class`, `policy_rule_ref`, `event_description`, `severity`, and `escalation_action`.
3. An additional `bbox` field was added for Dashboard UI rendering.

Both modules are decoupled from the Vision models, meaning they can function reliably regardless of which specific detection framework is used upstream.
