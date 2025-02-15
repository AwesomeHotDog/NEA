import tkinter as tk
import booking
import reviews
import staff_management  # For managing users & bookings
import movie_management  # For movie management
import analytics  # For reports & analytics

def staff_dashboard(username):
    """GUI for staff dashboard with management options."""
    root = tk.Toplevel()
    root.title("Staff Dashboard")
    root.geometry("500x500")

    tk.Label(root, text=f"Welcome, {username} (Staff)", font=("Arial", 16)).pack(pady=20)

    # Buttons for staff features
    tk.Button(root, text="Manage Movies", width=25, command=movie_management.show_movie_management).pack(pady=5)
    tk.Button(root, text="Manage Users", width=25, command=staff_management.show_user_management).pack(pady=5)
    tk.Button(root, text="Manage Bookings", width=25, command=staff_management.show_booking_management).pack(pady=5)
    tk.Button(root, text="View Analytics", width=25, command=analytics.generate_sales_report).pack(pady=5)

    # Logout Button
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

