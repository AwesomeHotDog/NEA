import sqlite3
import tkinter as tk
from tkinter import messagebox

def show_bookings():
    """Displays all bookings in a staff management window."""
    bookings_window = tk.Toplevel()
    bookings_window.title("Manage Bookings")
    bookings_window.geometry("500x400")

    bookings_listbox = tk.Listbox(bookings_window, width=60)
    bookings_listbox.pack(pady=10)

    def refresh_bookings():
        """Refreshes the booking list."""
        bookings_listbox.delete(0, tk.END)
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, movie_id, customer_name, seat_number, booking_time FROM Bookings")
        bookings = cursor.fetchall()
        conn.close()
        for booking in bookings:
            bookings_listbox.insert(tk.END, f"{booking[0]} - {booking[1]} (Seat {booking[3]}) - {booking[2]}")

    def delete_booking():
        """Deletes a selected booking."""
        selected_booking = bookings_listbox.curselection()
        if not selected_booking:
            messagebox.showerror("Error", "Please select a booking to cancel")
            return

        booking_id = bookings_listbox.get(selected_booking).split(" - ")[0]

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Bookings WHERE id=?", (booking_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Booking canceled successfully!")
        refresh_bookings()

    tk.Button(bookings_window, text="Cancel Selected Booking", command=delete_booking).pack(pady=5)
    refresh_bookings()
