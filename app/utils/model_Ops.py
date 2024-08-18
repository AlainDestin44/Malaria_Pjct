import onnx
import onnxruntime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
MODEL_PATH = '/Users/alaindestinkarasira/Documents/Malaria_pjct_v1/MalariaDiagnosis/app/models/best.onnx'

# Function to load the model and create a session
def load_model(model_path):
    # Load the ONNX model
    model = onnx.load(model_path)
    # Create an ONNX Runtime session
    sessionx = onnxruntime.InferenceSession(model_path)
    return model, sessionx

# Load the model and session
model, sessionss = load_model(MODEL_PATH )

# Get model input and output details
INPUT_NAME = sessionss.get_inputs()[0].name
INPUT_SHAPE = sessionss.get_inputs()[0].shape
OUTPUT_NAME = sessionss.get_outputs()[0].name

# Optionally, load class names from the model metadata
CLASS_NAMES = {}
for prop in model.metadata_props:
    if prop.key == "names" or prop.key == "classes":
        CLASS_NAMES=eval(prop.value)  # Be cautious with eval
        break