from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.db.models import Patients, DiagnosisReport, db
from app.utils.helpers import process_patient_images, aggregate_and_assess_severity

patient_bp = Blueprint('patient_bp', __name__)
@patient_bp.route('/')
def index():
    return render_template('dashboard.html')

@patient_bp.route('/register_patient', methods=['POST','GET'])
def register_patient():
    try:
        # Get the incoming JSON data
        data = request.get_json()

        # Extract the form data
        name = data.get('name')
        email = data.get('email')
        age = data.get('age')
        gender = data.get('gender')

        # Validate that required fields are not empty
        if not all([name, age, gender]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        # Create a new patient instance
        new_patient = Patients(
            name=name,
            email=email,
            age=age,
            gender=gender
        )

        # Add and commit the new patient to the database
        db.session.add(new_patient)
        db.session.commit()

        # Return success message with patient ID
        return jsonify({'success': True, 'message': 'Patient registered successfully', 'patient_id': new_patient.patient_id}), 201

    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@patient_bp.route('/patients', methods=['GET'])
def get_patients():
    patients = Patients.query.all()
    patients_data = [
        {
            "id": patient.patient_id,
            "name": patient.name,
            "email": patient.email,
            "age": patient.age,
            "gender": patient.gender,
            "created_at": patient.created_at
        }
        for patient in patients
    ]
    return jsonify(patients_data)


@patient_bp.route('/check_patient/<patient_id>', methods=['GET'])
def check_patient(patient_id):
    try:
        # print(patient_id)
        # Query your database for the patient_id
        patient = Patients.query.filter_by(patient_id=patient_id).first()
        print(patient)
        if patient:
            return jsonify({"exists": True}), 200
        else:
            return jsonify({"exists": False}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500