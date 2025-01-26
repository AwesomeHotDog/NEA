import tkinter as tk
from tkinter import Tk, Toplevel, Label, Entry, Button, StringVar, messagebox, ttk
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to authenticate staff
def authenticate_staff(username, password):
    conn = sqlite3.connect('cinema_system.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM staff WHERE username = ? AND password = ?", (username, password))
    staff = cursor.fetchone()
    conn.close()
    
    return staff  # None if authentication fails, otherwise staff data as a tuple

# Staff login screen
def staff_login_screen():
    def login():
        username = username_entry.get()
        password = password_entry.get()
        
        # Authenticate the staff
        staff = authenticate_staff(username, password)
        if staff:
            messagebox.showinfo("Login Successful", f"Welcome, {staff[1]}!")
            login_window.destroy()
            open_staff_dashboard(staff)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    
    # Create login window
    login_window = tk.Tk()
    login_window.title("Staff Login")
    
    tk.Label(login_window, text="Staff Login", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
    
    tk.Label(login_window, text="Username:").grid(row=1, column=0, padx=10, pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(login_window, text="Password:").grid(row=2, column=0, padx=10, pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Button(login_window, text="Login", command=login).grid(row=3, column=0, columnspan=2, pady=10)
    
    login_window.mainloop()

# Staff dashboard
def open_staff_dashboard(staff):
    dashboard = tk.Tk()
    dashboard.title("Staff Dashboard")
    
    tk.Label(dashboard, text=f"Welcome, {staff[1]} ({staff[3].capitalize()})", font=("Arial", 16)).pack(pady=10)
    
    # Add management buttons based on staff role
    if staff[3] == "admin":  # Only admins can access certain features
        tk.Button(dashboard, text="Manage Movies", command=manage_movies).pack(pady=5)
        tk.Button(dashboard, text="Manage Bookings", command=manage_bookings).pack(pady=5)
    else:
        tk.Label(dashboard, text="Access limited to general staff features.").pack(pady=5)
    
    tk.Button(dashboard, text="Logout", command=dashboard.destroy).pack(pady=20)

    dashboard.mainloop()

# Manage movies (admin only)
def manage_movies():
    movies_window = tk.Toplevel()
    movies_window.title("Manage Movies")
    
def fetch_movies():
    """Fetch all movies from the database."""
    conn = sqlite3.connect('cinema_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    conn.close()
    return movies

def add_movie(title, genre, duration, release_date):
    """Add a movie to the database."""
    conn = sqlite3.connect('cinema_system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movies (title, genre, duration, release_date) VALUES (?, ?, ?, ?)",
                   (title, genre, duration, release_date))
    conn.commit()
    conn.close()

def update_movie(movie_id, title, genre, duration, release_date):
    """Update an existing movie in the database."""
    conn = sqlite3.connect('cinema_system.db')
    cursor = conn.cursor()
    cursor.execute("""UPDATE movies SET title = ?, genre = ?, duration = ?, release_date = ?
                      WHERE id = ?""",
                   (title, genre, duration, release_date, movie_id))
    conn.commit()
    conn.close()

def delete_movie(movie_id):
    """Delete a movie from the database."""
    conn = sqlite3.connect('cinema_system.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    conn.commit()
    conn.close()

# Main Manage Movies Function
def manage_movies():
    """Open the Manage Movies window."""
    def refresh_movies():
        """Refresh the movie list in the Treeview."""
        for item in tree.get_children():
            tree.delete(item)
        movies = fetch_movies()
        for movie in movies:
            tree.insert("", "end", values=movie)

    def on_add_movie():
        """Handle adding a new movie."""
        title = title_var.get().strip()
        genre = genre_var.get().strip()
        duration = duration_var.get().strip()
        release_date = release_date_var.get().strip()

        if not title or not genre or not duration or not release_date:
            messagebox.showerror("Error", "All fields are required!")
            return
        if not duration.isdigit():
            messagebox.showerror("Error", "Duration must be a number!")
            return

        try:
            add_movie(title, genre, int(duration), release_date)
            refresh_movies()
            title_var.set("")
            genre_var.set("")
            duration_var.set("")
            release_date_var.set("")
            conn = sqlite3.connect("cinema_system.db")
            cursor = conn.cursor()
            cursor.execute(
            "INSERT INTO movies (title, genre, duration, release_date) VALUES (?, ?, ?, ?)",
            (title, genre, duration, release_date),
        )
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add movie: {e}")

    def on_update_movie():
        """Handle updating an existing movie."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a movie to update!")
            return

        movie_id = tree.item(selected_item, "values")[0]
        title = title_var.get().strip()
        genre = genre_var.get().strip()
        duration = duration_var.get().strip()
        release_date = release_date_var.get().strip()

        if not title or not genre or not duration or not release_date:
            messagebox.showerror("Error", "All fields are required!")
            return
        if not duration.isdigit():
            messagebox.showerror("Error", "Duration must be a number!")
            return

        try:
            update_movie(movie_id, title, genre, int(duration), release_date)
            refresh_movies()
            title_var.set("")
            genre_var.set("")
            duration_var.set("")
            release_date_var.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update movie: {e}")

    def on_delete_movie():
        """Handle deleting a movie."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a movie to delete!")
            return

        movie_id = tree.item(selected_item, "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this movie?")
        if confirm:
            try:
                delete_movie(movie_id)
                refresh_movies()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete movie: {e}")

    # Create a new window
    window = Toplevel()
    window.title("Manage Movies")
    window.geometry("800x400")

    # Input Fields
    Label(window, text="Title:").grid(row=0, column=0, padx=10, pady=10)
    Label(window, text="Genre:").grid(row=0, column=1, padx=10, pady=10)
    Label(window, text="Duration:").grid(row=0, column=2, padx=10, pady=10)
    Label(window, text="Release Date:").grid(row=0, column=3, padx=10, pady=10)

    title_var = StringVar()
    genre_var = StringVar()
    duration_var = StringVar()
    release_date_var = StringVar()

    Entry(window, textvariable=title_var).grid(row=1, column=0, padx=10, pady=10)
    Entry(window, textvariable=genre_var).grid(row=1, column=1, padx=10, pady=10)
    Entry(window, textvariable=duration_var).grid(row=1, column=2, padx=10, pady=10)
    Entry(window, textvariable=release_date_var).grid(row=1, column=3, padx=10, pady=10)

    # Buttons
    Button(window, text="Add Movie", command=on_add_movie).grid(row=2, column=0, padx=10, pady=10)
    Button(window, text="Update Movie", command=on_update_movie).grid(row=2, column=1, padx=10, pady=10)
    Button(window, text="Delete Movie", command=on_delete_movie).grid(row=2, column=2, padx=10, pady=10)

    # Movie List (Treeview)
    tree = ttk.Treeview(window, columns=("ID", "Title", "Genre", "Duration", "Release Date"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Genre", text="Genre")
    tree.heading("Duration", text="Duration")
    tree.heading("Release Date", text="Release Date")
    tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    # Populate the Treeview
    refresh_movies()

    # Configure column resizing
    window.grid_rowconfigure(3, weight=1)
    window.grid_columnconfigure(3, weight=1)

    window.mainloop()




# Manage bookings (admin only)
def manage_bookings():
    bookings_window = tk.Toplevel()
    bookings_window.title("Manage Bookings")
    
    tk.Label(bookings_window, text="Booking Management (Admin Only)", font=("Arial", 14)).pack(pady=10)
    tk.Label(bookings_window, text="Feature not implemented yet").pack(pady=20)



# Pop-up window with two options
def show_login_options():
    # Create the pop-up window
    popup = tk.Tk()
    popup.title("Login Options")
    
    # Add a label to the window
    tk.Label(popup, text="Select Login Type", font=("Arial", 14)).pack(pady=10)

    def function():
        popup.destroy()
        staff_login_screen()
        
    
    # Normal Login button
    def normal_login():
        print("Normal Login selected.")
        popup.destroy()  # Close the pop-up window
        run()

  

    tk.Button(popup, text="Normal Login", command=normal_login, width=20).pack(pady=10)
    
    # Staff Login button
    tk.Button(popup, text="Staff Login", command=function, width=20).pack(pady=10)
    
    # Run the pop-up window
    popup.mainloop()

# Run the pop-up window when this script is executed
if __name__ == "__main__":
    show_login_options()




def register_user():
    def submit_registration():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        conn = sqlite3.connect('cinema_system.db')
        cursor = conn.cursor()

        hashed_password = hash_password(password)

        try:
            cursor.execute(
                "INSERT INTO User (username, password_hash) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
            messagebox.showinfo("Success", "Registration successful")
            registration_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

    registration_window = tk.Toplevel(root)
    registration_window.title("Register")
    registration_window.geometry("400x300")

    tk.Label(registration_window, text="Register", font=("Arial", 20, "bold"), fg="blue").pack(pady=10)

    tk.Label(registration_window, text="Username:", font=("Arial", 12)).pack(anchor="w", padx=20)
    username_entry = tk.Entry(registration_window, font=("Arial", 12))
    username_entry.pack(padx=20, fill="x")

    tk.Label(registration_window, text="Password:", font=("Arial", 12)).pack(anchor="w", padx=20)
    password_entry = tk.Entry(registration_window, font=("Arial", 12), show="*")
    password_entry.pack(padx=20, fill="x")

    tk.Label(registration_window, text="Confirm Password:", font=("Arial", 12)).pack(anchor="w", padx=20)
    confirm_password_entry = tk.Entry(registration_window, font=("Arial", 12), show="*")
    confirm_password_entry.pack(padx=20, fill="x")

    tk.Button(registration_window, text="Register", font=("Arial", 12), bg="green", fg="white",
            command=submit_registration).pack(pady=20)

def login_user():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    conn = sqlite3.connect('cinema_system.db')
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "SELECT * FROM User WHERE username = ? AND password_hash = ?",
        (username, hashed_password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        open_customer_dashboard()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def open_customer_dashboard():
    customer_dashboard = tk.Toplevel(root)
    customer_dashboard.title("Customer Dashboard")
    customer_dashboard.geometry("600x400")

    tk.Label(customer_dashboard, text="Customer Dashboard", font=("Arial", 20, "bold"), fg="blue").pack(pady=10)

    # View Movies
    def view_movies():
        conn = sqlite3.connect('cinema_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
        conn.close()

        movies_window = tk.Toplevel(customer_dashboard)
        movies_window.title("Available Movies")
        movies_window.geometry("500x300")

        tk.Label(movies_window, text="Available Movies", font=("Arial", 16, "bold"), fg="blue").pack(pady=10)

        for movie in movies:
            movie_details = f"Title: {movie[1]}, Genre: {movie[2]}, Duration: {movie[3]} mins, Rating: {movie[4]}"
            tk.Label(movies_window, text=movie_details, font=("Arial", 12)).pack(anchor="w", padx=20)

    # Book Tickets
    def book_tickets():
        booking_window = tk.Toplevel(customer_dashboard)
        booking_window.title("Book Tickets")
        booking_window.geometry("400x400")

        tk.Label(booking_window, text="Book Tickets", font=("Arial", 16, "bold"), fg="blue").pack(pady=10)

        tk.Label(booking_window, text="Movie ID:", font=("Arial", 12)).pack(anchor="w", padx=20)
        movie_id_entry = tk.Entry(booking_window, font=("Arial", 12))
        movie_id_entry.pack(padx=20, fill="x")

        tk.Label(booking_window, text="Screening ID:", font=("Arial", 12)).pack(anchor="w", padx=20)
        screening_id_entry = tk.Entry(booking_window, font=("Arial", 12))
        screening_id_entry.pack(padx=20, fill="x")

        tk.Label(booking_window, text="Seats to Book:", font=("Arial", 12)).pack(anchor="w", padx=20)
        seats_entry = tk.Entry(booking_window, font=("Arial", 12))
        seats_entry.pack(padx=20, fill="x")

        def submit_booking():
            movie_id = movie_id_entry.get()
            screening_id = screening_id_entry.get()
            seats = seats_entry.get()

            if not movie_id or not screening_id or not seats:
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                seats = int(seats)
            except ValueError:
                messagebox.showerror("Error", "Seats must be a number")
                return

            conn = sqlite3.connect('cinema_system.db')
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "INSERT INTO Booking (customer_id, screening_id, seats_booked) VALUES (?, ?, ?)",
                    (1, screening_id, seats)  # Replace '1' with logged-in customer ID
                )
                conn.commit()
                messagebox.showinfo("Success", "Booking successful")
                booking_window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Invalid Screening ID or insufficient seats")
            finally:
                conn.close()

        tk.Button(booking_window, text="Book", font=("Arial", 12), bg="green", fg="white", command=submit_booking).pack(pady=20)

    # View Booking History
    def view_booking_history():
        conn = sqlite3.connect('cinema_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Booking WHERE customer_id = ?", (1,))  # Replace '1' with logged-in customer ID
        bookings = cursor.fetchall()
        conn.close()

        history_window = tk.Toplevel(customer_dashboard)
        history_window.title("Booking History")
        history_window.geometry("500x300")

        tk.Label(history_window, text="Booking History", font=("Arial", 16, "bold"), fg="blue").pack(pady=10)

        for booking in bookings:
            booking_details = f"Booking ID: {booking[0]}, Screening ID: {booking[2]}, Seats: {booking[3]}, Date: {booking[4]}"
            tk.Label(history_window, text=booking_details, font=("Arial", 12)).pack(anchor="w", padx=20)

    tk.Button(customer_dashboard, text="View Movies", font=("Arial", 12), bg="blue", fg="white", command=view_movies).pack(pady=10)
    tk.Button(customer_dashboard, text="Book Tickets", font=("Arial", 12), bg="green", fg="white", command=book_tickets).pack(pady=10)
    tk.Button(customer_dashboard, text="View Booking History", font=("Arial", 12), bg="purple", fg="white", command=view_booking_history).pack(pady=10)


root = tk.Tk()
root.title("Cinema System Login")
root.geometry("400x300")

# Styling
root.configure(bg="#f5f5f5")

# Title Label
tk.Label(root, text="Cinema System", font=("Arial", 24, "bold"), fg="blue", bg="#f5f5f5").pack(pady=10)

# Username Label and Entry
tk.Label(root, text="Username:", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", padx=20)
username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.pack(padx=20, fill="x")

# Password Label and Entry
tk.Label(root, text="Password:", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", padx=20)
password_entry = tk.Entry(root, font=("Arial", 12), show="*")
password_entry.pack(padx=20, fill="x")

# Login Button
tk.Button(root, text="Login", font=("Arial", 12), bg="blue", fg="white", command=login_user).pack(pady=10)

# Register Button
tk.Button(root, text="Register", font=("Arial", 12), bg="green", fg="white", command=register_user).pack()
import tkinter as tk


root.mainloop()