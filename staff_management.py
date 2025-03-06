import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import bcrypt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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

def initialize_database():
    """Creates the necessary database tables if they don't exist."""
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    
    # Create Movies table with the correct schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            duration INTEGER NOT NULL,
            release_date TEXT NOT NULL
        )
    """)
    
    # Create User table with all required fields
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            is_staff INTEGER DEFAULT 0
        )
    """)
    
    # Create Staff table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
        )
    """)
    
    # Create Showtimes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Showtimes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            show_date TEXT NOT NULL,
            show_time TEXT NOT NULL,
            hall_number INTEGER NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            available_seats INTEGER NOT NULL,
            FOREIGN KEY(movie_id) REFERENCES Movies(id) ON DELETE CASCADE
        )
    """)
    
    # Create Bookings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            showtime_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            seat_number TEXT NOT NULL,
            booking_time TEXT NOT NULL,
            FOREIGN KEY(showtime_id) REFERENCES Showtimes(id) ON DELETE CASCADE
        )
    """)
    
    # Create Reviews table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            review TEXT,
            FOREIGN KEY(user_id) REFERENCES User(id) ON DELETE CASCADE,
            FOREIGN KEY(movie_id) REFERENCES Movies(id) ON DELETE CASCADE
        )
    """)
    
    # Check if admin user exists
    cursor.execute("SELECT COUNT(*) FROM Staff WHERE username = 'admin'")
    admin_exists = cursor.fetchone()[0] > 0
    
    # Add default admin user only if it doesn't exist
    if not admin_exists:
        username = "admin"
        password = "admin123"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("""
            INSERT INTO Staff (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, hashed_password, 'admin'))
    
    # Commit all changes
    conn.commit()
    conn.close()
    print("✅ Database initialized with default admin user (username: admin, password: admin123)")

def populate_test_data():
    """Adds sample bookings to the database for testing."""
    # First, ensure tables exist with correct schema
    initialize_database()
    
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    
    try:
        # First, let's make sure we have some movies with all required fields
        movies = [
            ("The Dark Knight", "Action", 152, "2008-07-18"),
            ("Inception", "Sci-Fi", 148, "2010-07-16"),
            ("The Shawshank Redemption", "Drama", 142, "1994-09-23"),
            ("Pulp Fiction", "Crime", 154, "1994-10-14"),
            ("The Matrix", "Sci-Fi", 136, "1999-03-31")
        ]
        
        # Clear existing movies
        cursor.execute("DELETE FROM Movies")
        cursor.executemany("""
            INSERT INTO Movies (title, genre, duration, release_date) 
            VALUES (?, ?, ?, ?)
        """, movies)
        
        # Add some test users with all required fields
        test_users = [
            ("john_doe", "password123", "john@example.com", 0),
            ("jane_smith", "password123", "jane@example.com", 0),
            ("admin_user", "admin123", "admin@example.com", 1)
        ]
        
        cursor.execute("DELETE FROM User")
        cursor.executemany("""
            INSERT INTO User (username, password, email, is_staff) 
            VALUES (?, ?, ?, ?)
        """, test_users)
        
        # Add showtimes for each movie
        from datetime import datetime, timedelta
        import random
        
        cursor.execute("SELECT id FROM Movies")
        movie_ids = [row[0] for row in cursor.fetchall()]
        
        showtimes = []
        today = datetime.now().date()
        
        for movie_id in movie_ids:
            for day in range(7):
                show_date = today + timedelta(days=day)
                for time in ["10:00", "14:00", "18:00"]:
                    showtimes.append((
                        movie_id,
                        show_date.strftime("%Y-%m-%d"),
                        time,
                        (movie_id % 3) + 1,  # Hall number (1-3)
                        12.99,  # Price
                        50  # Available seats
                    ))
        
        cursor.execute("DELETE FROM Showtimes")
        cursor.executemany("""
            INSERT INTO Showtimes (movie_id, show_date, show_time, hall_number, price, available_seats)
            VALUES (?, ?, ?, ?, ?, ?)
        """, showtimes)
        
        # Generate some sample bookings
        cursor.execute("SELECT id FROM Showtimes")
        showtime_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id, username FROM User")
        users = cursor.fetchall()
        
        # Generate bookings
        for i in range(20):
            showtime_id = random.choice(showtime_ids)
            if random.random() > 0.3:  # 70% chance of registered user
                user = random.choice(users)
                customer_name = user[1]
            else:
                customer_name = random.choice(["Guest User", "Walk-in Customer", "Anonymous", "Cinema Guest"])
            
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)
            booking_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
            seat_number = f"{random.choice('ABCDE')}{random.randint(1, 10)}"
            
            cursor.execute("""
                INSERT INTO Bookings (showtime_id, customer_name, seat_number, booking_time)
                VALUES (?, ?, ?, ?)
            """, (showtime_id, customer_name, seat_number, booking_time.strftime("%Y-%m-%d %H:%M:%S")))
            
            # Update available seats
            cursor.execute("""
                UPDATE Showtimes 
                SET available_seats = available_seats - 1 
                WHERE id = ?
            """, (showtime_id,))
        
        conn.commit()
        messagebox.showinfo("Success", "Test data has been added to the database!")
        
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
    finally:
        conn.close()

def check_bookings():
    """Checks the current bookings in the database."""
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    
    try:
        # Check total number of bookings
        cursor.execute("SELECT COUNT(*) FROM Bookings")
        total_bookings = cursor.fetchone()[0]
        print(f"Total bookings in database: {total_bookings}")
        
        # Get some sample bookings
        cursor.execute("""
            SELECT 
                Bookings.id,
                Movies.title,
                Bookings.customer_name,
                Bookings.seat_number,
                Showtimes.show_date,
                Showtimes.show_time,
                Showtimes.price
            FROM Bookings
            JOIN Showtimes ON Bookings.showtime_id = Showtimes.id
            JOIN Movies ON Showtimes.movie_id = Movies.id
            ORDER BY Bookings.booking_time DESC
            LIMIT 5
        """)
        
        recent_bookings = cursor.fetchall()
        print("\nMost recent bookings:")
        for booking in recent_bookings:
            print(f"ID: {booking[0]}")
            print(f"Movie: {booking[1]}")
            print(f"Customer: {booking[2]}")
            print(f"Seat: {booking[3]}")
            print(f"Date: {booking[4]}")
            print(f"Time: {booking[5]}")
            print(f"Price: £{booking[6]:.2f}")
            print("-" * 50)
            
    except sqlite3.Error as e:
        print(f"Error checking bookings: {e}")
    finally:
        conn.close()

def show_analytics():
    """Shows analytics dashboard with booking statistics and graphs."""
    analytics_window = tk.Toplevel()
    analytics_window.title("Cinema Analytics")
    analytics_window.geometry("1200x800")
    analytics_window.configure(bg="#2C3E50")

    # Title
    tk.Label(analytics_window, text="Cinema Analytics Dashboard", 
            font=("Arial", 16, "bold"), fg="white", bg="#2C3E50").pack(pady=10)

    # Create main frame
    main_frame = tk.Frame(analytics_window, bg="#2C3E50")
    main_frame.pack(expand=True, fill="both", padx=20, pady=10)

    # Stats frame
    stats_frame = tk.Frame(main_frame, bg="#2C3E50")
    stats_frame.pack(fill="x", pady=10)

    # Graphs frame
    graphs_frame = tk.Frame(main_frame, bg="#2C3E50")
    graphs_frame.pack(fill="both", expand=True, pady=10)

    def get_analytics_data():
        """Fetches analytics data from the database."""
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        
        try:
            # Total bookings
            cursor.execute("SELECT COUNT(*) FROM Bookings")
            total_bookings = cursor.fetchone()[0]
            
            # Total revenue
            cursor.execute("""
                SELECT SUM(s.price)
                FROM Bookings b
                JOIN Showtimes s ON b.showtime_id = s.id
            """)
            total_revenue = cursor.fetchone()[0] or 0
            
            # Most popular movie
            cursor.execute("""
                SELECT m.title, COUNT(*) as booking_count
                FROM Bookings b
                JOIN Showtimes s ON b.showtime_id = s.id
                JOIN Movies m ON s.movie_id = m.id
                GROUP BY m.id, m.title
                ORDER BY booking_count DESC
                LIMIT 1
            """)
            popular_movie = cursor.fetchone() or ("No bookings", 0)
            
            # Today's bookings
            cursor.execute("""
                SELECT COUNT(*)
                FROM Bookings b
                JOIN Showtimes s ON b.showtime_id = s.id
                WHERE date(b.booking_time) = date('now')
            """)
            todays_bookings = cursor.fetchone()[0]
            
            # Available seats
            cursor.execute("SELECT SUM(available_seats) FROM Showtimes WHERE show_date >= date('now')")
            available_seats = cursor.fetchone()[0] or 0
            
            # Occupancy rate
            cursor.execute("""
                SELECT 
                    CAST(COUNT(*) AS FLOAT) / 
                    (SELECT COUNT(*) FROM Showtimes WHERE show_date >= date('now')) 
                FROM Bookings b
                JOIN Showtimes s ON b.showtime_id = s.id
                WHERE s.show_date >= date('now')
            """)
            occupancy_rate = (cursor.fetchone()[0] or 0) * 100

            # Get booking trends for the last 7 days
            cursor.execute("""
                SELECT date(booking_time), COUNT(*) as count
                FROM Bookings
                WHERE booking_time >= date('now', '-7 days')
                GROUP BY date(booking_time)
                ORDER BY date(booking_time)
            """)
            booking_trends = cursor.fetchall()

            # Get movie popularity data
            cursor.execute("""
                SELECT m.title, COUNT(*) as booking_count
                FROM Bookings b
                JOIN Showtimes s ON b.showtime_id = s.id
                JOIN Movies m ON s.movie_id = m.id
                GROUP BY m.id, m.title
                ORDER BY booking_count DESC
                LIMIT 5
            """)
            movie_popularity = cursor.fetchall()
            
            return {
                "total_bookings": total_bookings,
                "total_revenue": total_revenue,
                "popular_movie": popular_movie,
                "todays_bookings": todays_bookings,
                "available_seats": available_seats,
                "occupancy_rate": occupancy_rate,
                "booking_trends": booking_trends,
                "movie_popularity": movie_popularity
            }
            
        finally:
            conn.close()

    def create_stat_panel(parent, title, value, row, column):
        """Creates a styled panel for displaying statistics."""
        panel = tk.Frame(parent, bg="#34495E", padx=15, pady=10)
        panel.grid(row=row, column=column, padx=10, pady=5, sticky="nsew")
        
        tk.Label(panel, text=title, font=("Arial", 12), fg="#BDC3C7", bg="#34495E").pack()
        tk.Label(panel, text=str(value), font=("Arial", 14, "bold"), fg="white", bg="#34495E").pack()
        
        return panel

    def create_graphs(data):
        """Creates and displays graphs."""
        # Clear existing graphs
        for widget in graphs_frame.winfo_children():
            widget.destroy()

        # Create figure with two subplots
        fig = Figure(figsize=(12, 6), facecolor="#2C3E50")
        fig.patch.set_facecolor("#2C3E50")

        # Booking trends graph
        ax1 = fig.add_subplot(121)
        dates = [row[0] for row in data["booking_trends"]]
        counts = [row[1] for row in data["booking_trends"]]
        ax1.plot(dates, counts, marker='o', color='#3498DB', linewidth=2)
        ax1.set_title('Booking Trends (Last 7 Days)', color='white', pad=20)
        ax1.set_xlabel('Date', color='white')
        ax1.set_ylabel('Number of Bookings', color='white')
        ax1.tick_params(colors='white')
        ax1.set_facecolor("#34495E")
        plt.setp(ax1.get_xticklabels(), rotation=45)

        # Movie popularity graph
        ax2 = fig.add_subplot(122)
        movies = [row[0] for row in data["movie_popularity"]]
        bookings = [row[1] for row in data["movie_popularity"]]
        ax2.bar(movies, bookings, color='#3498DB')
        ax2.set_title('Top 5 Movies by Bookings', color='white', pad=20)
        ax2.set_xlabel('Movie', color='white')
        ax2.set_ylabel('Number of Bookings', color='white')
        ax2.tick_params(colors='white')
        ax2.set_facecolor("#34495E")
        plt.setp(ax2.get_xticklabels(), rotation=45)

        # Adjust layout and display
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh_analytics():
        """Updates the analytics display."""
        data = get_analytics_data()
        
        # Configure grid
        for i in range(2):
            stats_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Create stat panels
        create_stat_panel(stats_frame, "Total Bookings", data["total_bookings"], 0, 0)
        create_stat_panel(stats_frame, "Total Revenue", f"£{data['total_revenue']:.2f}", 0, 1)
        create_stat_panel(stats_frame, "Most Popular Movie", f"{data['popular_movie'][0]}\n({data['popular_movie'][1]} bookings)", 0, 2)
        create_stat_panel(stats_frame, "Today's Bookings", data["todays_bookings"], 1, 0)
        create_stat_panel(stats_frame, "Available Seats", data["available_seats"], 1, 1)
        create_stat_panel(stats_frame, "Occupancy Rate", f"{data['occupancy_rate']:.1f}%", 1, 2)

        # Create graphs
        create_graphs(data)

    # Add refresh button
    button_frame = tk.Frame(analytics_window, bg="#2C3E50")
    button_frame.pack(fill="x", pady=10)
    
    tk.Button(button_frame, text="Refresh Analytics", 
              command=refresh_analytics,
              bg="#3498DB", fg="white", 
              font=("Arial", 10)).pack(pady=5)

    # Initial load of analytics
    refresh_analytics()

def show_booking_management():
    """Displays all bookings with management options."""
    booking_window = tk.Tk()
    booking_window.title("Booking Management")
    booking_window.geometry("1000x600")
    booking_window.configure(bg="#2C3E50")

    # Title
    tk.Label(booking_window, text="Booking Management", 
            font=("Arial", 16, "bold"), fg="white", bg="#2C3E50").pack(pady=10)

    # Create Treeview
    columns = ("ID", "Movie", "Customer", "Seat", "Date", "Time", "Price")
    tree = ttk.Treeview(booking_window, columns=columns, show='headings', height=20)
    
    # Configure column headings and widths
    widths = {
        "ID": 50,
        "Movie": 200,
        "Customer": 150,
        "Seat": 80,
        "Date": 100,
        "Time": 100,
        "Price": 80
    }
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=widths.get(col, 120))
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(booking_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack the Treeview and scrollbar
    tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
    scrollbar.pack(side="right", fill="y", pady=5)

    def refresh_bookings():
        """Refresh the booking list with detailed information."""
        for item in tree.get_children():
            tree.delete(item)
            
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                Bookings.id,
                Movies.title,
                Bookings.customer_name,
                Bookings.seat_number,
                Showtimes.show_date,
                Showtimes.show_time,
                Showtimes.price
            FROM Bookings
            JOIN Showtimes ON Bookings.showtime_id = Showtimes.id
            JOIN Movies ON Showtimes.movie_id = Movies.id
            ORDER BY Showtimes.show_date, Showtimes.show_time
        """)
        
        bookings = cursor.fetchall()
        conn.close()
        
        for booking in bookings:
            # Format price as currency
            price = f"£{booking[6]:.2f}" if booking[6] is not None else "N/A"
            
            # Insert booking data into treeview
            tree.insert("", "end", values=(
                booking[0],          # ID
                booking[1],          # Movie Title
                booking[2],          # Customer Name
                booking[3],          # Seat Number
                booking[4],          # Date
                booking[5],          # Time
                price               # Price
            ))
    
    def delete_booking():
        """Deletes the selected booking."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a booking to delete.")
            return
        
        booking_id = tree.item(selected_item[0])['values'][0]
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this booking?"):
            conn = sqlite3.connect("cinema_system.db")
            cursor = conn.cursor()
            
            # Get the showtime_id before deleting the booking
            cursor.execute("SELECT showtime_id FROM Bookings WHERE id = ?", (booking_id,))
            showtime_id = cursor.fetchone()[0]
            
            # Delete the booking
            cursor.execute("DELETE FROM Bookings WHERE id = ?", (booking_id,))
            
            # Update available seats
            cursor.execute("""
                UPDATE Showtimes 
                SET available_seats = available_seats + 1 
                WHERE id = ?
            """, (showtime_id,))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Booking deleted successfully!")
            refresh_bookings()
    
    # Control buttons frame
    button_frame = tk.Frame(booking_window, bg="#2C3E50")
    button_frame.pack(fill="x", padx=10, pady=5)
    
    # Add styled buttons
    button_style = {"bg": "#3498DB", "fg": "white", "font": ("Arial", 10), "width": 15, "height": 2}
    
    tk.Button(button_frame, text="Refresh Bookings", command=refresh_bookings, **button_style).pack(side="left", padx=5)
    tk.Button(button_frame, text="Delete Selected", command=delete_booking, **button_style).pack(side="left", padx=5)
    tk.Button(button_frame, text="View Analytics", command=show_analytics, **button_style).pack(side="left", padx=5)
    
    # Initial load of bookings
    refresh_bookings()
    
    booking_window.mainloop()


