import sqlite3
import tkinter as tk

def show_analytics():
    """Displays booking and review analytics."""
    analytics_window = tk.Toplevel()
    analytics_window.title("Analytics Dashboard")
    analytics_window.geometry("400x300")

    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Bookings")
    total_bookings = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Reviews")
    total_reviews = cursor.fetchone()[0]

    cursor.execute("SELECT title FROM Movies WHERE id IN (SELECT movie_id FROM Reviews GROUP BY movie_id ORDER BY COUNT(*) DESC LIMIT 1)")
    top_movie = cursor.fetchone()
    top_movie_title = top_movie[0] if top_movie else "No reviews yet"

    conn.close()

    tk.Label(analytics_window, text=f"Total Bookings: {total_bookings}").pack(pady=10)
    tk.Label(analytics_window, text=f"Total Reviews: {total_reviews}").pack(pady=10)
    tk.Label(analytics_window, text=f"Most Reviewed Movie: {top_movie_title}").pack(pady=10)
