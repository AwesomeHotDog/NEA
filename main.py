import tkinter as tk
from database import initialize_database 
from database import populate_movies
import login
import register
import tkinter as tk
import login

def open_login():
    initialize_database()  # Ensure database and tables exist
    populate_movies()  # Populate the database with movies
    """Opens the login window for users."""
    login_root = tk.Toplevel()
    login_root.title("User Login")
    login.LoginApp(login_root, is_staff=False)

def open_staff_login():
    """Opens the login window for staff."""
    login_root = tk.Toplevel()
    login_root.title("Staff Login")
    login.LoginApp(login_root, is_staff=True)

def main():
    """Launch the main selection screen."""
    root = tk.Tk()
    root.title("Cinema System - Main Menu")
    root.geometry("400x350")
    root.configure(bg="#252525")  # ✅ Dark theme

    tk.Label(root, text="Welcome to the Cinema System", font=("Montserrat", 14, "bold"), fg="white", bg="#252525").pack(pady=15)

    tk.Button(root, text="User Login", width=20, bg="#3B3B3B", fg="white", font=("Helvetica", 11, "bold"), command=open_login).pack(pady=5)
    tk.Button(root, text="Staff Login", width=20, bg="#3B3B3B", fg="white", font=("Helvetica", 11, "bold"), command=open_staff_login).pack(pady=5)
    tk.Button(root, text="Exit", width=20, bg="#3B3B3B", fg="white", font=("Helvetica", 11, "bold"), command=root.destroy).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()


 