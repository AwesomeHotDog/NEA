import tkinter as tk
from tkinter import ttk
import booking
import reviews
import staff_management  # For managing users & bookings
import movie_management  # For movie management
import showtime_management  # For managing showtimes

def show_dashboard(username, is_staff=False):
    """Shows the main dashboard window."""
    root = tk.Tk()
    root.title("Cinema Dashboard")
    root.geometry("400x500")
    root.configure(bg="#2A2A2A")  # Dark theme

    # Welcome message
    tk.Label(root, text=f"Welcome, {username}!", font=("Arial", 16, "bold"), fg="white", bg="#2A2A2A").pack(pady=20)

    # Button style
    button_style = {
        "width": 20,
        "font": ("Arial", 12),
        "bg": "#4E4E4E",
        "fg": "white",
        "pady": 10
    }

    # User buttons
    ttk.Button(root, text="See Available Movies", **button_style, command=lambda: booking.show_booking(username)).pack(pady=5)
    ttk.Button(root, text="My Bookings", **button_style, command=lambda: booking.view_user_bookings(username)).pack(pady=5)
    ttk.Button(root, text="My Reviews", **button_style, command=lambda: reviews.show_reviews(username)).pack(pady=5)

    # Staff-only buttons
    if is_staff:
        ttk.Button(root, text="Manage Movies", **button_style, command=movie_management.show_movie_management).pack(pady=5)
        ttk.Button(root, text="Manage Showtimes", **button_style, command=showtime_management.show_schedule).pack(pady=5)
        ttk.Button(root, text="View All Bookings", **button_style, command=staff_management.show_booking_management).pack(pady=5)
        ttk.Button(root, text="View Analytics", **button_style, command=staff_management.show_analytics).pack(pady=5)

    # Logout button at the bottom
    ttk.Button(root, text="Logout", **button_style, command=root.destroy).pack(pady=20)

    root.mainloop()

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

    ttk.Button(root, text="See Available Movies", **button_style, command=lambda: booking.show_booking(username)).pack(pady=5)
    ttk.Button(root, text="My Bookings", **button_style, command=lambda: booking.view_user_bookings(username)).pack(pady=5)
    ttk.Button(root, text="Rate & Review Movies", **button_style, command=lambda: reviews.show_review_screen(username)).pack(pady=5)
    
    # Logout Button
    ttk.Button(root, text="Logout", style="Danger.TButton", command=root.destroy).pack(pady=20)

    root.mainloop()

def staff_dashboard(username):
    """Displays the staff dashboard with a modern UI."""
    root = tk.Tk()  # Changed from Toplevel to Tk
    root.title("Staff Dashboard")
    root.geometry("600x500")  # Made taller to accommodate new button
    root.configure(bg="#34495E")

    # Title Label
    tk.Label(root, text=f"Welcome, {username} (Staff)", 
             font=("Arial", 18, "bold"), fg="white", bg="#34495E").pack(pady=20)

    # Styling the buttons
    button_style = {"bg": "#3498DB", "fg": "white", "font": ("Arial", 12), "width": 20, "height": 2}

    # Staff functionality buttons - only the essential ones
    tk.Button(root, text="Manage Movies", command=movie_management.show_movie_management, **button_style).pack(pady=10)
    tk.Button(root, text="Manage Showtimes", command=showtime_management.show_schedule, **button_style).pack(pady=10)
    tk.Button(root, text="Manage Users", command=staff_management.show_user_management, **button_style).pack(pady=10)
    tk.Button(root, text="View All Bookings", command=staff_management.show_booking_management, **button_style).pack(pady=10)
    tk.Button(root, text="View Analytics", command=staff_management.show_analytics, **button_style).pack(pady=10)
    
    # Logout Button
    tk.Button(root, text="Logout", command=root.destroy, bg="#E74C3C", fg="white", 
              font=("Arial", 12), width=20, height=2).pack(pady=20)

    root.mainloop()

def guest_dashboard():
    """Displays the guest dashboard with limited functionality."""
    root = tk.Toplevel()
    root.title("Guest Dashboard")
    root.geometry("600x500")
    root.configure(bg="#2C3E50")  # Dark background color

    # Title Label
    ttk.Label(root, text="Welcome, Guest", font=("Arial", 18, "bold"), foreground="white", background="#2C3E50").pack(pady=15)

    # Styling the buttons
    button_style = {"width": 25, "padding": 5}

    ttk.Button(root, text="See Available Movies", **button_style, command=lambda: booking.show_booking("Guest")).pack(pady=5)
    
    # Register button to encourage account creation
    ttk.Button(root, text="Create Account", **button_style, command=lambda: open_register(root)).pack(pady=5)
    
    # Logout Button
    ttk.Button(root, text="Exit", style="Danger.TButton", command=root.destroy).pack(pady=20)

    root.mainloop()

def open_register(root):
    """Opens the registration window."""
    from register import RegisterApp
    root.destroy()  # Close guest dashboard
    register_root = tk.Tk()
    RegisterApp(register_root)