import sqlite3
import tkinter as tk
from tkinter import messagebox
from seat_selection import select_seat
from omdb_api import fetch_movie_details  # Import API function
from PIL import Image, ImageTk
import requests
from io import BytesIO
from datetime import datetime
from tkinter import ttk

def show_booking(username):
    """Displays the movie selection screen for booking."""
    booking_window = tk.Toplevel()
    booking_window.title("Book a Ticket")
    booking_window.geometry("1000x600")
    booking_window.configure(bg="#2A2A2A")  # Dark theme

    # Create main container frame
    main_frame = tk.Frame(booking_window, bg="#2A2A2A")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Left side - Movie and showtime selection
    left_frame = tk.Frame(main_frame, bg="#2A2A2A")
    left_frame.pack(side="left", fill="y", padx=(0, 20))

    # Add filter frame
    filter_frame = tk.Frame(left_frame, bg="#2A2A2A")
    filter_frame.pack(fill="x", pady=(0, 10))

    # Genre filter
    tk.Label(filter_frame, text="Genre:", fg="white", bg="#2A2A2A").pack(side="left", padx=5)
    genre_var = tk.StringVar()
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT genre FROM Movies ORDER BY genre")
    genres = ["All"] + [row[0] for row in cursor.fetchall()]
    conn.close()
    
    genre_combo = ttk.Combobox(filter_frame, textvariable=genre_var, values=genres, state="readonly", width=15)
    genre_combo.pack(side="left", padx=5)
    genre_combo.set("All")

    # Duration filter
    tk.Label(filter_frame, text="Duration:", fg="white", bg="#2A2A2A").pack(side="left", padx=5)
    duration_var = tk.StringVar()
    duration_options = ["All", "< 2h", "2-3h", "> 3h"]
    duration_combo = ttk.Combobox(filter_frame, textvariable=duration_var, values=duration_options, state="readonly", width=10)
    duration_combo.pack(side="left", padx=5)
    duration_combo.set("All")

    # Movie selection
    tk.Label(left_frame, text="Select a Movie", font=("Arial", 14, "bold"), fg="white", bg="#2A2A2A").pack(pady=10)
    movie_listbox = tk.Listbox(left_frame, width=40, bg="white")
    movie_listbox.pack(pady=5)

    # Showtime selection
    tk.Label(left_frame, text="Select Showtime", font=("Arial", 14, "bold"), fg="white", bg="#2A2A2A").pack(pady=10)
    showtime_listbox = tk.Listbox(left_frame, width=40, bg="white")
    showtime_listbox.pack(pady=5)

    # Right side - Movie details and poster
    right_frame = tk.Frame(main_frame, bg="#2A2A2A")
    right_frame.pack(side="right", fill="both", expand=True)

    # Poster label
    poster_label = tk.Label(right_frame, bg="#2A2A2A")
    poster_label.pack(pady=10)

    details_text = tk.StringVar()
    details_label = tk.Label(right_frame, textvariable=details_text, wraplength=400, fg="white", bg="#2A2A2A", justify="left")
    details_label.pack(pady=10)

    def load_movies():
        """Load movies based on selected filters."""
        genre = genre_var.get()
        duration = duration_var.get()

        # Build the query based on filters
        query = "SELECT id, title FROM Movies WHERE 1=1"
        params = []

        if genre != "All":
            query += " AND genre = ?"
            params.append(genre)

        if duration != "All":
            if duration == "< 2h":
                query += " AND duration < 120"
            elif duration == "2-3h":
                query += " AND duration BETWEEN 120 AND 180"
            else:  # > 3h
                query += " AND duration > 180"

        query += " ORDER BY title"

        # Clear current items
        movie_listbox.delete(0, tk.END)
        movie_dict.clear()

        # Load filtered movies
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute(query, params)
        movies = cursor.fetchall()
        conn.close()

        for movie in movies:
            movie_listbox.insert(tk.END, f"{movie[1]}")
            movie_dict[movie[1]] = movie[0]

        # Clear showtime selection and movie details
        showtime_listbox.delete(0, tk.END)
        details_text.set("")
        poster_label.config(image="")

    # Store movie dictionary at window level
    movie_dict = {}
    
    # Initial load of movies
    load_movies()

    # Store showtime dictionary at window level
    current_showtimes = {}

    def apply_filters():
        """Apply selected filters to movie list."""
        load_movies()

    # Add filter button
    tk.Button(filter_frame, text="Apply Filters", bg="#4E4E4E", fg="white", command=apply_filters).pack(side="left", padx=5)

    def load_showtimes():
        """Load showtimes for the selected movie."""
        selected_index = movie_listbox.curselection()
        current_showtimes.clear()  # Clear previous showtimes
        
        if not selected_index:
            showtime_listbox.delete(0, tk.END)
            return

        movie_title = movie_listbox.get(selected_index)
        movie_id = movie_dict[movie_title]

        # Get today's date
        today = datetime.now().date()

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, show_date, show_time, hall_number, price, available_seats
            FROM Showtimes
            WHERE movie_id = ? AND show_date >= ?
            ORDER BY show_date, show_time
        """, (movie_id, today.strftime("%Y-%m-%d")))
        showtimes = cursor.fetchall()
        conn.close()

        showtime_listbox.delete(0, tk.END)
        for showtime in showtimes:
            showtime_text = f"{showtime[1]} {showtime[2]} - Hall {showtime[3]} - ${showtime[4]} ({showtime[5]} seats)"
            showtime_listbox.insert(tk.END, showtime_text)
            current_showtimes[showtime_text] = showtime[0]

    def show_movie_details():
        """Fetch and display movie details from OMDB API."""
        selected_index = movie_listbox.curselection()
        if not selected_index:
            details_text.set("Please select a movie.")
            poster_label.config(image="")
            return

        movie_title = movie_listbox.get(selected_index)
        movie_data = fetch_movie_details(movie_title)

        if movie_data:
            # Display text details
            details_text.set(
                f"Title: {movie_data['title']}\n"
                f"Year: {movie_data['year']}\n"
                f"Genre: {movie_data['genre']}\n"
                f"IMDb Rating: {movie_data['rating']}\n"
                f"Plot: {movie_data['plot']}"
            )

            # Display poster
            if movie_data['poster'] and movie_data['poster'] != 'N/A':
                try:
                    response = requests.get(movie_data['poster'])
                    img_data = BytesIO(response.content)
                    img = Image.open(img_data)
                    img.thumbnail((300, 400))
                    photo = ImageTk.PhotoImage(img)
                    poster_label.config(image=photo)
                    poster_label.image = photo
                except Exception as e:
                    print(f"Error loading poster: {e}")
                    poster_label.config(image="")
            else:
                poster_label.config(image="")

            # Load showtimes for the selected movie
            load_showtimes()
        else:
            details_text.set("Movie details not found.")
            poster_label.config(image="")

    def proceed_to_seat_selection():
        """Opens seat selection for the selected showtime."""
        selected_showtime = showtime_listbox.curselection()
        if not selected_showtime:
            messagebox.showerror("Error", "Please select a showtime to book a ticket.")
            return

        showtime_text = showtime_listbox.get(selected_showtime)
        if showtime_text not in current_showtimes:
            messagebox.showerror("Error", "Invalid showtime selection. Please try again.")
            return
        
        showtime_id = current_showtimes[showtime_text]

        # For guest users, show a message about creating an account
        if username == "Guest":
            if messagebox.askyesno("Guest User", "As a guest, you can book tickets but won't be able to view or manage your bookings later. Would you like to create an account instead?"):
                from register import RegisterApp
                booking_window.destroy()
                register_root = tk.Tk()
                RegisterApp(register_root)
                return

        select_seat(showtime_id, username)
        booking_window.destroy()

    # Buttons frame
    button_frame = tk.Frame(left_frame, bg="#2A2A2A")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Show Details", bg="#4E4E4E", fg="white", command=show_movie_details).pack(side="left", padx=5)
    tk.Button(button_frame, text="Select Showtime", bg="#4E4E4E", fg="white", command=proceed_to_seat_selection).pack(side="left", padx=5)

    booking_window.mainloop()

def view_user_bookings(username):
    """Displays all bookings made by the logged-in user."""
    if username == "Guest":
        messagebox.showinfo("Guest User", "Guest users cannot view their bookings. Please create an account to access this feature.")
        return

    bookings_window = tk.Toplevel()
    bookings_window.title("My Bookings")
    bookings_window.geometry("800x600")
    bookings_window.configure(bg="#2A2A2A")  # Dark theme

    # Create main container frame
    main_frame = tk.Frame(bookings_window, bg="#2A2A2A")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Create Treeview for bookings
    columns = ("Movie", "Date", "Time", "Hall", "Seat", "Price", "Booking Time")
    booking_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
    
    # Configure columns
    for col in columns:
        booking_tree.heading(col, text=col)
        booking_tree.column(col, width=100)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=booking_tree.yview)
    booking_tree.configure(yscrollcommand=scrollbar.set)

    # Pack the Treeview and scrollbar
    booking_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Load bookings
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.title, s.show_date, s.show_time, s.hall_number, b.seat_number, s.price, b.booking_time
        FROM Bookings b
        JOIN Showtimes s ON b.showtime_id = s.id
        JOIN Movies m ON s.movie_id = m.id
        WHERE b.customer_name = ?
        ORDER BY s.show_date, s.show_time
    """, (username,))
    bookings = cursor.fetchall()
    conn.close()

    # Insert data into Treeview
    for booking in bookings:
        booking_tree.insert("", "end", values=booking)

    def cancel_booking():
        """Cancels the selected booking."""
        selected_item = booking_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a booking to cancel")
            return

        booking_data = booking_tree.item(selected_item[0])['values']
        movie_title = booking_data[0]
        show_date = booking_data[1]
        show_time = booking_data[2]
        seat_number = booking_data[4]

        if messagebox.askyesno("Confirm Cancel", f"Are you sure you want to cancel your booking for {movie_title} on {show_date} at {show_time} (Seat {seat_number})?"):
            conn = sqlite3.connect("cinema_system.db")
            cursor = conn.cursor()
            
            # Get the booking ID
            cursor.execute("""
                SELECT b.id
                FROM Bookings b
                JOIN Showtimes s ON b.showtime_id = s.id
                JOIN Movies m ON s.movie_id = m.id
                WHERE m.title = ? AND s.show_date = ? AND s.show_time = ? AND b.seat_number = ? AND b.customer_name = ?
            """, (movie_title, show_date, show_time, seat_number, username))
            
            booking_id = cursor.fetchone()[0]
            
            # Delete the booking
            cursor.execute("DELETE FROM Bookings WHERE id = ?", (booking_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Booking cancelled successfully!")
            bookings_window.destroy()
            view_user_bookings(username)  # Refresh the window

    # Add cancel button
    tk.Button(bookings_window, text="Cancel Selected Booking", bg="#A83232", fg="white", command=cancel_booking).pack(pady=10)

    bookings_window.mainloop()

def select_seat(showtime_id, username):
    """Displays the seat selection screen."""
    seat_window = tk.Toplevel()
    seat_window.title("Select Seats")  # Updated title to reflect multiple selection
    seat_window.geometry("800x600")
    seat_window.configure(bg="#2A2A2A")  # Dark theme

    # Create main container frame
    main_frame = tk.Frame(seat_window, bg="#2A2A2A")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Get showtime details
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.show_date, s.show_time, s.hall_number, s.price, s.available_seats, m.title
        FROM Showtimes s
        JOIN Movies m ON s.movie_id = m.id
        WHERE s.id = ?
    """, (showtime_id,))
    showtime = cursor.fetchone()
    conn.close()

    if not showtime:
        messagebox.showerror("Error", "Showtime not found")
        seat_window.destroy()
        return

    show_date, show_time, hall_number, price, available_seats, movie_title = showtime

    # Display showtime details
    details_frame = tk.Frame(main_frame, bg="#2A2A2A")
    details_frame.pack(fill="x", pady=(0, 20))

    tk.Label(details_frame, text=f"Movie: {movie_title}", font=("Arial", 12, "bold"), fg="white", bg="#2A2A2A").pack(side="left", padx=10)
    tk.Label(details_frame, text=f"Date: {show_date}", font=("Arial", 12, "bold"), fg="white", bg="#2A2A2A").pack(side="left", padx=10)
    tk.Label(details_frame, text=f"Time: {show_time}", font=("Arial", 12, "bold"), fg="white", bg="#2A2A2A").pack(side="left", padx=10)
    tk.Label(details_frame, text=f"Hall: {hall_number}", font=("Arial", 12, "bold"), fg="white", bg="#2A2A2A").pack(side="left", padx=10)
    tk.Label(details_frame, text=f"Price: ${price}", font=("Arial", 12, "bold"), fg="white", bg="#2A2A2A").pack(side="left", padx=10)

    # Add total price display
    total_price_var = tk.StringVar()
    total_price_var.set("Total Price: $0.00")
    tk.Label(details_frame, textvariable=total_price_var, font=("Arial", 12, "bold"), fg="white", bg="#2A2A2A").pack(side="right", padx=10)

    # Create seat selection frame
    seat_frame = tk.Frame(main_frame, bg="#2A2A2A")
    seat_frame.pack(expand=True)

    # Create seat buttons
    rows = 8
    cols = 10
    seat_buttons = {}
    selected_seats = set()  # Use a set to store multiple selected seats

    # Get booked seats
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT seat_number FROM Bookings WHERE showtime_id = ?", (showtime_id,))
    booked_seats = [row[0] for row in cursor.fetchall()]
    conn.close()

    def update_total_price():
        """Updates the total price display based on selected seats."""
        total = len(selected_seats) * price
        total_price_var.set(f"Total Price: ${total:.2f}")

    def select_seat_button(seat_number):
        """Handles seat button selection."""
        if seat_number in selected_seats:
            # Deselect the seat
            selected_seats.remove(seat_number)
            seat_buttons[seat_number].configure(bg="#6E6E6E")
        else:
            # Select the seat
            selected_seats.add(seat_number)
            seat_buttons[seat_number].configure(bg="#32A832")
        
        update_total_price()

    for row in range(rows):
        for col in range(cols):
            seat_number = f"{chr(65 + row)}{col + 1}"  # A1, A2, etc.
            seat_button = tk.Button(
                seat_frame,
                text=seat_number,
                width=4,
                height=2,
                bg="#4E4E4E" if seat_number in booked_seats else "#6E6E6E",
                fg="white",
                state="disabled" if seat_number in booked_seats else "normal",
                command=lambda s=seat_number: select_seat_button(s)
            )
            seat_button.grid(row=row, column=col, padx=2, pady=2)
            seat_buttons[seat_number] = seat_button

    # Legend frame
    legend_frame = tk.Frame(main_frame, bg="#2A2A2A")
    legend_frame.pack(fill="x", pady=20)

    tk.Label(legend_frame, text="Available", font=("Arial", 10), fg="white", bg="#2A2A2A").pack(side="left", padx=10)
    tk.Label(legend_frame, text="Selected", font=("Arial", 10), fg="white", bg="#2A2A2A").pack(side="left", padx=10)
    tk.Label(legend_frame, text="Booked", font=("Arial", 10), fg="white", bg="#2A2A2A").pack(side="left", padx=10)

    # Create legend boxes
    tk.Frame(legend_frame, width=20, height=20, bg="#6E6E6E").pack(side="left", padx=5)
    tk.Frame(legend_frame, width=20, height=20, bg="#32A832").pack(side="left", padx=5)
    tk.Frame(legend_frame, width=20, height=20, bg="#4E4E4E").pack(side="left", padx=5)

    def confirm_booking():
        """Confirms the seat booking."""
        if not selected_seats:
            messagebox.showerror("Error", "Please select at least one seat")
            return

        # Confirm multiple seat booking
        seats_str = ", ".join(sorted(selected_seats))
        total_price = len(selected_seats) * price
        if not messagebox.askyesno("Confirm Booking", 
                                  f"Do you want to book the following seats?\n\n"
                                  f"Seats: {seats_str}\n"
                                  f"Total Price: ${total_price:.2f}"):
            return

        # Create bookings
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        
        try:
            # Get current timestamp
            booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Insert bookings
            for seat_number in selected_seats:
                cursor.execute("""
                    INSERT INTO Bookings (showtime_id, customer_name, seat_number, booking_time)
                    VALUES (?, ?, ?, ?)
                """, (showtime_id, username, seat_number, booking_time))
            
            # Update available seats
            cursor.execute("""
                UPDATE Showtimes 
                SET available_seats = available_seats - ? 
                WHERE id = ?
            """, (len(selected_seats), showtime_id))
            
            conn.commit()
            messagebox.showinfo("Success", f"Successfully booked seats: {seats_str}")
            seat_window.destroy()
            
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to book seats: {str(e)}")
        finally:
            conn.close()

    # Add buttons frame
    button_frame = tk.Frame(main_frame, bg="#2A2A2A")
    button_frame.pack(pady=10)

    # Add clear selection button
    def clear_selection():
        """Clears all selected seats."""
        for seat in selected_seats.copy():
            select_seat_button(seat)

    tk.Button(button_frame, text="Clear Selection", bg="#4E4E4E", fg="white", command=clear_selection).pack(side="left", padx=5)
    tk.Button(button_frame, text="Confirm Booking", bg="#32A832", fg="white", command=confirm_booking).pack(side="left", padx=5)

    seat_window.mainloop()
