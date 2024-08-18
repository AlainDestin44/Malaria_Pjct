import onnx
import onnxruntime

# Load ONNX model
def load_model(model_path):
    model = onnx.load(model_path)
    session = onnxruntime.InferenceSession(model_path)
    return model, session

# Get model metadata
def get_model_info(model):
    try:
        return {
            'input_shape': [dim.dim_value for dim in model.graph.input[0].type.tensor_type.shape.dim],
            'output_shape': [dim.dim_value for dim in model.graph.output[0].type.tensor_type.shape.dim],
            'opset_version': model.opset_import[0].version
        }
    except Exception as e:
        return {'error': str(e)}

# Get class names from metadata
def get_class_names(metadata):
    for prop in metadata:
        if prop.key == "names" or prop.key == "classes":
            class_names = eval(prop.value)  # Be cautious with eval
            return class_names
    return {}
