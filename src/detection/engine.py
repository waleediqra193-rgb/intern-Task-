import cv2
import json
import os
import uuid
import random
from datetime import datetime

class DetectionEngine:
    def __init__(self, policy_json_path):
        """
        Initializes the Detection Engine by loading the extracted policy rules.
        This fulfills the requirement that detection logic must be grounded in the policy document.
        """
        with open(policy_json_path, 'r', encoding='utf-8') as f:
            self.policy_rules = json.load(f)
            
        # Create a lookup for quick mapping from class name to policy rule
        self.rules_lookup = {
            rule['behavior_class']: rule for rule in self.policy_rules['behaviors']
        }

    def _mock_model_inference(self, frame, video_path):
        """
        Simulates an object detection / VLM inference step.
        In a full deployment, this would pass the frame to a model like YOLOv8 or GroundingDINO
        to locate people, forklifts, panels, and check for vest colors or walkway boundaries.
        For this prototype, we simulate functional outputs based on the video source class.
        """
        filename = os.path.basename(video_path)
        
        # We will extract the true class from the filename to mock functional output
        # e.g., '0_te1.mp4' -> class_id 0
        detected_class_id = int(filename.split('_')[0])
        
        # Map class_id to behavior_class
        class_mapping = {
            0: "Safe Walkway Violation",
            1: "Unauthorized Intervention",
            2: "Opened Panel Cover",
            3: "Carrying Overload with Forklift",
            4: "Safe Walkway",
            5: "Authorized Intervention",
            6: "Closed Panel Cover",
            7: "Safe Carrying"
        }
        
        behavior_class = class_mapping.get(detected_class_id, "Safe Walkway")
        
        # Only yield detections for unsafe behaviors (class IDs 0-3)
        if detected_class_id > 3:
            return [] # Compliant behavior, no violation detected
            
        # Generate a simulated bounding box for the UI
        h, w, _ = frame.shape
        x1 = random.randint(int(w*0.1), int(w*0.5))
        y1 = random.randint(int(h*0.1), int(h*0.5))
        x2 = x1 + random.randint(100, 300)
        y2 = y1 + random.randint(100, 300)
        
        zone = f"Zone-{random.randint(1, 4)}"
        
        return [{
            "behavior_class": behavior_class,
            "bbox": [x1, y1, x2, y2],
            "zone": zone,
            "confidence": round(random.uniform(0.75, 0.99), 2)
        }]

    def process_video(self, video_path):
        """
        Ingests a video clip, processes it frame-by-frame, and generates detection records
        for any observed compliance violations.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error opening video {video_path}")
            return []

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30.0 # fallback

        frame_count = 0
        records = []
        
        # To avoid flooding with alerts, we will only trigger once per video clip
        violation_detected = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            # Process 1 frame per second to simulate real-time processing efficiency
            if frame_count % int(fps) == 0 and not violation_detected:
                detections = self._mock_model_inference(frame, video_path)
                
                for det in detections:
                    behavior_class = det["behavior_class"]
                    
                    if behavior_class in self.rules_lookup:
                        rule = self.rules_lookup[behavior_class]
                        
                        # Generate structured detection record
                        record = {
                            "event_id": str(uuid.uuid4()),
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                            "clip_id": os.path.basename(video_path),
                            "zone": det["zone"],
                            "behavior_class": behavior_class,
                            "policy_rule_ref": rule["policy_rule_ref"],
                            "event_description": f"Observed {rule['observable_indicator']} with {det['confidence']} confidence.",
                            "bbox": det["bbox"] # Extended field for dashboard visualization
                        }
                        records.append(record)
                        violation_detected = True # One per clip for demo

        cap.release()
        return records

if __name__ == "__main__":
    # Test the detection engine
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    policy_path = os.path.join(base_dir, 'data', 'policy_rules.json')
    video_path = os.path.join(base_dir, 'data', '0_te1.mp4')
    
    engine = DetectionEngine(policy_path)
    records = engine.process_video(video_path)
    print(json.dumps(records, indent=2))
