from src.webapp.app import create_app
from src.webapp.routes import main
from src.config import MODEL_PATH,OUTPUT_NAME,CLASS_NAMES,session,SEVERITY_THRESHOLD,INPUT_NAME

# print(CLASS_NAMES)
if __name__ == "__main__":
    # Create an instance of the Flask app
    app = create_app()
    app.run(debug=True)