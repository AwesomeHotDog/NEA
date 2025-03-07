import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import bcrypt
import dashboard

class LoginApp:
    def __init__(self, root, is_staff=False):
        self.root = root
        self.root.title("Staff Login" if is_staff else "User Login")
        self.root.geometry("400x400")
        self.root.configure(bg="#2A2A2A")  # Dark gray background

        # Apply modern styles
        self.style = ttk.Style()
        self.style.configure("TLabel", foreground="white", background="#2A2A2A", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
        self.style.configure("TEntry", padding=5)

        ttk.Label(root, text="Login", font=("Montserrat", 18, "bold"), foreground="white", background="#2A2A2A").pack(pady=10)

        ttk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(root, width=30)
        self.username_entry.pack(pady=5)

        ttk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Ensure the buttons are packed correctly
        self.login_button = ttk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        # Show Register button ONLY if it's a User login
        if not is_staff:
            self.register_button = ttk.Button(root, text="Register", command=self.open_register)
            self.register_button.pack(pady=5)

    def open_register(self):
        """Opens the registration window for users."""
        from register import RegisterApp  
        register_root = tk.Toplevel(self.root)
        RegisterApp(register_root)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()

        # First, check if the user is a staff member
        cursor.execute("SELECT password_hash, role FROM Staff WHERE username=?", (username,))
        result = cursor.fetchone()

        if result:
            stored_hash, role = result
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8') if isinstance(stored_hash, str) else stored_hash):
                messagebox.showinfo("Success", "Login successful!")
                self.root.destroy()
                if role == "admin":
                    dashboard.staff_dashboard(username)
                else:
                    dashboard.user_dashboard(username)
                return
        
        # If not found in Staff, check in the User table
        cursor.execute("SELECT password FROM User WHERE username=?", (username,))
        result = cursor.fetchone()
    
        conn.close()

        if result:
            stored_password = result[0]
            if password == stored_password:  # Plain text comparison for regular users
                messagebox.showinfo("Success", "Login successful!")
                self.root.destroy()
                dashboard.user_dashboard(username)
                return
        
        messagebox.showerror("Error", "Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
