import sqlite3
import tkinter as tk
from tkinter import messagebox
from seat_selection import select_seat

def show_booking(username):
    """Displays the movie selection screen for booking."""
    booking_window = tk.Toplevel()
    booking_window.title("Book a Ticket")
    booking_window.geometry("500x400")

    tk.Label(booking_window, text="Select a Movie", font=("Arial", 14)).pack(pady=10)
    
    movie_listbox = tk.Listbox(booking_window, width=50)
    movie_listbox.pack(pady=5)

    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM Movies")
    movies = cursor.fetchall()
    conn.close()
    
    for movie in movies:
        movie_listbox.insert(tk.END, f"{movie[0]} - {movie[1]}")

    def proceed_to_seat_selection():
        """Opens seat selection for the selected movie."""
        selected_movie = movie_listbox.curselection()
        if not selected_movie:
            messagebox.showerror("Error", "Please select a movie to book a ticket.")
            return
        
        movie_id = int(movie_listbox.get(selected_movie).split(" - ")[0])
        select_seat(movie_id, username)
        booking_window.destroy()

    tk.Button(booking_window, text="Select Movie", command=proceed_to_seat_selection).pack(pady=10)

    booking_window.mainloop()

def view_user_bookings(username):
    """Displays all bookings made by the logged-in user."""
    bookings_window = tk.Toplevel()
    bookings_window.title("My Bookings")
    bookings_window.geometry("500x400")

    tk.Label(bookings_window, text="Your Bookings", font=("Arial", 14)).pack(pady=10)
    
    bookings_listbox = tk.Listbox(bookings_window, width=60)
    bookings_listbox.pack(pady=10)

    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, movie_id, seat_number, booking_time FROM Bookings WHERE customer_name=?", (username,))
    bookings = cursor.fetchall()
    conn.close()
    
    for booking in bookings:
        bookings_listbox.insert(tk.END, f"{booking[0]} - Movie {booking[1]}, Seat {booking[2]} - {booking[3]}")

    def cancel_booking():
        """Cancels the selected booking."""
        selected_booking = bookings_listbox.curselection()
        if not selected_booking:
            messagebox.showerror("Error", "Please select a booking to cancel.")
            return
        
        booking_id = int(bookings_listbox.get(selected_booking).split(" - ")[0])

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Bookings WHERE id=?", (booking_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Booking canceled successfully!")
        bookings_window.destroy()
        view_user_bookings(username)  # Refresh the list
    
    tk.Button(bookings_window, text="Cancel Selected Booking", command=cancel_booking).pack(pady=10)
    
    bookings_window.mainloop()
