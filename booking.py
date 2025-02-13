import sqlite3
import tkinter as tk
from tkinter import messagebox

def show_booking(username):
    """Allows users to book a ticket."""
    booking_window = tk.Toplevel()
    booking_window.title("Book a Ticket")
    booking_window.geometry("400x400")

    tk.Label(booking_window, text="Movie ID:").pack(pady=5)
    movie_id_entry = tk.Entry(booking_window)
    movie_id_entry.pack(pady=5)

    tk.Label(booking_window, text="Seat Number:").pack(pady=5)
    seat_entry = tk.Entry(booking_window)
    seat_entry.pack(pady=5)

    def book_ticket():
        """Processes ticket booking."""
        movie_id = movie_id_entry.get()
        seat_number = seat_entry.get()

        if not movie_id or not seat_number:
            messagebox.showerror("Error", "All fields are required")
            return

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Bookings (movie_id, customer_name, seat_number, booking_time) VALUES (?, ?, ?, datetime('now'))",
                       (movie_id, username, seat_number))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Ticket booked successfully!")

    tk.Button(booking_window, text="Book Ticket", command=book_ticket).pack(pady=10)

    
def view_user_bookings(username):
    """Shows all bookings for the logged-in user."""
    bookings_window = tk.Toplevel()
    bookings_window.title("My Bookings")
    bookings_window.geometry("500x400")

    bookings_listbox = tk.Listbox(bookings_window, width=50)
    bookings_listbox.pack(pady=10)

    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, movie_id, seat_number, booking_time FROM Bookings WHERE customer_name=?", (username,))
    bookings = cursor.fetchall()
    conn.close()

    for booking in bookings:
        bookings_listbox.insert(tk.END, f"{booking[0]} - Movie {booking[1]}, Seat {booking[2]} - {booking[3]}")
