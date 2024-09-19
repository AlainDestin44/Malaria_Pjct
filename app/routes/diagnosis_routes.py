# Placeholder for your Flask app routes
from flask import Flask, render_template,Blueprint, request, session, redirect, url_for,flash,jsonify
from app.db import *
from werkzeug.utils import secure_filename
from app.utils.helpers import aggregate_and_assess_severity,TempStorage,allowed_file,process_patient_images
from app.utils.Updated_Helpers import process_images
import uuid

import os
from pathlib import Path
from collections import defaultdict
import numpy as np
from app.config import Config

configObj=Config()


diagnosis_bp = Blueprint('diagnosis_bp', __name__)
# Global dictionary to act as an in-memory database
uploaded_files_db = {}

# ---------------testing
# In-memory temporary dictionary to hold the uploaded images
temporary_storage = {}
# Define the allowed image file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = '/Users/alaindestinkarasira/Documents/MALARIA/Malaria_Pjct/MalariaDiagnosis/app/uploads'  # Set this in config
# Route to handle the image uploads
temp_files = {} 
# Route for uploading images temporarily (stored in temporary_storage)
@diagnosis_bp.route('/uploads', methods=['POST'])
def uploads():
    patient_id = request.form.get('id')
    file = request.files.get('image')

    if file and allowed_file(file.filename):
        if patient_id not in temporary_storage:
            temporary_storage[patient_id] = []

        # Store the file's content (binary data) in the temporary storage dictionary
        filename = secure_filename(file.filename)
        file_content = file.read()

        # Append the file data to the patient's list of images
        temporary_storage[patient_id].append({
            'filename': filename,
            'content': file_content
        })

        return jsonify({
            'success': True,
            'message': f'Image {filename} uploaded temporarily!',
            'uploaded_files': [f['filename'] for f in temporary_storage[patient_id]]
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid file format or no file uploaded!'
        }), 400

# Route for saving all images to disk from the temporary dictionary
@diagnosis_bp.route('/save_all', methods=['POST'])
def save_all():
    patient_id = request.form.get('id')

    if patient_id not in temporary_storage or len(temporary_storage[patient_id]) == 0:
        return jsonify({
            'success': False,
            'message': 'No images to save!'
        }), 400

    # Save images to the final disk location
    for file_data in temporary_storage[patient_id]:
        filename = file_data['filename']
        file_content = file_data['content']
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        newImage=PatientImages(patient_id=patient_id,image_path=file_path)
        db.session.add(newImage)
        db.session.commit()
        
        # Save the binary data to disk
        with open(file_path, 'wb') as f:
            f.write(file_content)
   
    patientInstance=DiagnosisReport(patient_id=patient_id,detected_parasites=None)
    db.session.add(patientInstance)  
    db.session.commit()

    # Once saved, clear the temporary storage for this patient
    del temporary_storage[patient_id]

    return jsonify({
        'success': True,
        'message': 'All images saved successfully!',
        'saved_files': os.listdir(UPLOAD_FOLDER)
    }), 200

# Route for resetting (clearing the temporary dictionary for a patient)
@diagnosis_bp.route('/reset', methods=['POST'])
def reset():
    patient_id = request.form.get('id')

    if patient_id in temporary_storage:
        # Clear the temporary storage for this patient
        del temporary_storage[patient_id]

    return jsonify({
        'success': True,
        'message': 'Image tracker reset successfully!'
    }), 200
#----------------end testing




# @diagnosis_bp.route('/uploads', methods=['POST'])
# def uploads():
#     # Initialize session if not already done
#     if 'uploaded_files' not in session:
#         session['uploaded_files'] = []
#         print("God help me to know a lot as possible but i want to master data engineering concepts")

    # # Handle POST request
    # if request.method == 'POST':
    #     # Check if the ID is provided
    #     if 'id' not in request.form or not request.form['id']:
    #         return jsonify({'success': False, 'message': 'Please enter an ID.'})
        
    #     user_id = request.form['id']

    #     # Validate if the image is being uploaded
    #     if 'upload_image' in request.form:
    #         # Check if a file is provided
    #         if 'image' not in request.files:
    #             return jsonify({'success': False, 'message': 'No file part'})

    #         file = request.files['image']
    #         if file.filename == '':
    #             return jsonify({'success': False, 'message': 'No selected file'})

    #         # Restrict the number of uploaded images to a maximum of 5
    #         if len(session['uploaded_files']) >= 5:
    #             return jsonify({'success': False, 'message': 'Maximum upload limit reached.'})

    #         # Save the file
    #         file_number = len(session['uploaded_files']) + 1
    #         filename = f"{user_id}_{file_number:03d}.jpg"
    #         file.save(os.path.join(configObj.UPLOAD_FOLDER, filename))

    #         # Track uploaded files in session
    #         session['uploaded_files'].append(filename)
    #         session.modified = True

    #         return jsonify({'success': True, 'uploaded_files': session['uploaded_files']})

    #     elif 'save_images' in request.form:
    #         # Handle saving all images
    #         if len(session['uploaded_files']) == 5:
    #             flash(f"All images successfully saved: {', '.join(session['uploaded_files'])}")
    #             # Clear the session after saving the images
    #             session.pop('uploaded_files', None)

    #             return jsonify({'success': True, 'message': 'All images saved successfully!'})
    #         else:
    #             return jsonify({'success': False, 'message': 'You must upload 5 images before saving.'})

    # return jsonify({'success': False, 'message': 'Invalid request'})



    # if request.method == 'POST':
    #     print(request.url)
    # return f"God I need you {request.url}"

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
                # db.session.commit()

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
from datetime import date

# API route to get all diagnoses
# @diagnosis_bp.route('/diagnosis_report', methods=['GET'])
# def diagnosis_report():
#     diagnoses = DiagnosisReport.query.all()
#         # Fetch all diagnoses from the database

#     # Convert each diagnosis to a dictionary
#     diagnosis_list = [diagnosis.to_dict() for diagnosis in diagnoses]

#     # Return as JSON
#     return jsonify(diagnosis_list)
    # print(diagnoses[0].status)
    # return 'God is able to do, just what he said he will do!!!'
@diagnosis_bp.route('/diagnosis_report', methods=['GET'])
def get_all_diagnoses():
    
    # today = date.today()
    diagnoses = DiagnosisReport.query.all()
    diagnosis_list = [
        {
            'id': d.id,
            'patient_id': d.patient_id,
            'date': date.today(),
            'status': d.status
        } for d in diagnoses
    ]
    return jsonify({'diagnoses': diagnosis_list})
MODEL_PATH = '/Users/alaindestinkarasira/Documents/MALARIA/Malaria_Pjct/MalariaDiagnosis/app/models/new_best.onnx'

@diagnosis_bp.route('/get_all_patients', methods=['GET'])
def get_all_patients():
    patient = Patients.query.all()
    patient_list = [
        {
            
            'Name': d.name,
            'patient_id': d.patient_id,
            'age':d.age,
            'email':d.email,
            'gender':d.gender,
        } for d in patient
    ]
    return jsonify({'patients': patient_list})

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
        # print (files[0])
        if not files:
            return f"No data found for User ID: {user_id}.", 404

        db_contents = f"User ID: {user_id}<br>"
        db_contents += "Uploaded Files:<br>"
        for file in files:
            image_paths.append(file.image_path)
            # print (file.image_path)
        # print(image_paths)
        results= process_images(MODEL_PATH,image_paths)
        # print(results)
        # # Create a temporary storage instance
        # temp_storage = TempStorage()

        # # Process the images for the given patient
        # process_patient_images(user_id, image_paths, temp_storage)

        # # Aggregate results and assess severity
        # aggregated_results= aggregate_and_assess_severity(
        #     temp_storage.get_patient_detections(user_id), 0.1
        # )
        # # Construct the response with patient ID, parasite detected, probability, severity
        # response_data = {
        #     "patient_id": user_id,
        #     "detected_parasites": []
        # }

        # # Iterate through the aggregated results and add each parasite's details
        # response_data = {
        #     "detected_parasites": [],
        #     "total_wbc_count": aggregated_results["total_wbc_count"],
        #     "adjusted_parasite_density": aggregated_results["adjusted_parasite_density"],
        #     "severity": aggregated_results["severity"]
        # }

        # Fill in detected parasites
        # for parasite in aggregated_results["detected_parasites"]:
        #     response_data["detected_parasites"].append({
        #         "parasite_name": parasite["parasite_name"],
        #         "count": parasite["count"],
        #         "average_confidence": parasite["average_confidence"]
        #     })

        # Log the results
        # print(f"Aggregated Instances: {aggregated_results['instances']}")
        # print(f"Aggregated Instances: {response_data}")
        # Update the status in the diagnosis_report table
        diagnosis_record = DiagnosisReport.query.filter_by(patient_id=user_id).first()
        if diagnosis_record:
            diagnosis_record.status = 'completed'
            diagnosis_record.detected_parasites=results
            db.session.commit()

        # newpt= PatientDiagnosis(user_id,aggregated_results)

        
        # db.session.add(newpt)
        # db.session.commit()
        # Return the results as a JSON response
         # Return the response as a JSON object
        return jsonify(results)
    except Exception as e:
        # Log any exceptions that occur
        print(f"Error processing images: {str(e)}")
        # print (image_paths)
        return jsonify({'error': str(e)}), 500
    

@diagnosis_bp.route('/get_result/<string:id>', methods=['GET'])
def get_result(id):
    print("God I want to excel in data engineering")
    try:
        patient_id = id

        # Query the DiagnosisReport table for the given patient_id
        report = DiagnosisReport.query.filter_by(patient_id=patient_id).first()

        if report:
            # Assuming `report.detected_parasites` is an object, extract necessary fields
            detected_parasites = report.detected_parasites
            print (detected_parasites)
            # Prepare the response data with proper serialization
            response_data = {
                "total_wbcs": detected_parasites['total_wbcs'] if detected_parasites else None,
                "parasite_density": detected_parasites['parasite_density'] if detected_parasites else None,
                "severity": detected_parasites['severity'] if detected_parasites else None,
                "total_parasites":detected_parasites['total_parasites'] if detected_parasites else None,
                "dominant_parasite": detected_parasites['dominant_parasite'] if detected_parasites else None,
                "dominant_confidence": detected_parasites['dominant_confidence'] if detected_parasites else None,
                "image_results": detected_parasites['image_results'] if detected_parasites else [],
                # "created_at": detected_parasites['created_at']  # Add other fields as needed
            }

            print(response_data)  # Debugging statement to check the data
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "No report found for the given patient ID."}), 404

    except Exception as e:
        # Log the error (if logging is configured)
        print(f"Error: {str(e)}")  # Debugging statement to trace the issue
        return jsonify({"error": str(e)}), 500

@diagnosis_bp.route('/')
def index():
    return render_template('dashboard.html')





