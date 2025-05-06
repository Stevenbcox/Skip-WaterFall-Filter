import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
import hashlib
import subprocess
import main  # Import your main processing script


def check_password():
    username = username_entry.get()
    password = password_entry.get()

    # Hash the entered password for comparison
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Check against stored credentials
    if username == "Steven" and hashed_password == "b4cf157dfe3ea3fc0f4dc60843617f8c90954b4b3b4a9fa38e23e55ef52ec799":
        messagebox.showinfo("Login", "Login successful!")
        login_frame.pack_forget()  # Hide login frame
        main_frame.pack(padx=10, pady=10)  # Show main interface
    else:
        messagebox.showerror("Login", "Incorrect username or password.")


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        file_path_var.set(file_path)


def run_green_run():
    program_path = r"P:\Users\Steven Cox\Projects\RNN filter file\dist\gui\gui.exe"
    try:
        subprocess.Popen(program_path, creationflags=subprocess.CREATE_NO_WINDOW)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Program not found at: {program_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")


def run_ascension():
    program_path = r"P:\Users\Steven Cox\Projects\Verifacts Filter File\dist\gui\gui.exe"
    try:
        subprocess.Popen(program_path, creationflags=subprocess.CREATE_NO_WINDOW)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Program not found at: {program_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")


def start_processing():
    input_file = file_path_var.get()
    min_balance_due = balance_due_var.get()

    if not input_file:
        messagebox.showerror("Error", "Please select an input file.")
        return
    if not min_balance_due:
        messagebox.showerror("Error", "Please select a minimum balance.")
        return

    try:
        min_balance_due = float(min_balance_due)
    except ValueError:
        messagebox.showerror("Error", "Invalid selection for minimum balance.")
        return

    try:
        output_path = main.main(input_file, min_balance_due)
        if output_path:
            messagebox.showinfo("Success", f"Filtering complete. File saved as: {output_path}")
        else:
            messagebox.showwarning("Warning", "Processing completed, but no file path was returned.")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")


# Create the main window with Darkly theme
root = ttk.Window(themename="darkly")
root.title("Der Riese")

# ----------------- Login Frame -----------------
login_frame = ttk.Frame(root)
login_frame.pack(padx=20, pady=20)

username_label = ttk.Label(login_frame, text="Username:")
username_label.pack()
username_entry = ttk.Entry(login_frame)
username_entry.pack()

password_label = ttk.Label(login_frame, text="Password:")
password_label.pack()
password_entry = ttk.Entry(login_frame, show="*")  # Mask password input
password_entry.pack()
password_entry.bind("<Return>", lambda event: check_password())  # Allow pressing Enter to submit login

login_button = ttk.Button(login_frame, text="Login", command=check_password, bootstyle="primary")
login_button.pack(pady=5)

# ----------------- Main Application Frame -----------------
main_frame = ttk.Frame(root)

# File path input
file_path_var = tk.StringVar()
ttk.Label(main_frame, text="Input File:", foreground="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
file_entry = ttk.Entry(main_frame, textvariable=file_path_var, width=30, state="readonly")
file_entry.grid(row=0, column=1, padx=5, pady=5)
ttk.Button(main_frame, text="Browse", command=select_file, bootstyle="primary").grid(row=0, column=2, padx=5, pady=5)

# Minimum balance due dropdown
balance_due_var = tk.StringVar(value="1000")
ttk.Label(main_frame, text="Minimum Balance:", foreground="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
balance_dropdown = ttk.Combobox(main_frame, textvariable=balance_due_var,
                                values=["1000", "1500", "2000", "2500", "3000", "3500", "4000", "4500", "5000"])
balance_dropdown.grid(row=1, column=1, padx=5, pady=5)
balance_dropdown.config(width=18, state="readonly")

# Button row inside a centered frame
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=2, column=0, columnspan=3, pady=10)

ttk.Button(button_frame, text="Ascension", command=run_ascension, bootstyle="info", width=12).pack(side="left", padx=10)
ttk.Button(button_frame, text="Start Processing", command=start_processing, bootstyle="success", width=18).pack(
    side="left", padx=10)
ttk.Button(button_frame, text="Green Run", command=run_green_run, bootstyle="info", width=12).pack(side="left", padx=10)

# ----------------- Run the application -----------------
root.mainloop()
