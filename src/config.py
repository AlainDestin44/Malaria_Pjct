# config.py
import onnx
import onnxruntime

# Define the path to your model
MODEL_PATH = '/Users/alaindestinkarasira/Documents/Malaria_Diagnosis_/src/models/weights/best.onnx'
SEVERITY_THRESHOLD=10
# Function to load the model and create a session
def load_model(model_path):
    # Load the ONNX model
    model = onnx.load(model_path)
    # Create an ONNX Runtime session
    session = onnxruntime.InferenceSession(model_path)
    return model, session

# Load the model and session
model, session = load_model(MODEL_PATH)

# Get model input and output details
INPUT_NAME = session.get_inputs()[0].name
INPUT_SHAPE = session.get_inputs()[0].shape
OUTPUT_NAME = session.get_outputs()[0].name

# Optionally, load class names from the model metadata
CLASS_NAMES = {}
for prop in model.metadata_props:
    if prop.key == "names" or prop.key == "classes":
        CLASS_NAMES=eval(prop.value)  # Be cautious with eval
        break
