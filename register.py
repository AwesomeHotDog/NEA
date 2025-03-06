import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import bcrypt

class RegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("400x400")
        self.root.configure(bg="#1A1A1A")

        ttk.Label(root, text="Register", font=("Arial", 18, "bold"), foreground="white", background="#1A1A1A").pack(pady=10)

        ttk.Label(root, text="Username:", foreground="white", background="#1A1A1A").pack()
        self.username_entry = ttk.Entry(root, width=30)
        self.username_entry.pack(pady=5)

        ttk.Label(root, text="Password:", foreground="white", background="#1A1A1A").pack()
        self.password_entry = ttk.Entry(root, width=30, show="*")
        self.password_entry.pack(pady=5)

        ttk.Label(root, text="Confirm Password:", foreground="white", background="#1A1A1A").pack()
        self.confirm_password_entry = ttk.Entry(root, width=30, show="*")
        self.confirm_password_entry.pack(pady=5)

        ttk.Label(root, text="Email:", foreground="white", background="#1A1A1A").pack()
        self.email_entry = ttk.Entry(root, width=30)
        self.email_entry.pack(pady=5)

        ttk.Button(root, text="Register", command=self.register_user).pack(pady=10)

    def register_user(self):
        """Handles user registration with validation."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        email = self.email_entry.get()

        if not username or not password or not confirm_password or not email:
            messagebox.showerror("Error", "All fields are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO User (username, password, email, is_staff) VALUES (?, ?, ?, ?)",
                           (username, password, email, 0))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.root.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or Email already exists")
        finally:
            conn.close()
