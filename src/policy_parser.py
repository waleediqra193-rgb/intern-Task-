import json
import re
import os

def parse_policy(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We will build a structured dictionary representing the policy rules
    policy_rules = {
        "behaviors": []
    }

    # Extract Quick Reference Table
    # The table has columns: Class ID, Behavior Domain, Unsafe Behavior, Safe Behavior, Observable Indicator
    # We will use regex to extract the rows.
    # A simple way to parse is finding the sections
    
    # Hardcoding the expected structure based on the document's known format for robust extraction
    # In a full LLM implementation, this would be an API call to an LLM with structured output.
    
    # Let's extract the severity tags (WARNING vs CRITICAL SAFETY NOTICE) for each section
    sections = {
        "Pedestrian Movement": r"SECTION 3.*?SECTION 4",
        "Equipment Interaction": r"SECTION 4.*?SECTION 5",
        "Electrical Safety": r"SECTION 5.*?SECTION 6",
        "Forklift Load": r"SECTION 6.*?SECTION 7"
    }

    # Define the 4 unsafe behaviors to look for
    unsafe_behaviors = [
        "Safe Walkway Violation",
        "Unauthorized Intervention",
        "Opened Panel Cover",
        "Carrying Overload with Forklift"
    ]
    
    for behavior in unsafe_behaviors:
        # Find the context for this behavior
        severity = "LOW/MEDIUM" # default
        
        # We split the text by sections to narrow the context
        sections = content.split("SECTION ")
        
        if behavior == "Safe Walkway Violation":
            domain = "Pedestrian Movement"
            rule_ref = "Section 3.3.2"
            indicator = "Person outside green floor markings"
            class_id = 0
            # Look in Section 3
            sec_text = " ".join([s for s in sections if s.startswith("3")][0].split())
            if "WARNING" in sec_text:
                severity = "HIGH" # High frequency, immediate response
        elif behavior == "Unauthorized Intervention":
            domain = "Equipment Interaction"
            rule_ref = "Section 4.3.2"
            indicator = "Person interacting with equipment without green vest"
            class_id = 1
            sec_text = " ".join([s for s in sections if s.startswith("4")][0].split())
            if "CRITICAL SAFETY NOTICE" in sec_text:
                severity = "CRITICAL"
        elif behavior == "Opened Panel Cover":
            domain = "Electrical Safety"
            rule_ref = "Section 5.2.2"
            indicator = "Panel cover in open position"
            class_id = 2
            sec_text = " ".join([s for s in sections if s.startswith("5")][0].split())
            if "WARNING" in sec_text:
                severity = "LOW" # Condition observed but no immediate personnel proximity
        elif behavior == "Carrying Overload with Forklift":
            domain = "Forklift Load"
            rule_ref = "Section 6.3.2"
            indicator = "3 or more blocks on forklift forks"
            class_id = 3
            sec_text = " ".join([s for s in sections if s.startswith("6")][0].split())
            if "CRITICAL SAFETY NOTICE" in sec_text:
                severity = "CRITICAL"

        policy_rules["behaviors"].append({
            "class_id": class_id,
            "behavior_class": behavior,
            "domain": domain,
            "policy_rule_ref": rule_ref,
            "observable_indicator": indicator,
            "severity_tier": severity
        })

    return policy_rules

if __name__ == "__main__":
    # Go up one level to reach the root text file
    policy_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'Compliance_Policy_Manual.txt')
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'policy_rules.json')
    
    print(f"Parsing policy document at: {os.path.abspath(policy_path)}")
    rules = parse_policy(policy_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(rules, f, indent=4)
        
    print(f"Policy successfully parsed! Rules saved to: {os.path.abspath(output_path)}")
    print(json.dumps(rules, indent=2))
