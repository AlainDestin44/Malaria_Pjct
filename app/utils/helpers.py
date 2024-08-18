# Placeholder for your utility functions
from pathlib import Path
from collections import defaultdict
from app.utils.model_Ops import INPUT_NAME,INPUT_SHAPE,CLASS_NAMES,OUTPUT_NAME,sessionss
import numpy as np
import cv2

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Perform inference
def run_inference(image,output_name,input_name):
    results = sessionss.run([output_name], {input_name: image})
    # print(results[0].shape)  # Print raw model output for debugging
    return results[0]

# Process detections
def process_detections(detections, confidence_threshold=0.4):
    results = []
    for detection in detections[0]:  # Iterate over all detections
        objectness = float(detection[4])
        class_scores = detection[5:]  # The rest are class scores
        class_id = int(np.argmax(class_scores))
        confidence = class_scores[class_id]
        
        if objectness > confidence_threshold and confidence > confidence_threshold:
            class_name = CLASS_NAMES.get(class_id, str(class_id))
            bbox = detection[0:4].tolist()
            results.append({
                'class': class_id,
                'class_name': class_name,
                'confidence': confidence,
                'bbox': bbox
            })
            # print("in process detection")
    return results


def preprocess_image(image_path, input_shape):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (input_shape[2], input_shape[3]))
    image = image.transpose(2, 0, 1)
    image = np.expand_dims(image, 0)
    image = image.astype(np.float32) / 255.0
    # print('in preprocessing phase')
    return image

def process_patient_images(patient_id, image_paths, temp_storage):
    for image_path in image_paths:
        # Ensure the image path is a Path object
        image_file = Path(image_path)

        # Generate an image ID based on the filename
        image_id = f"{patient_id}_{image_file.stem}"

        # Preprocess the image
        image = preprocess_image(str(image_file), INPUT_SHAPE)

        # Run inference
        detections = run_inference(image, OUTPUT_NAME, INPUT_NAME)

        # Process detections
        results = process_detections(detections, confidence_threshold=0.5)

        # Save the results to temporary storage
        temp_storage.save_detection(patient_id, image_id, results)

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

