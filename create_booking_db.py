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

    # Create Employee table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            position TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            hire_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    # Create Movie table to store information about the movies being shown
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Movie (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            duration INTEGER NOT NULL,  -- in minutes
            rating TEXT NOT NULL  -- e.g., PG, PG-13, R
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

    # Create Booking table for customer ticket bookings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Booking (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            screening_id INTEGER NOT NULL,
            seats_booked INTEGER NOT NULL,
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
            FOREIGN KEY (screening_id) REFERENCES Screening(screening_id) ON DELETE CASCADE
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

    # Create Food table to store available food items in the cinema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Food (
            food_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')

    # Create FoodOrder table to track food orders placed by customers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FoodOrder (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            food_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
            FOREIGN KEY (food_id) REFERENCES Food(food_id) ON DELETE CASCADE
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Cinema database and tables created successfully.")


