import matplotlib.pyplot as plt
import sqlite3

def generate_sales_report():
    """Displays a bar chart of movie bookings with movie titles."""
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    
    # Fetch movie bookings with actual movie titles
    cursor.execute("""
        SELECT Movies.title, COUNT(Bookings.id) 
        FROM Bookings 
        JOIN Movies ON Bookings.movie_id = Movies.id 
        GROUP BY Movies.title
    """)
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No bookings found.")
        return

    movie_titles = [row[0] for row in data]  # Extract movie titles
    booking_counts = [row[1] for row in data]  # Extract booking counts

    plt.bar(movie_titles, booking_counts)
    plt.xlabel("Movies")
    plt.ylabel("Number of Bookings")
    plt.title("Movie Booking Report")
    plt.xticks(rotation=45, ha='right')  # Rotate movie titles for better visibility
    plt.tight_layout()
    plt.show()
