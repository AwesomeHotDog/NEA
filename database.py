import sqlite3
import bcrypt

def initialize_database():
    """Creates the database and tables if they don't exist."""
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create User Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_staff INTEGER DEFAULT 0,
            email TEXT UNIQUE
        )
    """)

    # Create Staff Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
        )
    """)

    # Create Movies Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            duration INTEGER NOT NULL,
            release_date TEXT NOT NULL
        )
    """)

    # Create Showtimes Table
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

    # Create Bookings Table
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

    # Create Reviews Table
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

    # Commit table creation
    conn.commit()

    # Add default admin user
    add_admin_user(cursor)

    # Close connection
    conn.commit()
    conn.close()

def add_admin_user(cursor):
    """Adds a default admin user if no staff exist."""
    cursor.execute("SELECT COUNT(*) FROM Staff")
    count = cursor.fetchone()[0]

    if count == 0:  # If no staff exist, create an admin user
        username = "admin"
        password = "admin123"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  
        cursor.execute("INSERT INTO Staff (username, password_hash, role) VALUES (?, ?, ?)",
                       (username, hashed_password, 'admin'))
        print("✅ Default Admin Created: Username = admin, Password = admin123")

def populate_movies():
    """Inserts sample movies if the database is empty."""
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    
    # Check if movies exist
    cursor.execute("SELECT COUNT(*) FROM Movies")
    movie_count = cursor.fetchone()[0]
    
    if movie_count == 0:
        movies = [
            ("Inception", "Sci-Fi", 148, "2010-07-16"),
            ("The Dark Knight", "Action", 152, "2008-07-18"),
            ("Interstellar", "Sci-Fi", 169, "2014-11-07"),
            ("Titanic", "Romance", 195, "1997-12-19"),
            ("Avengers: Endgame", "Action", 181, "2019-04-26"),
            ("Joker", "Drama", 122, "2019-10-04"),
            ("The Matrix", "Sci-Fi", 136, "1999-03-31"),
            ("The Godfather", "Crime", 175, "1972-03-24"),
            ("The Shawshank Redemption", "Drama", 142, "1994-09-23"),
            ("Pulp Fiction", "Crime", 154, "1994-10-14"),
            ("Forrest Gump", "Drama", 142, "1994-07-06"),
            ("Gladiator", "Action", 155, "2000-05-05")
        ]

        cursor.executemany("""
            INSERT INTO Movies (title, genre, duration, release_date) 
            VALUES (?, ?, ?, ?)
        """, movies)
        print("✅ Movies have been successfully added to the database!")
    else:
        print(f"✅ Movies already exist in the database ({movie_count} found).")

    # Check if showtimes exist
    cursor.execute("SELECT COUNT(*) FROM Showtimes")
    showtime_count = cursor.fetchone()[0]
    
    if showtime_count == 0:
        # Get all movie IDs
        cursor.execute("SELECT id FROM Movies")
        movie_ids = [row[0] for row in cursor.fetchall()]
        
        # Generate showtimes for the next 7 days
        from datetime import datetime, timedelta
        today = datetime.now().date()
        showtimes = []
        
        for movie_id in movie_ids:
            for day in range(7):
                show_date = today + timedelta(days=day)
                # Add 3 showtimes per day
                for time in ["10:00", "14:00", "18:00"]:
                    showtimes.append((
                        movie_id,
                        show_date.strftime("%Y-%m-%d"),
                        time,
                        (movie_id % 3) + 1,  # Hall number (1-3)
                        12.99,  # Price
                        50  # Available seats
                    ))
        
        cursor.executemany("""
            INSERT INTO Showtimes (movie_id, show_date, show_time, hall_number, price, available_seats)
            VALUES (?, ?, ?, ?, ?, ?)
        """, showtimes)
        
        conn.commit()
        print("✅ Showtimes have been successfully added to the database!")
    else:
        print(f"✅ Showtimes already exist in the database ({showtime_count} found).")
    
    conn.close()

if __name__ == "__main__":
    initialize_database()
    populate_movies()
    print("Database initialized and checked for movies and showtimes.")
