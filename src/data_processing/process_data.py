from collections import defaultdict

class TempStorage:
    def __init__(self):
        self.patient_detections = defaultdict(list)

    def save_detection(self, patient_id, image_id, detection_results):
        self.patient_detections[patient_id].append({
            "image_id": image_id,
            "results": detection_results
        })

    def get_patient_detections(self, patient_id):
        return self.patient_detections.get(patient_id, [])

def aggregate_and_assess_severity(image_results, severity_threshold):
    aggregated_results = {}

    # Aggregate data across all images
    for result in image_results:
        seen_parasites = set()  # To avoid double counting in the same image
        for parasite in result["results"]:
            parasite_type = parasite["class_name"]
            confidence = parasite["confidence"]

            # Unique key to identify each detected instance by class and bounding box
            unique_key = (parasite_type, tuple(parasite["bbox"]))

            if unique_key not in seen_parasites:
                seen_parasites.add(unique_key)

                if parasite_type not in aggregated_results:
                    aggregated_results[parasite_type] = {
                        "count": 0,
                        "total_confidence": 0.0,
                        "instances": 0
                    }

                aggregated_results[parasite_type]["count"] += 1
                aggregated_results[parasite_type]["total_confidence"] += confidence
                aggregated_results[parasite_type]["instances"] += 1

    # Calculate average confidence and severity, and print results
    severity_results = {}
    for parasite_type, data in aggregated_results.items():
        data["average_confidence"] = (
            data["total_confidence"] / data["instances"]
            if data["instances"] > 0 else 0
        )
        # Example severity computation: (count * average_confidence)
        severity = data["count"] * data["average_confidence"]

        # Assess severity based on the threshold
        severity_level = "low"
        if severity > severity_threshold:
            severity_level = "high"
        
        # Store the results
        severity_results[parasite_type] = {
            "severity": severity,
            "severity_level": severity_level,
            "count": data["count"],
            "average_confidence": data["average_confidence"]
        }
    return severity_results       
