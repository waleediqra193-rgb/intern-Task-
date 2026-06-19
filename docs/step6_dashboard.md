# Step 6: Module 5 — Operations Dashboard

## Overview
The Operations Dashboard is the final piece of the automated compliance system. It provides a real-time graphical interface for facility overseers to monitor the factory floor, view active alerts, and export compliance audit records.

## Implementation Details
The dashboard was built using **Streamlit** (`src/dashboard/app.py`). It integrates all previous modules (Detection, Severity, Escalation, Reports) into a single unified application loop.

### View A: Live Feed Monitor
- Allows the user to select one of the ingested video feeds.
- Processes the video utilizing `cv2`, passing frames to the `DetectionEngine`.
- If a violation is detected and routed by the `SeverityMatrix`, the dashboard renders a visible bounding box over the subject, color-coded by severity (Red for HIGH/CRITICAL, Yellow for LOW/MEDIUM).
- Features a prominent status indicator that turns into an `ALERT TRIGGERED` banner upon critical violations.

### View B: Alert Timeline Stream
- A dynamic, chronological list of active alerts.
- This view polls the `EscalationRouter`'s active alert queue. As soon as a `HIGH` or `CRITICAL` event occurs in the live feed, it is pushed to this timeline.

### View C: Historical Log & Export
- Connects directly to the immutable SQLite database (`outputs/reports.db`) populated by the `ReportGenerator`.
- Renders the full audit trail as a sortable, interactive Pandas DataFrame.
- Provides multiselect filters for `Severity` and `Behavior Class`.
- Includes a functional "Export Filtered Logs (CSV)" button that complies with the data retention requirement.

## Usage
To run the dashboard locally:
```bash
cd factory-compliance-system
streamlit run src/dashboard/app.py
```
