import sqlite3
import tkinter as tk
from tkinter import messagebox
from seat_selection import select_seat

def show_booking(username):
    """Displays the movie selection screen for booking."""
    booking_window = tk.Toplevel()
    booking_window.title("Book a Ticket")
    booking_window.geometry("500x400")
    booking_window.configure(bg="#2A2A2A")  # ✅ Dark theme

    tk.Label(booking_window, text="Select a Movie", font=("Arial", 14, "bold"), fg="white", bg="#2A2A2A").pack(pady=10)

    movie_listbox = tk.Listbox(booking_window, width=50, bg="white")
    movie_listbox.pack(pady=5)

    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM Movies")
    movies = cursor.fetchall()
    conn.close()

    movie_dict = {}  # Store movie ID and title
    for movie in movies:
        movie_listbox.insert(tk.END, f"{movie[1]}")  # ✅ Show actual movie title
        movie_dict[movie[1]] = movie[0]  # Store ID mapped to title

    def proceed_to_seat_selection():
        """Opens seat selection for the selected movie."""
        selected_index = movie_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a movie to book a ticket.")
            return
        
        movie_title = movie_listbox.get(selected_index)  # Get the selected movie title
        movie_id = movie_dict[movie_title]  # Get the movie ID
        select_seat(movie_id, username)
        booking_window.destroy()

    tk.Button(booking_window, text="Select Movie", bg="#4E4E4E", fg="white", command=proceed_to_seat_selection).pack(pady=10)

    booking_window.mainloop()
    def proceed_to_seat_selection():
        """Opens multi-seat selection for the selected movie."""
        selected_index = movie_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a movie to book tickets.")
            return
    
    movie_title = movie_listbox.get(selected_index)
    movie_id = movie_dict[movie_title]  # ✅ Get movie ID correctly
    select_seat(movie_id, username)  # ✅ Now allows multiple seat selection
    booking_window.destroy()

    
    

def view_user_bookings(username):
    """Displays all bookings made by the logged-in user."""
    bookings_window = tk.Toplevel()
    bookings_window.title("My Bookings")
    bookings_window.geometry("500x400")
    bookings_window.configure(bg="#2A2A2A")  # ✅ Dark theme

    tk.Label(bookings_window, text="Your Bookings", font=("Arial", 14, "bold"), fg="white", bg="#2A2A2A").pack(pady=10)

    bookings_listbox = tk.Listbox(bookings_window, width=60, bg="white")
    bookings_listbox.pack(pady=10)

    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Bookings.id, Movies.title, Bookings.seat_number, Bookings.booking_time 
        FROM Bookings 
        JOIN Movies ON Bookings.movie_id = Movies.id 
        WHERE Bookings.customer_name=?
    """, (username,))
    bookings = cursor.fetchall()
    conn.close()

    if not bookings:
        bookings_listbox.insert(tk.END, "No bookings found.")

    booking_dict = {}  # Store booking ID mapped to index
    for i, booking in enumerate(bookings):
        booking_text = f"{booking[1]} - Seat {booking[2]} - {booking[3]}"  # ✅ Show actual movie title
        bookings_listbox.insert(tk.END, booking_text)
        booking_dict[i] = booking[0]  # Store booking ID mapped to index

    def cancel_booking():
        """Cancels the selected booking."""
        selected_index = bookings_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a booking to cancel.")
            return

        booking_id = booking_dict[selected_index[0]]  # ✅ Get correct booking ID

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Bookings WHERE id=?", (booking_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Booking canceled successfully!")
        bookings_window.destroy()
        view_user_bookings(username)  # ✅ Refresh booking list after deletion

    tk.Button(bookings_window, text="Cancel Selected Booking", bg="#A83232", fg="white", command=cancel_booking).pack(pady=10)

    bookings_window.mainloop()
