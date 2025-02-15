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
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
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

    # Create Bookings Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            seat_number TEXT NOT NULL,
            booking_time TEXT NOT NULL,
            FOREIGN KEY(movie_id) REFERENCES Movies(id) ON DELETE CASCADE
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
    
    cursor.execute("SELECT COUNT(*) FROM Movies")
    count = cursor.fetchone()[0]
    
    if count == 0:
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
            ("Gladiator", "Action", 155, "2000-05-05"),
        ]

        cursor.executemany("INSERT INTO Movies (title, genre, duration, release_date) VALUES (?, ?, ?, ?)", movies)
        conn.commit()
        print("✅ Movies have been successfully added to the database!")
    else:
        print(f"✅ Movies already exist in the database ({count} found).")
    
    conn.close()

if __name__ == "__main__":
    initialize_database()
    populate_movies()
    print("Database initialized and checked for movies.")
