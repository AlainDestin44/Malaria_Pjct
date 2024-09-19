// section-switching.js

// Show the Dashboard section
document.getElementById('dashboard-link').addEventListener('click', function () {
    document.getElementById('dashboard-section').style.display = 'block';
    document.getElementById('patient-management-section').style.display = 'none';
    document.getElementById('diagnosis-section').style.display = 'none';
});

// Show the Patient Management section
document.getElementById('patient-management-link').addEventListener('click', function () {
    document.getElementById('dashboard-section').style.display = 'none';
    document.getElementById('patient-management-section').style.display = 'block';
    document.getElementById('diagnosis-section').style.display = 'none';
});

// Show the Diagnosis Module section
document.getElementById('diagnosis-link').addEventListener('click', function () {
    document.getElementById('dashboard-section').style.display = 'none';
    document.getElementById('patient-management-section').style.display = 'none';
    document.getElementById('diagnosis-section').style.display = 'block';
});