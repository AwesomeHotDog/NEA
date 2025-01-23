import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Create the database and tables
def create_database():
    conn = sqlite3.connect('cinema_system.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Create Customer table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Customer (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT
    )''')

    # Create Movie table to store available movies
    cursor.execute('''CREATE TABLE IF NOT EXISTS Movie (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        duration INTEGER NOT NULL,  -- in minutes
        rating TEXT NOT NULL  -- e.g., PG, PG-13, R
    )''')

    # Create Screening table to track movie screenings
    cursor.execute('''CREATE TABLE IF NOT EXISTS Screening (
        screening_id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        screening_time TIMESTAMP NOT NULL,
        available_seats INTEGER NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE
    )''')

    # Create Booking table for customer ticket bookings
    cursor.execute('''CREATE TABLE IF NOT EXISTS Booking (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        screening_id INTEGER NOT NULL,
        seats_booked INTEGER NOT NULL,
        booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
        FOREIGN KEY (screening_id) REFERENCES Screening(screening_id) ON DELETE CASCADE
    )''')

    conn.commit()
    conn.close()

# Function to add a customer to the database
def add_customer():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()

    if not first_name or not last_name or not email:
        messagebox.showwarning("Input Error", "Please fill in all the required fields.")
        return

    conn = sqlite3.connect('cinema_system.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Customer (first_name, last_name, email, phone)
                      VALUES (?, ?, ?, ?)''', (first_name, last_name, email, phone))
    conn.commit()

    # Get the customer ID after insertion
    customer_id = cursor.lastrowid
    conn.close()

    messagebox.showinfo("Success", f"Customer {first_name} {last_name} added successfully!")
    clear_form()

    # Open the new window for movie selection
    open_movie_selection_window(customer_id)

# Function to open the movie selection window
def open_movie_selection_window(customer_id):
    # Create a new window
    movie_window = tk.Toplevel(root)
    movie_window.title("Select Movie and Seats")
    movie_window.geometry("400x300")

    # Label
    label = tk.Label(movie_window, text="Choose a Movie and Number of Seats", font=("Helvetica", 14))
    label.grid(row=0, column=0, columnspan=2, pady=10)

    # Fetch available movies from the database
    conn = sqlite3.connect('cinema_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movie")
    movies = cursor.fetchall()
    conn.close()

    movie_list = [movie[1] for movie in movies]  # Get only the movie titles

    # Create movie dropdown (combobox)
    movie_label = tk.Label(movie_window, text="Select Movie:", font=("Helvetica", 12))
    movie_label.grid(row=1, column=0, sticky=tk.W, pady=5)
    
    movie_combobox = ttk.Combobox(movie_window, values=movie_list, font=("Helvetica", 12), width=25)
    movie_combobox.grid(row=1, column=1, pady=5)

    # Create seats dropdown
    seat_label = tk.Label(movie_window, text="Select Number of Seats:", font=("Helvetica", 12))
    seat_label.grid(row=2, column=0, sticky=tk.W, pady=5)

    seat_combobox = ttk.Combobox(movie_window, values=[1, 2, 3, 4, 5], font=("Helvetica", 12), width=25)
    seat_combobox.grid(row=2, column=1, pady=5)

    # Submit button to book seats
    def submit_booking():
        selected_movie = movie_combobox.get()
        selected_seats = seat_combobox.get()

        if not selected_movie or not selected_seats:
            messagebox.showwarning("Input Error", "Please select a movie and number of seats.")
            return

        # Find the movie ID
        conn = sqlite3.connect('cinema_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT movie_id FROM Movie WHERE title=?", (selected_movie,))
        movie_id = cursor.fetchone()[0]

        # Find available screening
        cursor.execute("SELECT screening_id, available_seats FROM Screening WHERE movie_id=?", (movie_id,))
        screenings = cursor.fetchall()

        if not screenings:
            messagebox.showerror("Error", "No screenings available for this movie.")
            return

        # Select the first available screening (could be extended to choose from multiple screenings)
        screening_id, available_seats = screenings[0]

        # Check if enough seats are available
        if int(selected_seats) > available_seats:
            messagebox.showerror("Error", "Not enough seats available.")
            return

        # Update available seats
        cursor.execute('''UPDATE Screening SET available_seats = available_seats - ?
                          WHERE screening_id = ?''', (selected_seats, screening_id))

        # Insert the booking into the Booking table
        cursor.execute('''INSERT INTO Booking (customer_id, screening_id, seats_booked)
                          VALUES (?, ?, ?)''', (customer_id, screening_id, selected_seats))

        conn.commit()
        conn.close()

        messagebox.showinfo("Booking Success", f"Successfully booked {selected_seats} seats for {selected_movie}!")
        movie_window.destroy()

    submit_button = tk.Button(movie_window, text="Submit Booking", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=submit_booking)
    submit_button.grid(row=3, column=0, columnspan=2, pady=10)

# Function to clear input fields
def clear_form():
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

# Initialize the Tkinter window
root = tk.Tk()
root.title("Cinema Management System")
root.geometry("500x350")
root.config(bg="#f0f0f0")

# Add a header label
header_label = tk.Label(root, text="Reel House Cinema", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
header_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create form labels and entry fields for adding a customer
form_frame = tk.Frame(root, bg="#f0f0f0")
form_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

first_name_label = tk.Label(form_frame, text="First Name:", font=("Helvetica", 12), bg="#f0f0f0")
first_name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
first_name_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
first_name_entry.grid(row=0, column=1, pady=5)

last_name_label = tk.Label(form_frame, text="Last Name:", font=("Helvetica", 12), bg="#f0f0f0")
last_name_label.grid(row=1, column=0, sticky=tk.W, pady=5)
last_name_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
last_name_entry.grid(row=1, column=1, pady=5)

email_label = tk.Label(form_frame, text="Email:", font=("Helvetica", 12), bg="#f0f0f0")
email_label.grid(row=2, column=0, sticky=tk.W, pady=5)
email_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
email_entry.grid(row=2, column=1, pady=5)

phone_label = tk.Label(form_frame, text="Phone:", font=("Helvetica", 12), bg="#f0f0f0")
phone_label.grid(row=3, column=0, sticky=tk.W, pady=5)
phone_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
phone_entry.grid(row=3, column=1, pady=5)

# Create buttons for submitting and clearing the form
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

add_button = tk.Button(button_frame, text="Add Customer", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=add_customer, width=15)
add_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(button_frame, text="Clear", font=("Helvetica", 12), bg="#f44336", fg="white", command=clear_form, width=15)
clear_button.grid(row=0, column=1, padx=10)

# Run the program
if __name__ == "__main__":
    create_database()  # Create the database and tables if not already done
    root.mainloop()
