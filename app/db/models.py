# Placeholder for your database models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

class DiagnosisReport(db.Model):
    __tablename__ = 'diagnosis_report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.String(50), nullable=False)
    detected_parasites = db.Column(JSONB, nullable=False)
    status=db.Column(db.String(50), nullable=False)

    def __init__(self, patient_id, detected_parasites):
        self.patient_id = patient_id
        self.detected_parasites = detected_parasites
        self.status='initiated'

    def __repr__(self):
        return f"<PatientDiagnosis {self.patient_id}>"

class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(80), nullable=False)
    first_name= db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<UploadedFile {self.patient_id} - {self.first_name}>"
    
class PatientImages(db.Model):
    __tablename__ = 'PatientsImages'
    image_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(80), nullable=False)
    image_path= db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return f"<UploadedFile {self.patient_id} - {self.image_path}>"
