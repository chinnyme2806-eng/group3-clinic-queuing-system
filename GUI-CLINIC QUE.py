import tkinter as tk
from tkinter import ttk, messagebox

patients = []

# ------------------------
# Functions
# ------------------------

def add_patient():
    try:
        pid = int(id_entry.get())
        age = int(age_entry.get())

        patient = (
            pid,
            name_entry.get(),
            age,
            sex_var.get(),
            condition_entry.get(),
            "waiting"
        )

        patients.append(patient)

        tree.insert("", tk.END, values=patient)

        clear_fields()

        messagebox.showinfo(
            "Success",
            "Patient added successfully!"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "ID and Age must be numbers."
        )

def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    condition_entry.delete(0, tk.END)

def delete_patient():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a patient first."
        )
        return

    tree.delete(selected[0])

def update_status():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a patient."
        )
        return

    item = tree.item(selected)

    values = list(item["values"])

    values[5] = status_var.get()

    tree.item(selected, values=values)

# ------------------------
# Main Window
# ------------------------

root = tk.Tk()
root.title("Clinic Queuing System")
root.geometry("900x600")

title = tk.Label(
    root,
    text="CLINIC QUEUING SYSTEM",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

# ------------------------
# Input Frame
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
    values=["waiting", "inprogress", "done"]
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

root.mainloop()