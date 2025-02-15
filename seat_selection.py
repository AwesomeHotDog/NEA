import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def select_seat(movie_id, username):
    """Creates a visual multi-seat selection system for booking tickets."""
    seat_window = tk.Toplevel()
    seat_window.title("Select Seats")
    seat_window.geometry("500x500")
    seat_window.configure(bg="#2A2A2A")  # ✅ Dark theme

    ttk.Label(seat_window, text="Select Your Seats", font=("Arial", 14, "bold"), foreground="white", background="#2A2A2A").pack(pady=10)

    seats = []
    seat_buttons = {}
    selected_seats = set()  # ✅ Store selected seats

    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT seat_number FROM Bookings WHERE movie_id=?", (movie_id,))
    booked_seats = {row[0] for row in cursor.fetchall()}  # ✅ Use a set for fast lookup
    conn.close()

    seat_frame = tk.Frame(seat_window, bg="#2A2A2A")
    seat_frame.pack(pady=10)

    def toggle_seat(seat):
        """Toggles seat selection (select or deselect)."""
        if seat in booked_seats:
            messagebox.showerror("Error", f"Seat {seat} is already booked!")
            return

        if seat in selected_seats:
            selected_seats.remove(seat)
            seat_buttons[seat].config(bg="green")  # ✅ Mark as available again
        else:
            selected_seats.add(seat)
            seat_buttons[seat].config(bg="orange")  # ✅ Highlight selected seat

    def confirm_booking():
        """Confirms booking for multiple selected seats."""
        if not selected_seats:
            messagebox.showerror("Error", "Please select at least one seat!")
            return

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()

        for seat in selected_seats:
            cursor.execute(
                "INSERT INTO Bookings (movie_id, customer_name, seat_number, booking_time) VALUES (?, ?, ?, datetime('now'))",
                (movie_id, username, seat)
            )
        
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Seats {', '.join(selected_seats)} booked successfully!")
        seat_window.destroy()

    # ✅ Generate a seat grid (5 rows x 5 columns)
    for row in range(5):
        for col in range(5):
            seat = f"{row+1}{chr(65+col)}"  # E.g., "1A", "2B"
            btn_color = "red" if seat in booked_seats else "green"
            button = tk.Button(seat_frame, text=seat, width=4, height=2, bg=btn_color, fg="white",
                               command=lambda s=seat: toggle_seat(s))
            button.grid(row=row, column=col, padx=5, pady=5)
            seat_buttons[seat] = button

    ttk.Button(seat_window, text="Confirm Booking", command=confirm_booking).pack(pady=10)

    seat_window.mainloop()
