# Placeholder for your Flask app routes
from flask import Flask, render_template,Blueprint, request, session, redirect, url_for,flash,jsonify
from app.db import *
from werkzeug.utils import secure_filename
from app.utils.helpers import aggregate_and_assess_severity,TempStorage,allowed_file,process_patient_images

import os
from pathlib import Path
from collections import defaultdict
import numpy as np
from app.config import Config

configObj=Config()


diagnosis_bp = Blueprint('diagnosis_bp', __name__)
# Global dictionary to act as an in-memory database
uploaded_files_db = {}


@diagnosis_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'uploaded_files' not in session:
        session['uploaded_files'] = []

    if request.method == 'POST':
        # Check if the ID is provided
        if 'id' not in request.form or not request.form['id']:
            flash('Please enter an ID.')
            return redirect(request.url)
        
        user_id = request.form['id']
                # Initialize the list for the user ID if it doesn't exist in the global dictionary
        if user_id not in uploaded_files_db:
            uploaded_files_db[user_id] = []

        if 'upload_image' in request.form:
            # Handle the image upload process
            if 'image' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['image']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                # Generate a custom filename using the provided ID
                file_number = len(session['uploaded_files']) + 1
                filename = f"{user_id}_{file_number:03d}.jpg"
                filename = secure_filename(filename)
                file_path = os.path.join(configObj.UPLOAD_FOLDER, filename)

                
                # Save the file immediately to the upload folder
                file.save(os.path.join(configObj.UPLOAD_FOLDER, filename))
            # Track the filename in the global dictionary under the specific user ID
                uploaded_files_db[user_id].append(filename)
                newImage=PatientImages(patient_id=user_id,image_path=file_path)
                # new_file = UploadedFile(user_id=user_id, filename=file_path )
                db.session.add(newImage)
                db.session.commit()

                # Track the filename in the session
                session['uploaded_files'].append(filename)
                session.modified = True

                if len(session['uploaded_files']) >= configObj.MAX_IMAGES:
                    flash('You have reached the upload limit of 5 images.')
                else:
                    flash(f'Image {len(session["uploaded_files"])} uploaded. Please upload more.')

        elif 'save_images' in request.form:
            # Handle saving the images (since they are already saved, we just clear the session)
            if len(session['uploaded_files']) == configObj.MAX_IMAGES:
                # Flash the uploaded file names
                flash(f"All images successfully saved: {', '.join(session['uploaded_files'])}")
                
                # Clear the session after saving the images
                session.pop('uploaded_files', None)
                
                patientInstance=DiagnosisReport(patient_id=user_id,detected_parasites=None)
                db.session.add(patientInstance)
                db.session.commit()
                # Optionally, clear the user ID
                flash('ID has been cleared.')
                return redirect(url_for('diagnosis_bp.upload'))

        return redirect(request.url)

    # Fetch all diagnoses for the table display
    diagnoses = DiagnosisReport.query.all()
    return render_template('upload.html', 
                           diagnoses=diagnoses,
                           uploaded_files=session.get('uploaded_files'),
                           max_images=configObj.MAX_IMAGES)
# @app.route('/process_diagnosis/<string:id>', methods=['GET','POST'])
# def process_diagnosis(id):

@diagnosis_bp.route('/process_diagnosis/<string:id>', methods=['GET','POST'])
def process_diagnosis(id):
    image_paths=[]
    try:
        # Hardcoded patient ID and image folder path
        user_id = id
        # Log the received request and paths
        print(f"Processing images for patient ID: {user_id}")
        # Create a list to hold image paths

        files = PatientImages.query.filter_by(patient_id=id).all()
        if not files:
            return f"No data found for User ID: {user_id}.", 404

        db_contents = f"User ID: {user_id}<br>"
        db_contents += "Uploaded Files:<br>"
        for file in files:
            image_paths.append(file.image_path)

        # Create a temporary storage instance
        temp_storage = TempStorage()

        # Process the images for the given patient
        process_patient_images(user_id, image_paths, temp_storage)

        # Aggregate results and assess severity
        aggregated_results= aggregate_and_assess_severity(
            temp_storage.get_patient_detections(user_id), 2
        )
        # Construct the response with patient ID, parasite detected, probability, severity
        response_data = {
            "patient_id": user_id,
            "detected_parasites": []
        }

        # Iterate through the aggregated results and add each parasite's details
        for parasite_type, data in aggregated_results.items():
            response_data["detected_parasites"].append({
                "parasite_name": parasite_type,
                "severity_level": data["severity_level"],
                "count": data["count"],
                "average_confidence": data["average_confidence"]
            })

        # Log the results
        # print(f"Aggregated Instances: {aggregated_results['instances']}")
        print(f"Aggregated Instances: {aggregated_results}")
        # Update the status in the diagnosis_report table
        diagnosis_record = DiagnosisReport.query.filter_by(patient_id=user_id).first()
        if diagnosis_record:
            diagnosis_record.status = 'completed'
            diagnosis_record.detected_parasites=aggregated_results
            db.session.commit()

        # newpt= PatientDiagnosis(user_id,aggregated_results)

        
        # db.session.add(newpt)
        # db.session.commit()
        # Return the results as a JSON response
         # Return the response as a JSON object
        return jsonify(response_data)
    except Exception as e:
        # Log any exceptions that occur
        print(f"Error processing images: {str(e)}")
        print (image_paths)
        return jsonify({'error': str(e)}), 500
    

@diagnosis_bp.route('/get_result/<string:id>', methods=['GET'])
def get_result(id):
    try:
        patient_id=id
        # Query the DiagnosisReport table for the given patient_id
        report = DiagnosisReport.query.filter_by(patient_id=patient_id).first()

        if report:
            # Prepare the response data
            response_data = {
                "patient_id": report.patient_id,
                "detected_parasites": report.detected_parasites,  # Assuming this is a JSON or list
                "status": report.status,
                # "created_at": report.created_at  # Add any additional fields you need
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "No report found for the given patient ID."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
