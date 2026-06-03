import tkinter as tk
from tkinter import ttk, messagebox
import queue_data  # backend

# ------------------------
# Helper: load patients into table
# ------------------------

def load_patients_into_table():
    tree.delete(*tree.get_children())  # clear table first
    patients = queue_data.get_all_patients()
    for p in patients:
        tree.insert("", tk.END, values=(
            p["id"],
            p["name"],
            p["age"],
            p["sex"],
            p["condition"],
            p["status"]
        ))

# ------------------------
# Functions
# ------------------------

def add_patient():
    try:
        pid = int(id_entry.get())
        age = int(age_entry.get())

        patient = {
            "id": pid,
            "name": name_entry.get(),
            "age": age,
            "sex": sex_var.get(),
            "condition": condition_entry.get(),
            "status": "waiting"
        }

        queue_data.add_patient(patient)  # saves to JSON
        load_patients_into_table()       # refresh table
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Patient added successfully!"
        )

    except ValueError as e:
        error_msg = str(e)
        # Specific error messages from queue_data
        if "already exists" in error_msg:
            messagebox.showerror("Error", error_msg)
        elif "cannot be negative" in error_msg:
            messagebox.showerror("Error", error_msg)
        else:
            # Non-integer input
            messagebox.showerror("Error", "ID and Age must be valid numbers.")

def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    condition_entry.delete(0, tk.END)
    sex_var.set("Male")

def delete_patient():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a patient first."
        )
        return

    item = tree.item(selected[0])
    patient_id = int(item["values"][0])

    queue_data.delete_patient(patient_id)  # removes from JSON
    load_patients_into_table()             # refresh table

def update_status():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a patient."
        )
        return

    item = tree.item(selected[0])
    values = list(item["values"])
    patient_id = int(values[0])
    new_status = status_var.get()

    try:
        queue_data.update_patient_status(patient_id, new_status)  # saves to JSON
        load_patients_into_table()                                # refresh table
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def open_update_window():
    """Open a separate window to update the selected patient's information."""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a patient to update.")
        return

    # Get selected patient data
    item = tree.item(selected[0])
    values = item["values"]
    patient_id = int(values[0])
    current_name = values[1]
    current_age = values[2]
    current_sex = values[3]
    current_condition = values[4]

    # Create a new top-level window
    update_win = tk.Toplevel(root)
    update_win.title(f"Update Patient ID {patient_id}")
    update_win.geometry("400x300")
    update_win.resizable(False, False)

    # Center the window relative to main window
    update_win.transient(root)
    update_win.grab_set()

    # Form fields
    tk.Label(update_win, text="Name:").pack(pady=(10,0))
    name_entry_upd = tk.Entry(update_win, width=30)
    name_entry_upd.insert(0, current_name)
    name_entry_upd.pack(pady=5)

    tk.Label(update_win, text="Age:").pack()
    age_entry_upd = tk.Entry(update_win, width=30)
    age_entry_upd.insert(0, current_age)
    age_entry_upd.pack(pady=5)

    tk.Label(update_win, text="Sex:").pack()
    sex_var_upd = tk.StringVar(value=current_sex)
    sex_combo_upd = ttk.Combobox(update_win, textvariable=sex_var_upd, values=["Male", "Female"], width=28)
    sex_combo_upd.pack(pady=5)

    tk.Label(update_win, text="Condition:").pack()
    condition_entry_upd = tk.Entry(update_win, width=30)
    condition_entry_upd.insert(0, current_condition)
    condition_entry_upd.pack(pady=5)

    def save_update():
        new_name = name_entry_upd.get().strip()
        new_age_str = age_entry_upd.get().strip()
        new_sex = sex_var_upd.get()
        new_condition = condition_entry_upd.get().strip()

        if not new_name or not new_age_str or not new_condition:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            new_age = int(new_age_str)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return

        # Catch negative age error
        try:
            success = queue_data.update_patient_info(patient_id, new_name, new_age, new_sex, new_condition)
            if success:
                load_patients_into_table()
                update_win.destroy()
                messagebox.showinfo("Success", f"Patient ID {patient_id} updated.")
            else:
                messagebox.showerror("Error", f"Patient ID {patient_id} not found.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    tk.Button(update_win, text="Save Changes", command=save_update, bg="#4CAF50", fg="white").pack(pady=20)
    tk.Button(update_win, text="Cancel", command=update_win.destroy).pack()

# ------------------------
# Main Window
# ------------------------

root = tk.Tk()
root.title("Clinic Queuing System")
root.geometry("900x600")

title = tk.Label(
    root,
    text="CLINIC QUEUE SYSTEM",
    font=("Arial", 19, "bold")
)
title.pack(pady=10)

# ------------------------
# Input Frame (Add only)
# ------------------------

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Patient ID").grid(row=0, column=0)
id_entry = tk.Entry(frame)
id_entry.grid(row=0, column=1)

tk.Label(frame, text="Name").grid(row=1, column=0)
name_entry = tk.Entry(frame)
name_entry.grid(row=1, column=1)

tk.Label(frame, text="Age").grid(row=2, column=0)
age_entry = tk.Entry(frame)
age_entry.grid(row=2, column=1)

tk.Label(frame, text="Sex").grid(row=3, column=0)

sex_var = tk.StringVar()
sex_combo = ttk.Combobox(
    frame,
    textvariable=sex_var,
    values=["Male", "Female"]
)
sex_combo.grid(row=3, column=1)
sex_combo.current(0)

tk.Label(frame, text="Condition").grid(row=4, column=0)
condition_entry = tk.Entry(frame)
condition_entry.grid(row=4, column=1)

tk.Button(
    frame,
    text="Add Patient",
    command=add_patient
).grid(row=5, column=0, columnspan=2, pady=10)

# ------------------------
# Table
# ------------------------

columns = (
    "ID",
    "Name",
    "Age",
    "Sex",
    "Condition",
    "Status"
)

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill="both", expand=True, padx=20)

# ------------------------
# Buttons
# ------------------------

bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

status_var = tk.StringVar()

status_combo = ttk.Combobox(
    bottom_frame,
    textvariable=status_var,
    values=["waiting", "in_progress", "done"]
)
status_combo.pack(side="left", padx=5)
status_combo.current(0)

tk.Button(
    bottom_frame,
    text="Update Status",
    command=update_status
).pack(side="left", padx=5)

tk.Button(
    bottom_frame,
    text="Delete Patient",
    command=delete_patient
).pack(side="left", padx=5)

# New button: Update Info (opens separate window)
tk.Button(
    bottom_frame,
    text="Update Info",
    command=open_update_window
).pack(side="left", padx=5)

# Load existing patients from JSON on startup
load_patients_into_table()

root.mainloop()