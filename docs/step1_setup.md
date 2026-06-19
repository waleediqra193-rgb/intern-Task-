# Step 1: Project Setup & Data Preparation

## Overview
This document covers the initialization of the directory structure and the extraction of the sample video dataset required for the Factory Compliance & Alert Escalation System.

## Directory Structure
The workspace has been organized as follows:
```text
factory-compliance-system/
├── README.md
├── compliance_policy.pdf
├── data/
│   ├── 0_te1.mp4 (Safe Walkway Violation)
│   ├── 1_te1.mp4 (Unauthorized Intervention)
│   ├── 2_te1.mp4 (Opened Panel Cover)
│   ├── 3_te1.mp4 (Carrying Overload with Forklift)
│   ├── 4_te1.mp4 (Safe Walkway)
│   ├── 5_te1.mp4 (Authorized Intervention)
│   ├── 6_te1.mp4 (Closed Panel Cover)
│   └── 7_te1.mp4 (Safe Carrying)
├── src/
├── docs/
└── outputs/
```

## Data Preparation
We successfully extracted an 8-video subset from the Kaggle dataset archive (`archive.zip`). Instead of unzipping the full 9.5GB payload, we isolated one sample video per defined behavior class:
- **Unsafe Behaviors**: Walkway Violation, Unauthorized Intervention, Opened Panel Cover, Forklift Overload.
- **Safe Behaviors**: Safe Walkway, Authorized Intervention, Closed Panel Cover, Safe Carrying.

These sample clips will be used to build and test the computer vision and escalation pipelines in subsequent phases.
