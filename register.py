import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt
import login

def show_registration():
    register_window = tk.Toplevel()
    register_window.title("User Registration")
    register_window.geometry("400x400")

    tk.Label(register_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(register_window)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack(pady=5)

    tk.Label(register_window, text="Confirm Password:").pack(pady=5)
    confirm_password_entry = tk.Entry(register_window, show="*")
    confirm_password_entry.pack(pady=5)

    tk.Label(register_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(register_window)
    email_entry.pack(pady=5)

    def register():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        email = email_entry.get()

        if not username or not password or not confirm_password or not email:
            messagebox.showerror("Error", "All fields are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO User (username, password_hash, email) VALUES (?, ?, ?)",
                           (username, hashed_password, email))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            register_window.destroy()
            login.show_user_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or Email already exists")

        conn.close()

    tk.Button(register_window, text="Register", command=register).pack(pady=10)
