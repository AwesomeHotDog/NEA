import sqlite3
import tkinter as tk
from tkinter import messagebox

def show_user_management():
    """Displays a list of users with management options."""
    user_window = tk.Toplevel()
    user_window.title("User Management")
    user_window.geometry("500x400")

    tk.Label(user_window, text="Manage Users", font=("Arial", 14)).pack(pady=10)
    
    user_listbox = tk.Listbox(user_window, width=50)
    user_listbox.pack(pady=10)

    def refresh_users():
        """Refresh the user list."""
        user_listbox.delete(0, tk.END)
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM User")
        users = cursor.fetchall()
        conn.close()
        for user in users:
            user_listbox.insert(tk.END, f"{user[0]} - {user[1]}")
    
    def delete_user():
        """Deletes the selected user."""
        selected_user = user_listbox.curselection()
        if not selected_user:
            messagebox.showerror("Error", "Please select a user to delete.")
            return
        
        user_id = int(user_listbox.get(selected_user).split(" - ")[0])
        
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM User WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "User deleted successfully!")
        refresh_users()
    
    tk.Button(user_window, text="Delete Selected User", command=delete_user).pack(pady=5)
    refresh_users()

def show_booking_management():
    """Displays all bookings with management options."""
    booking_window = tk.Toplevel()
    booking_window.title("Booking Management")
    booking_window.geometry("500x400")

    tk.Label(booking_window, text="Manage Bookings", font=("Arial", 14)).pack(pady=10)
    
    booking_listbox = tk.Listbox(booking_window, width=60)
    booking_listbox.pack(pady=10)

    def refresh_bookings():
        """Refresh the booking list."""
        booking_listbox.delete(0, tk.END)
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, movie_id, customer_name, seat_number, booking_time FROM Bookings")
        bookings = cursor.fetchall()
        conn.close()
        for booking in bookings:
            booking_listbox.insert(tk.END, f"{booking[0]} - Movie {booking[1]}, Seat {booking[3]} - {booking[2]} at {booking[4]}")
    
    def delete_booking():
        """Deletes the selected booking."""
        selected_booking = booking_listbox.curselection()
        if not selected_booking:
            messagebox.showerror("Error", "Please select a booking to delete.")
            return
        
        booking_id = int(booking_listbox.get(selected_booking).split(" - ")[0])
        
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Bookings WHERE id=?", (booking_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Booking deleted successfully!")
        refresh_bookings()
    
    tk.Button(booking_window, text="Delete Selected Booking", command=delete_booking).pack(pady=5)
    refresh_bookings()


