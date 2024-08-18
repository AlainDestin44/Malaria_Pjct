from flask import Blueprint, render_template_string, request, jsonify
import json
import os
from ..config import MODEL_PATH,OUTPUT_NAME,CLASS_NAMES,session,SEVERITY_THRESHOLD,INPUT_NAME,INPUT_SHAPE
from src.models.predict import preprocess_image, run_inference, process_detections,process_patient_images
from src.data_processing.process_data import TempStorage, aggregate_and_assess_severity

# Initialize the model and session
# model, session = load_model(MODEL_PATH)
# class_names = get_class_names(model.metadata_props)

# # Get model details
# input_name = session.get_inputs()[0].name
# input_shape = session.get_inputs()[0].shape
# output_name = session.get_outputs()[0].name

# Blueprint for Flask routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    image_path = '/Users/alaindestinkarasira/Documents/Malaria_Diagnosis_/data/Raw/pm_62.jpg'  # Update this path
    image = preprocess_image(image_path, session.get_inputs()[0].shape)
    detections = run_inference(image,OUTPUT_NAME,INPUT_NAME)
    results = process_detections(detections, 0.4)
    # Create a temporary storage instance
    temp_storage = TempStorage()
    patient_id="Pat_001"
   # Process the images for the given patient
           # Preprocess the image
    image = preprocess_image(str(image_path), INPUT_SHAPE)
    
    # Run inference
    detections = run_inference(image,OUTPUT_NAME,INPUT_NAME)
    # print(detections)
    
    # Process detections
    results = process_detections(detections, confidence_threshold=0.5)
    
    # Save the results to temporary storage
    temp_storage.save_detection(patient_id, 'im1', results)


    # Aggregate results and assess severity
    aggregated_results = aggregate_and_assess_severity(temp_storage.get_patient_detections(patient_id), 2)
    return aggregated_results

def fetch_image_paths_from_db(patient_id):
    # Query the database for image paths associated with the patient ID
    # image_records = session.query(Image).filter_by(patient_id=patient_id).all()
    
    # # Extract the file paths from the records
    # image_paths = [record.file_path for record in image_records]

    image_folder = "/Users/alaindestinkarasira/Documents/Malaria_Diagnosis_/data/PO"  # Ensure the case matches

    # Log the received request and paths
    print(f"Processing images for patient ID: {patient_id} in folder: {image_folder}")
    # Create a list to hold image paths
    image_paths = []

    # Iterate through the folder and collect all image file paths
    for root, dirs, files in os.walk(image_folder):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):  # Add more extensions if needed
                image_paths.append(os.path.join(root, file))
    return image_paths

@main.route('/Process',methods=['GET'])
def process_images():
    try:
        # Hardcoded patient ID and image folder path
        patient_id = "pat_001"
        # Log the received request and paths
        print(f"Processing images for patient ID: {patient_id}")
        # Create a list to hold image paths
        image_paths = fetch_image_paths_from_db(patient_id)

        # Create a temporary storage instance
        temp_storage = TempStorage()

        # Process the images for the given patient
        process_patient_images(patient_id, image_paths, temp_storage)

        # Aggregate results and assess severity
        aggregated_results= aggregate_and_assess_severity(
            temp_storage.get_patient_detections(patient_id), 2
        )
        # Construct the response with patient ID, parasite detected, probability, severity
        response_data = {
            "patient_id": patient_id,
            "detected_parasites": []
        }

        # Iterate through the aggregated results and add each parasite's details
        for parasite_type, data in aggregated_results.items():
            response_data["detected_parasites"].append({
                "parasite_name": parasite_type,
                "severity_level": data["severity_level"],
                "count": data["count"],
                "average_confidence": data["average_confidence"]
            })

        # Log the results
        # print(f"Aggregated Instances: {aggregated_results['instances']}")
        print(f"Aggregated Instances: {aggregated_results}")

        # Return the results as a JSON response
         # Return the response as a JSON object
        return jsonify(response_data)
    except Exception as e:
        # Log any exceptions that occur
        print(f"Error processing images: {str(e)}")
        return jsonify({'error': str(e)}), 500


def init_routes(app):
    app.register_blueprint(main)
