import tkinter as tk
from tkinter import ttk
import booking
import reviews
import staff_management  # For managing users & bookings
import movie_management  # For movie management
import analytics  # For reports & analytics

def user_dashboard(username):
    """Displays the user dashboard with a modern UI."""
    root = tk.Toplevel()
    root.title("User Dashboard")
    root.geometry("600x500")
    root.configure(bg="#2C3E50")  # Dark background color

    # Title Label
    ttk.Label(root, text=f"Welcome, {username}", font=("Arial", 18, "bold"), foreground="white", background="#2C3E50").pack(pady=15)

    # Styling the buttons
    button_style = {"width": 25, "padding": 5}

    ttk.Button(root, text="Search Movies", **button_style, command=movie_management.show_movie_management).pack(pady=5)
    ttk.Button(root, text="Book Tickets", **button_style, command=lambda: booking.show_booking(username)).pack(pady=5)
    ttk.Button(root, text="My Bookings", **button_style, command=lambda: booking.view_user_bookings(username)).pack(pady=5)
    ttk.Button(root, text="Rate & Review Movies", **button_style, command=lambda: reviews.show_review_screen(username)).pack(pady=5)
    
    # Logout Button
    ttk.Button(root, text="Logout", style="Danger.TButton", command=root.destroy).pack(pady=20)

    root.mainloop()

def staff_dashboard(username):
    """Displays the staff dashboard with a modern UI."""
    root = tk.Toplevel()
    root.title("Staff Dashboard")
    root.geometry("600x500")
    root.configure(bg="#34495E")

    # Title Label
    ttk.Label(root, text=f"Welcome, {username} (Staff)", font=("Arial", 18, "bold"), foreground="white", background="#34495E").pack(pady=15)

    # Styling the buttons
    button_style = {"width": 25, "padding": 5}

    ttk.Button(root, text="Manage Users", **button_style, command=staff_management.show_user_management).pack(pady=5)
    ttk.Button(root, text="Manage Movies", **button_style, command=movie_management.show_movie_management).pack(pady=5)
    ttk.Button(root, text="Manage Bookings", **button_style, command=staff_management.show_booking_management).pack(pady=5)
    ttk.Button(root, text="View Analytics", **button_style, command=analytics.generate_sales_report).pack(pady=5)
    
    # Logout Button
    ttk.Button(root, text="Logout", style="Danger.TButton", command=root.destroy).pack(pady=20)

    root.mainloop()