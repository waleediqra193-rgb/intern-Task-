import json
import os

class SeverityMatrix:
    def __init__(self, policy_json_path):
        """
        Initializes the Severity Categorization Matrix by loading the policy rules.
        """
        with open(policy_json_path, 'r', encoding='utf-8') as f:
            self.policy_rules = json.load(f)
            
        self.severity_lookup = {
            rule['behavior_class']: rule['severity_tier'] 
            for rule in self.policy_rules['behaviors']
        }

    def assign_severity(self, detection_event):
        """
        Evaluates the context of a detected violation and assigns a risk severity tier.
        Mutates the detection_event dictionary in place by adding the 'severity' field.
        """
        behavior_class = detection_event.get("behavior_class")
        
        # Look up severity from the parsed policy
        # If behavior is not explicitly defined in the policy, default to MEDIUM
        severity = self.severity_lookup.get(behavior_class, "MEDIUM")
        
        detection_event["severity"] = severity
        return detection_event

if __name__ == "__main__":
    # Test the Severity Matrix
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    policy_path = os.path.join(base_dir, 'data', 'policy_rules.json')
    
    matrix = SeverityMatrix(policy_path)
    
    # Mock event from Module 1
    mock_event = {
        "event_id": "1234-abcd",
        "behavior_class": "Carrying Overload with Forklift"
    }
    
    evaluated_event = matrix.assign_severity(mock_event)
    print(json.dumps(evaluated_event, indent=2))
