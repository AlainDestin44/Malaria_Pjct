// modal-handlers.js

// Show the 'Upload Image' modal when the 'New Diagnosis' button is clicked
document.getElementById('new-diagnosis-btn').addEventListener('click', function () {
    $('#uploadImageModal').modal('show');  // Trigger the modal using jQuery
});

// Show the 'Register Patient' modal when the 'Add New Patient' button is clicked
document.getElementById('add-patient-btn').addEventListener('click', function () {
    $('#registerPatientModal').modal('show');  // Trigger the modal using jQuery
});

// Function to add a new patient via the backend API
document.getElementById('registerPatientForm').addEventListener('submit', function (e) {
    e.preventDefault();  // Prevent the default form submission

    // Collect form data
    const patientData = {
        name: document.getElementById('patientName').value,
        email: document.getElementById('patientEmail').value,
        age: document.getElementById('patientAge').value,
        gender: document.querySelector('input[name="gender"]:checked').value,
    };
    console.log(patientData);

    // Send AJAX request to Flask backend
    fetch('http://127.0.0.1:5002/register_patient', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(patientData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data);  // Log response for debugging
        if (data.success) {
            alert('Patient registered successfully! ID: ' + data.patient_id);
            // Optionally clear the form or close the modal
            document.getElementById('registerPatientForm').reset();
            $('#registerPatientModal').modal('hide');
        } else {
            alert('Failed to register patient: ' + (data.error || 'Unknown error.'));
        }
    })
    .catch(error => console.error('Error:', error));
});
// Function to upload diagnosis images
document.getElementById('uploadImageForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append('patientId', document.getElementById('patientId').value);
    
    const files = document.getElementById('diagnosisImages').files;
    for (let i = 0; i < files.length; i++) {
        formData.append('images', files[i]);
    }

    // Send the images to the Flask backend
    fetch('/api/diagnoses', {
        method: 'POST',
        body: formData  // FormData allows file uploads
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Diagnosis images uploaded successfully!');
            document.getElementById('uploadImageForm').reset();
            $('#uploadImageModal').modal('hide');
        } else {
            alert('Failed to upload diagnosis images.');
        }
    })
    .catch(error => console.error('Error:', error));
});
