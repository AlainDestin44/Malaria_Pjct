# Malaria Diagnosis Project

This repository contains the code for a malaria diagnosis system that processes and classifies images for the presence of malaria parasites. The project uses deep learning techniques for image classification and data processing.

## Project Structure

- **`main.py`**: This is the main entry point of the application. It initializes the system, handles user inputs, and coordinates the overall workflow.
  
- **`predict.py`**: Contains the functions and models used to make predictions on input images. This file is responsible for loading the trained model and performing the classification tasks.

- **`process_data.py`**: Handles data preprocessing tasks, including image loading, resizing, and any transformations needed before feeding the data into the model.

## Setup Instructions

### Prerequisites

- **Python 3.x**: Ensure you have Python installed on your machine.
- **Virtual Environment**: Just create a virtual environment.

### Installing Dependencies

1. **Clone the repository**:

    ```bash
    git clone https://github.com/YourUsername/Malaria_Pjct.git
    cd Malaria_Pjct
    ```

2. **Create a virtual environment (Optional)**:

    ```bash
    python3 -m venv MalariaEnv
    source MalariaEnv/bin/activate  # On Windows, use `MalariaEnv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

    Ensure that a `requirements.txt` file is included in the repository with all the necessary dependencies. If you don't have one, you can generate it using:

    ```bash
    pip freeze > requirements.txt
    ```

### Running the Application

1. **Run the main application**:

    ```bash
    python main.py
    ```

    This will start the application and guide you through the process of uploading images, processing them, and getting predictions.

2. **Make Predictions**:

    The `predict.py` script can be used to make standalone predictions if needed:

    ```bash
    python predict.py --image_path path/to/image.png
    ```

3. **Process Data**:

    You can preprocess the data using the `process_data.py` script:

    ```bash
    python process_data.py --data_dir path/to/dataset
    ```

## File Descriptions

- **`main.py`**: Manages the workflow of the application, including user input, invoking the prediction and data processing modules, and handling outputs.

- **`predict.py`**: Focuses on model inference, loading the trained model, and classifying new images to determine the presence of malaria.

- **`process_data.py`**: Prepares the image data for training and prediction by performing necessary preprocessing steps.



