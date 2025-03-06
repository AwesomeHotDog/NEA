import tkinter as tk
from tkinter import ttk, messagebox
import login
import register
import staff_management
import database
import dashboard

def open_staff_login():
    """Opens the staff login screen."""
    staff_management.initialize_database()
    database.populate_movies()
    login_root = tk.Toplevel()
    login.LoginApp(login_root, is_staff=True)

def open_user_login():
    """Opens the user login screen."""
    staff_management.initialize_database()
    database.populate_movies()
    login_root = tk.Toplevel()
    login.LoginApp(login_root, is_staff=False)

def show_guest_dashboard():
    """Shows the guest dashboard."""
    dashboard.user_dashboard("Guest")

def main():
    root = tk.Tk()
    root.title("Cinema System")
    root.geometry("400x500")
    root.configure(bg="#1A1A1A")  # Darker background

    # Configure styles
    style = ttk.Style()
    style.configure("TLabel", foreground="white", background="#1A1A1A", font=("Helvetica", 12))
    style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10)
    style.configure("Title.TLabel", font=("Montserrat", 24, "bold"))

    # Create main container
    main_frame = tk.Frame(root, bg="#1A1A1A", padx=40, pady=20)
    main_frame.pack(expand=True, fill="both")

    # Title with cinema icon
    title_frame = tk.Frame(main_frame, bg="#1A1A1A")
    title_frame.pack(pady=(0, 30))

    tk.Label(title_frame, 
            text="🎬 Cinema System",
            font=("Montserrat", 24, "bold"),
            fg="#E0E0E0",
            bg="#1A1A1A").pack()

    tk.Label(title_frame,
            text="Book your tickets today",
            font=("Helvetica", 12),
            fg="#BBBBBB",
            bg="#1A1A1A").pack(pady=(5, 0))

    # Button container
    button_frame = tk.Frame(main_frame, bg="#1A1A1A")
    button_frame.pack(expand=True)

    # Common button style
    button_style = {
        "width": 25,
        "height": 2,
        "font": ("Segoe UI", 11, "bold"),
        "border": 0,
        "cursor": "hand2"
    }

    # Staff Login button with icon
    tk.Button(button_frame,
              text="👤 Staff Login",
              command=open_staff_login,
              bg="#2980B9",
              fg="white",
              activebackground="#3498DB",
              activeforeground="white",
              **button_style).pack(pady=10)

    # User Login button with icon
    tk.Button(button_frame,
              text="🔑 User Login",
              command=open_user_login,
              bg="#27AE60",
              fg="white",
              activebackground="#2ECC71",
              activeforeground="white",
              **button_style).pack(pady=10)

    # Guest button with icon
    tk.Button(button_frame,
              text="👋 Continue as Guest",
              command=show_guest_dashboard,
              bg="#7F8C8D",
              fg="white",
              activebackground="#95A5A6",
              activeforeground="white",
              **button_style).pack(pady=10)

    # Footer
    footer_frame = tk.Frame(main_frame, bg="#1A1A1A")
    footer_frame.pack(side="bottom", pady=20)

    tk.Label(footer_frame,
            text="© 2024 Cinema System",
            font=("Helvetica", 9),
            fg="#888888",
            bg="#1A1A1A").pack()

    root.mainloop()

if __name__ == "__main__":
    main()


 