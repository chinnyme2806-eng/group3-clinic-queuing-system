import queue_data as db

def display_menu():
    """Display the main menu options."""
    print("\n===== CLINIC QUEUING SYSTEM =====")
    print("1. Add Patient")
    print("2. View Patient List")
    print("3. Update Patient Info / Status")
    print("4. Delete Patient")
    print("5. Exit")
    print("=================================")

def add_patient():
    """Prompt for patient details and add to queue. Auto-return to menu."""
    print("\n--- Add New Patient ---")
    try:
        # --- Patient ID ---
        while True:
            try:
                pid = int(input("Patient ID: "))
                if pid <= 0:
                    print("ID must be a positive integer.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter an integer ID.")

        # Check if ID already exists (friendly error)
        existing = db.get_patient_by_id(pid)
        if existing:
            print(f"Error: Patient with ID {pid} already exists. Returning to menu.")
            return

        # --- Name ---
        while True:
            name = input("Name: ").strip()
            if name:
                break
            print("Name cannot be empty.")

        # --- Age ---
        while True:
            try:
                age = int(input("Age: "))
                if age <= 0:
                    print("Age must be a positive integer.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid age (integer).")

        # --- Sex ---
        while True:
            sex = input("Sex (m/f): ").strip().lower()
            if sex in ('m', 'f'):
                break
            print("Please enter 'm' or 'f'.")

        # --- Condition ---
        while True:
            condition = input("Condition: ").strip()
            if condition:
                break
            print("Condition cannot be empty.")

        # Build patient dictionary – status always 'waiting'
        patient = {
            "id": pid,
            "name": name,
            "age": age,
            "sex": sex,
            "condition": condition,
            "status": "waiting"
        }

        db.add_patient(patient)
        print("Patient added successfully with status 'waiting'.")
        # Automatically returns to main menu (no extra prompt)

    except ValueError as ve:
        # Catch any unexpected ValueErrors (e.g., from db.add_patient)
        print(f"Error: {ve}")

def view_patients():
    """Display all patients in a formatted list, then wait for Enter."""
    patients = db.get_all_patients()
    print("\n--- Patient Queue ---")
    if not patients:
        print("No patients in the queue.")
    else:
        # Simple table header
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Sex':<5} {'Condition':<15} {'Status':<12}")
        print("-" * 70)
        for p in patients:
            print(f"{p['id']:<5} {p['name']:<20} {p['age']:<5} {p['sex']:<5} {p['condition']:<15} {p['status']:<12}")
    input("\nPress Enter to return to the main menu...")

def update_patient():
    """Search patient by ID, then offer sub-menu to update info or status."""
    while True:
        try:
            pid_str = input("\nEnter Patient ID to update (or leave blank to go back): ").strip()
            if pid_str == "":
                return  # back to main menu
            pid = int(pid_str)
        except ValueError:
            print("Invalid ID. Please enter a number.")
            continue

        patient = db.get_patient_by_id(pid)
        if not patient:
            print(f"No patient found with ID {pid}.")
            continue
            # 'continue' makes the loop start again
        # Display current patient info
        print("\nCurrent patient details:")
        print(f"  ID: {patient['id']}")
        print(f"  Name: {patient['name']}")
        print(f"  Age: {patient['age']}")
        print(f"  Sex: {patient['sex']}")
        print(f"  Condition: {patient['condition']}")
        print(f"  Status: {patient['status']}")

        # Sub-menu loop for this patient
        while True:
            print("\n  --- Update Options ---")
            print("  1. Update Patient Info")
            print("  2. Update Status")
            print("  3. Back to Main Menu")
            choice = input("  Enter your choice (1-3): ").strip()

            if choice == '1':
                # Update info (name, age, sex, condition)
                print("\nLeave blank to keep the current value.")
                new_name = input(f"  New name [{patient['name']}]: ").strip()
                if new_name == "":
                    new_name = patient['name']

                while True:
                    new_age_str = input(f"  New age [{patient['age']}]: ").strip()
                    if new_age_str == "":
                        new_age = patient['age']
                        break
                    try:
                        new_age = int(new_age_str)
                        if new_age <= 0:
                            print("Age must be positive.")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid integer.")

                while True:
                    new_sex = input(f"  New sex (m/f) [{patient['sex']}]: ").strip().lower()
                    if new_sex == "":
                        new_sex = patient['sex']
                        break
                    if new_sex in ('m', 'f'):
                        break
                    print("Please enter 'm' or 'f'.")

                new_condition = input(f"  New condition [{patient['condition']}]: ").strip()
                if new_condition == "":
                    new_condition = patient['condition']

                success = db.update_patient_info(pid, new_name, new_age, new_sex, new_condition)
                if success:
                    print("Patient information updated successfully.")
                else:
                    print("Failed to update patient information.")
                # After update, sub-menu will be shown again (back option available)

            elif choice == '2':
                # Update status only
                print("\n  Valid statuses: waiting, in_progress, done")
                new_status = input(f"  New status [{patient['status']}]: ").strip().lower()
                if new_status == "":
                    new_status = patient['status']
                try:
                    success = db.update_patient_status(pid, new_status)
                    if success:
                        print("Patient status updated successfully.")
                except ValueError as ve:
                    print(f"Error: {ve}")
                # Sub-menu reappears

            elif choice == '3':
                break   # exit sub-menu -> back to main menu
            else:
                print("Invalid choice. Please select 1, 2, or 3.")

        # After breaking out of sub-menu, we return to main menu immediately.
        # (No extra prompt needed because '3' itself is the "return" option.)
        break   # exit the outer while loop for patient ID search

def delete_patient():
    """Ask for ID, confirm and delete. Then wait for Enter."""
    while True:
        try:
            pid_str = input("\nEnter Patient ID to delete (or leave blank to go back): ").strip()
            if pid_str == "":
                return
            pid = int(pid_str)
        except ValueError:
            print("Invalid ID. Please enter a number.")
            continue

        patient = db.get_patient_by_id(pid)
        if not patient:
            print(f"No patient found with ID {pid}.")
            continue

        # Confirmation
        confirm = input(f"Are you sure you want to delete {patient['name']} (ID {pid})? (y/n): ").strip().lower()
        if confirm == 'y':
            if db.delete_patient(pid):
                print(f"Patient {patient['name']} deleted successfully.")
            else:
                print("Failed to delete patient.")
            # After deletion, show return-to-menu prompt
            input("\nPress Enter to return to the main menu...")
            break
        else:
            print("Deletion cancelled.")
            # Also give option to return (can just break to menu or loop again)
            # We'll break to main menu for simplicity
            break

def main():
    """Main program loop."""
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()
        if choice == '1':
            add_patient()
        elif choice == '2':
            view_patients()
        elif choice == '3':
            update_patient()
        elif choice == '4':
            delete_patient()
        elif choice == '5':
            print("Exiting Clinic Queuing System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()