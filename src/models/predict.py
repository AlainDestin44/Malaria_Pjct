import cv2
import numpy as np
from src.config import MODEL_PATH, INPUT_SHAPE,OUTPUT_NAME,INPUT_NAME,session,CLASS_NAMES
from pathlib import Path
# Preprocess the image
def preprocess_image(image_path, input_shape):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (input_shape[2], input_shape[3]))
    image = image.transpose(2, 0, 1)
    image = np.expand_dims(image, 0)
    image = image.astype(np.float32) / 255.0
    return image

# Perform inference
def run_inference(image,output_name,input_name):
    results = session.run([output_name], {input_name: image})
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
    return results

# def process_patient_images(patient_id, image_folder, temp_storage):
#     # Ensure the image folder path is a Path object
#     image_folder = Path(image_folder)
    
#     # Get all image files in the folder
#     image_files = [f for f in image_folder.iterdir() if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.bmp')]
    
#     for image_file in image_files:
#         # Generate an image ID based on the filename
#         image_id = f"{patient_id}_{image_file.stem}"
        
#         # Preprocess the image
#         image = preprocess_image(str(image_file), INPUT_SHAPE)
        
#         # Run inference
#         detections = run_inference(image,OUTPUT_NAME,INPUT_NAME)
#         # print(detections)
        
#         # Process detections
#         results = process_detections(detections, confidence_threshold=0.5)
        
#         # Save the results to temporary storage
#         temp_storage.save_detection(patient_id, image_id, results)

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



