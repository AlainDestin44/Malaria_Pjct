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

