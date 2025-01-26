import sqlite3

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('cinema_system.db')
    
    # Enable foreign key support
    conn.execute("PRAGMA foreign_keys = ON")

    # Create a cursor object
    cursor = conn.cursor()
    
    # Create Customer table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT
        )
    ''')

    # Staff table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'staff'
        )
    ''')


    # Create Manager table, which references Employee as the manager
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Manager (
            manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            department TEXT NOT NULL,
            start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES Employee(employee_id) ON DELETE CASCADE
        )
    ''')

    # Movies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT,
            duration INTEGER,
            release_date TEXT
        )
    ''')

    # Create Screening table to track movie screenings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Screening (
            screening_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            screening_time TIMESTAMP NOT NULL,
            available_seats INTEGER NOT NULL,
            FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE
        )
    ''')

    # Bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER,
            customer_name TEXT,
            seat_number TEXT,
            booking_time TEXT,
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        )
    ''')


    # Create Payment table to track payment information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Payment (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,  -- e.g., Card, Cash, Online
            payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (booking_id) REFERENCES Booking(booking_id) ON DELETE CASCADE
        )
    ''')

    # Create Review table to store movie reviews by customers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Review (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
            FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE
        )
    ''')

    # Create User table for account registration
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            customer_id INTEGER,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def add_default_admin():
    conn = sqlite3.connect("cinema_system.db")  # Use the correct database name
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO staff (username, password, role) VALUES (?, ?, ?)", 
                   ('admin', 'admin123', 'admin'))
    conn.commit()
    conn.close()

add_default_admin()
if __name__ == '__main__':
    create_database()
    print("Cinema database and tables created successfully.")
