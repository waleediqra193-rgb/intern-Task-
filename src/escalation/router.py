import json
import os

class EscalationRouter:
    def __init__(self, db_logger):
        """
        Initializes the Escalation Pipeline.
        Takes a ReportGenerator instance to handle persistent logging.
        """
        self.db_logger = db_logger
        
        # In-memory queue to simulate live notifications (WebSocket/SSE)
        self.active_alerts = []

    def route_event(self, detection_event):
        """
        Executes programmatic workflows tied to severity tier.
        Mutates the event by appending the 'escalation_action' taken.
        """
        severity = detection_event.get("severity")
        
        if severity in ["LOW", "MEDIUM"]:
            escalation_action = "Logged to DB"
            detection_event["escalation_action"] = escalation_action
            self.db_logger.log_event(detection_event)
            
        elif severity in ["HIGH", "CRITICAL"]:
            escalation_action = "Real-time alert triggered + DB log"
            detection_event["escalation_action"] = escalation_action
            
            # Push to live notification queue
            self.active_alerts.append(detection_event)
            
            # Persist to database
            self.db_logger.log_event(detection_event)
        else:
            # Fallback
            detection_event["escalation_action"] = "Logged to DB (Unknown Severity)"
            self.db_logger.log_event(detection_event)
            
        return detection_event
        
    def get_and_clear_alerts(self):
        """
        Allows the dashboard to poll for new real-time alerts.
        """
        alerts = list(self.active_alerts)
        self.active_alerts.clear()
        return alerts

if __name__ == "__main__":
    from src.reports.database import ReportGenerator
    
    # Test the Escalation Pipeline
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(base_dir, 'outputs', 'reports.db')
    
    logger = ReportGenerator(db_path)
    router = EscalationRouter(logger)
    
    mock_event_low = {
        "event_id": "low-123",
        "timestamp": "2026-01-01T00:00:00Z",
        "clip_id": "test.mp4",
        "zone": "Zone-1",
        "behavior_class": "Opened Panel Cover",
        "policy_rule_ref": "Section 5",
        "event_description": "Panel open.",
        "severity": "LOW"
    }
    
    mock_event_crit = {
        "event_id": "crit-456",
        "timestamp": "2026-01-01T00:00:01Z",
        "clip_id": "test.mp4",
        "zone": "Zone-2",
        "behavior_class": "Unauthorized Intervention",
        "policy_rule_ref": "Section 4",
        "event_description": "No vest.",
        "severity": "CRITICAL"
    }
    
    router.route_event(mock_event_low)
    router.route_event(mock_event_crit)
    
    print("Logs in DB:")
    print(json.dumps(logger.get_all_logs(), indent=2))
    
    print("Active Alerts in Queue:")
    print(json.dumps(router.get_and_clear_alerts(), indent=2))
