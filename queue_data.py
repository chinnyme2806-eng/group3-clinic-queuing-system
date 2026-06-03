import json
import os

DATA_FILE = "patient_list.json"


def load_data():
    """
    Load patient data from the JSON file.
    Returns a list of patient dictionaries.
    If the file doesn't exist or is corrupted, returns an empty list.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            # Ensure the loaded data is a list
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, IOError):
        # If file is empty or corrupted, start fresh
        return []

def save_data(data):
    """
    Save a list of patient dictionaries to the JSON file.
    """
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def add_patient(patient):
    """
    Add a new patient to the queue.
    Raises ValueError if a patient with the same ID already exists.
    Or if age is negative.
    """
    data = load_data()
    # Check for duplicate ID
    for p in data:
        if p['id'] == patient['id']:
            raise ValueError(f"Patient with ID {patient['id']} already exists.")
    # Validate ID
    if patient['id'] < 0:
        raise ValueError("Patient ID cannot be negative.")
    # Validate age
    if patient['age'] < 0:
        raise ValueError("Age cannot be negative.")

    data.append(patient)
    save_data(data)

def get_all_patients():
    """Return a list of all patients in the queue."""
    return load_data()

def get_patient_by_id(patient_id):
    """
    Return the patient dictionary for the given ID,
    or None if not found.
    """
    data = load_data()
    for p in data:
        if p['id'] == patient_id:
            return p
    return None

def update_patient_info(patient_id, name, age, sex, condition):
    """
    Update the information fields of a patient (not the status).
    Returns True if the patient was found and updated, False otherwise.
    Raises ValueError if age is negative.
    """
    if age < 0:
        raise ValueError("Age cannot be negative.")
    data = load_data()
    for p in data:
        if p['id'] == patient_id:
            p['name'] = name
            p['age'] = age
            p['sex'] = sex
            p['condition'] = condition
            save_data(data)
            return True
    return False

def update_patient_status(patient_id, new_status):
    """
    Update the status of a patient.
    Valid statuses: 'waiting', 'in_progress', 'done'.
    Returns True if updated, False if patient not found.
    Raises ValueError if the status is invalid.
    """
    valid_statuses = ['waiting', 'in_progress', 'done']
    if new_status not in valid_statuses:
        raise ValueError(f"Invalid status. Choose from {valid_statuses}.")
    data = load_data()
    for p in data:
        if p['id'] == patient_id:
            p['status'] = new_status
            save_data(data)
            return True
    return False

def delete_patient(patient_id):
    """
    Delete a patient by ID.
    Returns True if the patient was deleted, False if not found.
    """
    data = load_data()
    for i, p in enumerate(data):
        if p['id'] == patient_id:
            del data[i]
            save_data(data)
            return True
    return False
