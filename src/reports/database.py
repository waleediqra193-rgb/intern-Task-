import sqlite3
import os

class ReportGenerator:
    def __init__(self, db_path):
        """
        Initializes the SQLite database for compliance reporting.
        Creates the required schema if it does not exist.
        """
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create immutable compliance audit table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compliance_logs (
                event_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                clip_id TEXT NOT NULL,
                zone TEXT NOT NULL,
                behavior_class TEXT NOT NULL,
                policy_rule_ref TEXT NOT NULL,
                event_description TEXT NOT NULL,
                severity TEXT NOT NULL,
                escalation_action TEXT NOT NULL,
                bbox TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def log_event(self, event_record):
        """
        Autonomously produces a structured, immutable compliance record.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO compliance_logs (
                event_id, timestamp, clip_id, zone, behavior_class, 
                policy_rule_ref, event_description, severity, escalation_action, bbox
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event_record['event_id'],
            event_record['timestamp'],
            event_record['clip_id'],
            event_record['zone'],
            event_record['behavior_class'],
            event_record['policy_rule_ref'],
            event_record['event_description'],
            event_record['severity'],
            event_record['escalation_action'],
            str(event_record.get('bbox', '[]'))
        ))
        
        conn.commit()
        conn.close()
        
    def get_all_logs(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM compliance_logs ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
