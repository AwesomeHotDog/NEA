import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox
import dashboard

def show_user_login():
    """Displays the user login screen."""
    login_window = tk.Toplevel()
    login_window.title("User Login")
    login_window.geometry("400x300")

    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM User WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            dashboard.user_dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    tk.Button(login_window, text="Login", command=login).pack(pady=10)

def show_staff_login():
    """Displays the staff login screen."""
    login_window = tk.Toplevel()
    login_window.title("Staff Login")
    login_window.geometry("400x300")

    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash, role FROM Staff WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stored_hash, role = result
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                messagebox.showinfo("Success", f"Welcome {username} ({role})!")
                login_window.destroy()
                dashboard.staff_dashboard(username)
            else:
                messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    tk.Button(login_window, text="Login", command=login).pack(pady=10)
