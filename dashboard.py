import tkinter as tk
import reviews
import booking
import movie_management



def staff_dashboard(username):
    """GUI for staff dashboard with more management options."""
    root = tk.Toplevel()
    root.title("Staff Dashboard")
    root.geometry("500x500")

    tk.Label(root, text=f"Welcome, {username} (Staff)", font=("Arial", 16)).pack(pady=20)

    # Movie Management
    tk.Button(root, text="Manage Movies", width=25, command=movie_management.show_movie_management).pack(pady=5)

    # Booking Management
    tk.Button(root, text="View Bookings", width=25, command=booking_management.show_bookings).pack(pady=5)

    # User Management
    tk.Button(root, text="Manage Users", width=25, command=user_management.show_user_management).pack(pady=5)

    # Analytics
    tk.Button(root, text="View Analytics", width=25, command=analytics.show_analytics).pack(pady=5)

    # Logout
    tk.Button(root, text="Logout", width=25, command=root.destroy).pack(pady=20)

    root.mainloop()

def user_dashboard(username):
    """User dashboard with multiple features."""
    root = tk.Toplevel()
    root.title("User Dashboard")
    root.geometry("500x500")

    tk.Label(root, text=f"Welcome, {username} (User)", font=("Arial", 16)).pack(pady=20)

    # View Movies
    tk.Button(root, text="View Available Movies", width=25, command=movie_management.show_movies).pack(pady=5)

    # Book Tickets
    tk.Button(root, text="Book a Ticket", width=25, command=lambda: booking.show_booking(username)).pack(pady=5)

    # View Bookings
    tk.Button(root, text="My Bookings", width=25, command=lambda: booking.view_user_bookings(username)).pack(pady=5)

    # Review Movies
    tk.Button(root, text="Rate & Review Movies", width=25, command=lambda: reviews.show_review_screen(username)).pack(pady=5)

    # Manage Reviews
    tk.Button(root, text="Manage My Reviews", width=25, command=lambda: reviews.manage_reviews(username)).pack(pady=5)

    # Logout
    tk.Button(root, text="Logout", width=25, command=root.destroy).pack(pady=20)

    root.mainloop()

