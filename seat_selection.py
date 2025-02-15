import tkinter as tk
from tkinter import messagebox
import sqlite3

def select_seat(movie_id, username):
    """Creates a visual seat selection system for booking tickets."""
    seat_window = tk.Toplevel()
    seat_window.title("Select a Seat")
    seat_window.geometry("400x400")

    tk.Label(seat_window, text="Select a Seat", font=("Arial", 14)).pack(pady=10)

    seats = []
    seat_buttons = {}

    # Connect to database and fetch booked seats
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT seat_number FROM Bookings WHERE movie_id=?", (movie_id,))
    booked_seats = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Create a frame to contain the seat buttons and use grid() inside it
    seat_frame = tk.Frame(seat_window)
    seat_frame.pack(pady=10)  # Using pack() here, grid() inside the frame is fine

    def book_seat(seat):
        """Handles seat selection and booking confirmation."""
        if seat in booked_seats:
            messagebox.showerror("Error", f"Seat {seat} is already booked!")
            return

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Bookings (movie_id, customer_name, seat_number, booking_time) VALUES (?, ?, ?, datetime('now'))",
                       (movie_id, username, seat))
        conn.commit()
        conn.close()

        booked_seats.append(seat)
        seat_buttons[seat].config(bg="red", state="disabled")  # Update seat button color
        messagebox.showinfo("Success", f"Seat {seat} booked successfully!")
        seat_window.destroy()

    # Generate a grid of seat buttons inside the seat_frame
    for row in range(5):  # 5 rows
        for col in range(5):  # 5 columns
            seat = f"{row+1}{chr(65+col)}"  # E.g., "1A", "2B"
            btn_color = "red" if seat in booked_seats else "green"
            button = tk.Button(seat_frame, text=seat, width=4, height=2,
                               bg=btn_color, fg="white",
                               command=lambda s=seat: book_seat(s))
            button.grid(row=row, column=col, padx=5, pady=5)
            seat_buttons[seat] = button

    seat_window.mainloop()
