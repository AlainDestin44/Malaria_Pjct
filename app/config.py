# Placeholder for your configuration settings
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../instance/.env'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY=os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
    MAX_IMAGES = 5