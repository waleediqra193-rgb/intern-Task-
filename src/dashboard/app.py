import streamlit as st
import pandas as pd
import cv2
import os
import sys

# Ensure src modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.detection.engine import DetectionEngine
from src.severity.matrix import SeverityMatrix
from src.escalation.router import EscalationRouter
from src.reports.database import ReportGenerator

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
POLICY_PATH = os.path.join(BASE_DIR, 'data', 'policy_rules.json')
DB_PATH = os.path.join(BASE_DIR, 'outputs', 'reports.db')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Initialize Modules
@st.cache_resource
def init_system():
    engine = DetectionEngine(POLICY_PATH)
    matrix = SeverityMatrix(POLICY_PATH)
    logger = ReportGenerator(DB_PATH)
    router = EscalationRouter(logger)
    return engine, matrix, logger, router

engine, matrix, logger, router = init_system()

st.set_page_config(page_title="Factory Compliance Dashboard", layout="wide")
st.title("🛡️ Factory Compliance & Alert Escalation Dashboard")

# Layout: 2 Columns for Live Feed and Alert Timeline
col1, col2 = st.columns([2, 1])

with col1:
    st.header("View A: Live Feed Monitor")
    
    # Get list of sample videos
    video_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.mp4')]
    selected_video = st.selectbox("Select Camera Feed (Mock Video Clip)", video_files)
    
    start_feed = st.button("▶️ Process Feed")
    
    video_placeholder = st.empty()
    status_indicator = st.empty()

with col2:
    st.header("View B: Alert Timeline Stream")
    alert_placeholder = st.empty()
    
# Historical Logs Section
st.markdown("---")
st.header("View C: Historical Log & Export")
log_container = st.empty()

# Logic to process video
if start_feed and selected_video:
    video_path = os.path.join(DATA_DIR, selected_video)
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_count = 0
    violation_detected = False
    active_detections = []
    
    # Timeline state
    if "timeline" not in st.session_state:
        st.session_state.timeline = []

    status_indicator.info("Status: Monitoring...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # Process 1 frame per second to simulate real-time processing
        if frame_count % int(fps) == 0 and not violation_detected:
            # Module 1: Detection
            detections = engine._mock_model_inference(frame, video_path)
            
            for det in detections:
                behavior_class = det["behavior_class"]
                
                if behavior_class in engine.rules_lookup:
                    rule = engine.rules_lookup[behavior_class]
                    import uuid
                    from datetime import datetime
                    raw_event = {
                        "event_id": str(uuid.uuid4()),
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "clip_id": selected_video,
                        "zone": det["zone"],
                        "behavior_class": behavior_class,
                        "policy_rule_ref": rule["policy_rule_ref"],
                        "event_description": f"Observed {rule['observable_indicator']} with {det['confidence']} confidence.",
                        "bbox": det["bbox"]
                    }
                    
                    # Module 2: Severity Matrix
                    evaluated_event = matrix.assign_severity(raw_event)
                    
                    # Module 3: Escalation Router (implicitly triggers Module 4: ReportGenerator)
                    final_event = router.route_event(evaluated_event)
                    
                    # Dashboard Rendering updates
                    violation_detected = True
                    sev = final_event['severity']
                    
                    # Update status indicator
                    if sev in ['HIGH', 'CRITICAL']:
                        status_indicator.error(f"🚨 ALERT TRIGGERED: {behavior_class} ({sev} RISK)")
                    else:
                        status_indicator.warning(f"⚠️ VIOLATION DETECTED: {behavior_class} ({sev} RISK)")
                    
                    # Draw BBox
                    x1, y1, x2, y2 = det['bbox']
                    color = (0, 0, 255) if sev in ['HIGH', 'CRITICAL'] else (0, 255, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                    cv2.putText(frame, f"{behavior_class} [{sev}]", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                    
        # Render Frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
        
        # Update Timeline
        alerts = router.get_and_clear_alerts()
        if alerts:
            st.session_state.timeline.extend(alerts)
            
        with alert_placeholder.container():
            for al in reversed(st.session_state.timeline):
                st.error(f"**{al['timestamp']}** | {al['zone']} | {al['behavior_class']}")
        
    cap.release()
    
    if not violation_detected:
        status_indicator.success("Status: Feed finished. No violations detected. (COMPLIANT)")

# Always render historical logs
logs = logger.get_all_logs()
if logs:
    df = pd.DataFrame(logs)
    
    # Filter controls
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f_sev = st.multiselect("Filter by Severity", options=df['severity'].unique())
    with col_f2:
        f_class = st.multiselect("Filter by Behavior Class", options=df['behavior_class'].unique())
        
    if f_sev:
        df = df[df['severity'].isin(f_sev)]
    if f_class:
        df = df[df['behavior_class'].isin(f_class)]
        
    # Drop bbox for cleaner display
    display_df = df.drop(columns=['bbox'], errors='ignore')
    
    st.dataframe(display_df, use_container_width=True)
    
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Logs (CSV)",
        data=csv,
        file_name='compliance_audit_log.csv',
        mime='text/csv',
    )
else:
    st.info("No compliance logs available yet.")
