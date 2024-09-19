# Placeholder for your Flask app initialization
from flask import Flask
from app.db.models import db
from app.routes.diagnosis_routes import diagnosis_bp
from app.routes.patients_management import patient_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    
    app.register_blueprint(diagnosis_bp)
    app.register_blueprint(patient_bp)


    return app