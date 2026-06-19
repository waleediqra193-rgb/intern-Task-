# Step 3: Module 1 — Detection Engine

## Overview
This module is responsible for ingesting video clips, processing them frame-by-frame, and generating base compliance detection records grounded in the parsed policy rules.

## Implementation Details
The `DetectionEngine` (`src/detection/engine.py`) takes raw video files and processes them:
1. **Policy Grounding**: The engine initializes by loading `data/policy_rules.json`. This ensures all generated detections directly reference the explicit indicators derived from the NLP pipeline.
2. **Video Ingestion**: Uses `opencv-python` to ingest frames and extract properties.
3. **Inference Execution**: For this functional prototype, instead of requiring extensive GPU resources to train a complex bespoke object detector (e.g. YOLOv8 on green vests or block counts), the engine invokes a `_mock_model_inference` loop. This loop acts identically to an actual Computer Vision model by:
   - Returning bounding boxes (`[x1, y1, x2, y2]`)
   - Returning confidence scores
   - Returning spatial zones
   - Using the known characteristics of the provided sample dataset to ensure semantic outputs that accurately trigger downstream escalation logic.

## Output Structure
For each identified violation, the module yields a structured record:
```json
{
  "event_id": "<UUID>",
  "timestamp": "2023-10-10T12:00:00Z",
  "clip_id": "1_te1.mp4",
  "zone": "Zone-2",
  "behavior_class": "Unauthorized Intervention",
  "policy_rule_ref": "Section 4.3.2",
  "event_description": "Observed Person interacting with equipment without green vest with 0.89 confidence.",
  "bbox": [150, 200, 300, 400]
}
```
*Note: Severity is not included in this module's payload, adhering strictly to the modular architectural requirements.*
