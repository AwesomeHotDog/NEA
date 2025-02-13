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
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute("INSERT INTO Staff (username, password_hash, role) VALUES (?, ?, ?)",
                       (username, hashed_password, 'admin'))
        print("✅ Default Admin Created: Username = admin, Password = admin123")

if __name__ == "__main__":
    initialize_database()
    print("✅ Database initialized successfully.")
