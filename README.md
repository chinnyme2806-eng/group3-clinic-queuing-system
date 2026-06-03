# Clinic Queuing System

A desktop-based clinic queue management application built with Python and Tkinter. It allows clinic staff to manage patient records, track queue statuses, and persist data using a local JSON file.

---

## Features

- Add new patients with ID, name, age, sex, and condition
- View all patients in a sortable table
- Update patient queue status (Waiting, In Progress, Done)
- Update patient queue info (name, age, sex, condition)
- Delete patients from the queue
- Persistent storage via JSON — data is saved and reloaded on every launch
- Duplicate patient ID detection

---

## Built With

- **Python 3** — core programming language
- **Tkinter** — GUI framework (bundled with Python)
- **JSON** — local flat-file data storage

---

## Requirements

- Python 3.x
- Tkinter (included by default with most Python installations)

No third-party packages required.

---

## Installation & Setup

1. Make sure Python 3 is installed on your machine.
2. Clone or download the project files into a folder.
3. No additional dependencies need to be installed.

---

## Usage

Run the application from your terminal:

```bash
python clinic_main.py
```

> **Note:** Always run `clinic_main.py`, not `queue_data.py`. Running `queue_data.py` directly will not open any window — it is the backend module only.

Once open, you can:
- Fill in the form fields and click **Add Patient** to register a patient
- Select a row in the table and use the dropdown to **Update Status**
- Select a row in the table and click **Update Info** and a fill in the form fields and click **Save Changes** or **Cancel**
- Select a row and click **Delete Patient** to remove them from the queue

---

## Project Structure

```
clinic-queuing-system/
│
├── clinic_main.py       # Frontend — Tkinter GUI
├── queue_data.py        # Backend — data logic and JSON operations
├── patient_list.json    # Local data storage (auto-created if missing)
└── README.md
```

---

## Patient Status Values

| Status        | Description                        |
|---------------|------------------------------------|
| `waiting`     | Patient is in the queue            |
| `in_progress` | Patient is currently being seen    |
| `done`        | Patient has been attended to       |

---

## Authors

| Role             | Name             |
|------------------|------------------|
| Project Manager  | Chinnyme Adizas  |
| Backend          | Jhomar Tañeza    |
| Frontend         | Benj Kleyton Yu  |
| QA               | Mae Joy Marcos   |
| Client           | Genica Lacandazo |


---

## License

This project was developed for academic purposes. All rights reserved by the project team. 2026
