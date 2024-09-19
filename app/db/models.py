# Placeholder for your database models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr



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

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "status": self.status
        }

    def __repr__(self):
        return f"<PatientDiagnosis {self.patient_id}>"

# class Patients(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     patient_id = db.Column(db.String(80), nullable=False)
#     first_name= db.Column(db.String(120), nullable=False)

#     def __repr__(self):
#         return f"<UploadedFile {self.patient_id} - {self.first_name}>"
    
# class PatientImages(db.Model):
#     __tablename__ = 'PatientsImages'
#     image_id = db.Column(db.Integer, primary_key=True)
#     patient_id = db.Column(db.String(80), nullable=False)
#     image_path= db.Column(db.String(120), nullable=False)


#     def __repr__(self):
#         return f"<UploadedFile {self.patient_id} - {self.image_path}>"
class PatientImages(db.Model):
    __tablename__ = 'patientsimages'
    image_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(80), nullable=False)
    image_path= db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return f"<UploadedFile {self.patient_id} - {self.image_path}>"
        
class Patients(db.Model):
    __tablename__ = 'Patients'
    patient_id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'other', name='gender_types'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self, **kwargs):
        super(Patients, self).__init__(**kwargs)
        if not self.patient_id:
            self.patient_id = self.generate_patient_id()

    def generate_patient_id(self):
        # Generate patient ID with the 'PID' prefix
        prefix = 'PID'
        with db.session.no_autoflush:
            last_patient = db.session.query(Patients).order_by(Patients.patient_id.desc()).first()
            if last_patient:
                # Extract the numeric part of the ID and increment it
                last_id = int(last_patient.patient_id[len(prefix):])
                new_id = last_id + 1
            else:
                # Start with 1 if no patients exist
                new_id = 1
            # Return the new patient ID in the format PID01, PID02, etc.
            return f'{prefix}{new_id:02d}'