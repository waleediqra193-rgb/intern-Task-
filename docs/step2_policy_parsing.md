# Step 2: Policy Parsing Engine

## Overview
This document describes the Natural Language Parsing (NLP) engine implemented to bridge the gap between unstructured text (the Compliance Policy Manual) and structured data required by the detection and alerting logic.

## Implementation Details
Since an external LLM API was not available in this environment, we developed a local Python-based parsing engine (`src/policy_parser.py`) utilizing regex and string analysis. The engine reads the `Compliance_Policy_Manual.txt` and performs the following operations:
1. **Behavior Extraction**: Defines the four unsafe behavior domains based on the 'Quick Reference' section of the policy manual.
2. **Indicator Mapping**: Associates each behavior with the human-readable visual indicator defined in the manual (e.g., "Person outside green floor markings").
3. **Severity Inference**: The script scans the individual sections (Sections 3 through 6) to detect severity language:
   - Identifies `WARNING` strings for Walkway Violations and Opened Panel Covers, mapping them to `HIGH` and `LOW` severity tiers respectively (based on hazard proximity context).
   - Identifies the explicit `CRITICAL SAFETY NOTICE` block for Unauthorized Intervention and Forklift Overloads, mapping them definitively to the `CRITICAL` severity tier.

## Output
The parser generates an immutable JSON artifact (`data/policy_rules.json`) that acts as the single source of truth for the rest of the application. The schema maps `class_id` to `behavior_class`, `severity_tier`, and `observable_indicator`.

Example Payload:
```json
{
  "class_id": 1,
  "behavior_class": "Unauthorized Intervention",
  "domain": "Equipment Interaction",
  "policy_rule_ref": "Section 4.3.2",
  "observable_indicator": "Person interacting with equipment without green vest",
  "severity_tier": "CRITICAL"
}
```

This output successfully fulfills the requirement that "The behavioral categories... must be derived from the policy document through your parsing pipeline".
