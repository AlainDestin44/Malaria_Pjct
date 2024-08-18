<<<<<<< HEAD
# Malaria Detection and Classification System

This project is a testing web application designed for diagnosing malaria using deep learning techniques according to the proposed process. It leverages YOLOv5 for object detection within images and provides utilities for preprocessing, model inference, and result generation.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Helper Functions and Classes](#helper-functions-and-classes)

## Project Structure

The project is organized into several directories, each serving a specific purpose:

- `app/static/css/`: Contains CSS files for application styling.
- `app/templates/`: Includes HTML templates used throughout the application.
- `app/models/`: Stores YOLOv5 model weights.
- `app/routes/`: Contains route handlers for diagnosis endpoints.
- `app/utils/`: Houses utility modules for preprocessing, inference, and result processing.
- `app/db/`: Includes the ORM model class for database interactions.
- `instance/`: Contains configuration files like `.env`.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
`git clone https://github.com/username/repo.git cd repo`

2. Install dependencies:
`pip install -r requirements.txt`

3. Set up environment variables in the `.env` file located in the `instance/` directory:
   - `SECRET_KEY`: Your Flask app secret key.
   - `DATABASE_URL`: URL to your database.
   - `MODEL_PATH`: Path to your YOLOv5 model weights.
   - `UPLOAD_FOLDER`: Directory path for uploading images.

4. Run the application:
`python run.py`
## Usage

After setting up, you can access the application through your web browser. The main functionality allows users to upload images, which are then processed by the YOLOv5 model to detect and classify potential malaria cases.

## Helper Functions and Classes

### TempStorage Class

Manages temporary storage of detection results for patients.

#### Methods

- `save_detection(patient_id, image_id, detection_results)`: Saves detection results for a patient and image.
- `get_patient_detections(patient_id)`: Retrieves detection results for a specific patient.

### Utility Functions

- `allowed_file(filename)`: Checks if the file has an allowed image extension (png, jpg, jpeg, gif).
- `run_inference(image, output_name, input_name)`: Performs model inference on the provided image.
- `process_detections(detections, confidence_threshold=0.4)`: Processes raw detection results, filtering based on confidence.
- `preprocess_image(image_path, input_shape)`: Preprocesses an image for model input by resizing, normalizing, and reshaping.
- `process_patient_images(patient_id, image_paths, temp_storage)`: Processes images for a patient, including preprocessing, inference, and saving results.
- `aggregate_and_assess_severity(image_results, severity_threshold)`: Aggregates and assesses the severity of detected parasites based on multiple images.
=======
# Malaria Diagnosis Project

This repository contains the code for a malaria diagnosis system that processes and classifies images to detect the presence of malaria parasites. The project includes image preprocessing, object detection using a deep learning model, and returns the results in a JSON format.

## Project Structure

- **`main.py`**: The main entry point of the application. It coordinates the workflow, including image preprocessing, model inference, and aggregating results, and outputs the results in JSON format.

- **`predict.py`**: Contains the core functions for processing images, performing inference with the trained model, and managing the overall prediction workflow.

- **`process_data.py`**: Handles the preprocessing of image data, including loading, resizing, and applying necessary transformations to prepare the data for the model.

## Setup Instructions

### Prerequisites

- **Python 3.x**: Ensure you have Python installed on your machine.

### Installing Dependencies

1. **Clone the repository**:

    ```bash
    git clone https://github.com/YourUsername/Malaria_Pjct.git
    cd Malaria_Pjct
    ```

2. **Create a virtual environment (Optional)**:

    ```bash
    python3 -m venv MalariaEnv
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Run the main application**:

    ```bash
    python main.py
    ```

    This will start the application, process the images, detect parasites, aggregate the results, and return them in a JSON format.

2. **Prediction Functions**:

    The `predict.py` script contains functions for processing images, performing inference with the trained model, and managing the prediction workflow.

    Example usage of the functions within a script or application:

    These functions can be integrated into other parts of the application to handle image preprocessing, model inference, and result output.

3. **Process Data**:

    Use the `process_data.py` script to preprocess image data before feeding it into the model:

    This script will prepare your dataset by loading, resizing, and transforming the images as required.

## File Descriptions

- **`main.py`**: Manages the overall application workflow, including preprocessing images, passing them to the model for parasite detection, aggregating results, and outputting them in JSON format.

- **`predict.py`**: Contains functions for image preprocessing, model inference, and prediction workflow management. These functions can be called directly in scripts or applications.

- **`process_data.py`**: Handles the preprocessing of image data, preparing it for model training or inference.

>>>>>>> origin/mainn
