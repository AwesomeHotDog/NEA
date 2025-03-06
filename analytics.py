import matplotlib.pyplot as plt
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from datetime import datetime, timedelta

def show_analytics():
    """Displays analytics in a Tkinter window with multiple charts."""
    # Create main window
    analytics_window = tk.Tk()
    analytics_window.title("Cinema Analytics")
    analytics_window.geometry("1000x800")
    analytics_window.configure(bg='#2C3E50')

    # Title
    tk.Label(analytics_window, text="Cinema Analytics Dashboard", 
             font=("Arial", 16, "bold"), fg="white", bg="#2C3E50").pack(pady=10)

    def create_charts():
        # Create figure for the plots
        fig = Figure(figsize=(12, 10), facecolor='#2C3E50')
        
        # Movie Bookings Chart
        ax1 = fig.add_subplot(221)  # Changed to 2x2 grid
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        
        # Fetch movie bookings with actual movie titles
        cursor.execute("""
            SELECT Movies.title, COUNT(Bookings.id) 
            FROM Bookings 
            JOIN Movies ON Bookings.movie_id = Movies.id 
            GROUP BY Movies.title
            ORDER BY COUNT(Bookings.id) DESC
            LIMIT 5
        """)
        data = cursor.fetchall()

        if data:
            movie_titles = [row[0] for row in data]
            booking_counts = [row[1] for row in data]
            
            bars = ax1.bar(movie_titles, booking_counts, color='#3498DB')
            ax1.set_xlabel("Movies", color='white')
            ax1.set_ylabel("Number of Bookings", color='white')
            ax1.set_title("Top 5 Movies by Bookings", color='white', pad=20)
            ax1.tick_params(axis='x', rotation=45, colors='white')
            ax1.tick_params(axis='y', colors='white')
            ax1.set_facecolor('#34495E')
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', color='white')
        
        # Daily Revenue Chart
        ax2 = fig.add_subplot(222)  # Changed to 2x2 grid
        cursor.execute("""
            SELECT date(booking_time) as booking_date, 
                   COUNT(*) as num_bookings,
                   SUM(price) as total_revenue
            FROM Bookings
            WHERE booking_time >= date('now', '-7 days')
            GROUP BY booking_date
            ORDER BY booking_date
        """)
        revenue_data = cursor.fetchall()

        if revenue_data:
            dates = [row[0] for row in revenue_data]
            revenues = [row[2] if row[2] is not None else 0 for row in revenue_data]
            
            line = ax2.plot(dates, revenues, marker='o', color='#2ECC71', linewidth=2)
            ax2.set_xlabel("Date", color='white')
            ax2.set_ylabel("Revenue (£)", color='white')
            ax2.set_title("Daily Revenue (Last 7 Days)", color='white', pad=20)
            ax2.tick_params(axis='x', rotation=45, colors='white')
            ax2.tick_params(axis='y', colors='white')
            ax2.set_facecolor('#34495E')
            
            # Add value labels on data points
            for x, y in zip(dates, revenues):
                ax2.text(x, y, f'£{y:.2f}', ha='center', va='bottom', color='white')

        # User Booking Patterns
        ax3 = fig.add_subplot(223)  # Added new subplot
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN User.username IS NOT NULL THEN User.username 
                    ELSE 'Guest' 
                END as user_type,
                COUNT(*) as booking_count
            FROM Bookings
            LEFT JOIN User ON Bookings.user_id = User.id
            GROUP BY user_type
            ORDER BY booking_count DESC
            LIMIT 5
        """)
        user_data = cursor.fetchall()

        if user_data:
            usernames = [row[0] for row in user_data]
            user_bookings = [row[1] for row in user_data]
            
            bars = ax3.bar(usernames, user_bookings, color='#E74C3C')
            ax3.set_xlabel("Users", color='white')
            ax3.set_ylabel("Number of Bookings", color='white')
            ax3.set_title("Top Users by Bookings", color='white', pad=20)
            ax3.tick_params(axis='x', rotation=45, colors='white')
            ax3.tick_params(axis='y', colors='white')
            ax3.set_facecolor('#34495E')
            
            for bar in bars:
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', color='white')

        # Booking Time Distribution
        ax4 = fig.add_subplot(224)  # Added new subplot
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN strftime('%H', booking_time) BETWEEN '00' AND '05' THEN 'Night (00-05)'
                    WHEN strftime('%H', booking_time) BETWEEN '06' AND '11' THEN 'Morning (06-11)'
                    WHEN strftime('%H', booking_time) BETWEEN '12' AND '17' THEN 'Afternoon (12-17)'
                    ELSE 'Evening (18-23)'
                END as time_period,
                COUNT(*) as booking_count
            FROM Bookings
            GROUP BY time_period
            ORDER BY booking_count DESC
        """)
        time_data = cursor.fetchall()
        conn.close()

        if time_data:
            time_periods = [row[0] for row in time_data]
            time_counts = [row[1] for row in time_data]
            
            pie = ax4.pie(time_counts, labels=time_periods, autopct='%1.1f%%', 
                         colors=['#3498DB', '#2ECC71', '#E74C3C', '#F1C40F'])
            ax4.set_title("Booking Time Distribution", color='white', pad=20)
            ax4.set_facecolor('#34495E')

        fig.tight_layout(pad=3.0)
        return fig

    # Create initial charts
    fig = create_charts()
    
    # Create canvas and add to window
    canvas = FigureCanvasTkAgg(fig, master=analytics_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

    def refresh_data():
        """Refreshes the analytics data."""
        fig.clear()
        new_fig = create_charts()
        canvas.figure = new_fig
        canvas.draw()

    # Refresh button
    tk.Button(analytics_window, text="Refresh Data", 
              command=refresh_data,
              bg="#3498DB", fg="white",
              font=("Arial", 10)).pack(pady=10)
    
    analytics_window.mainloop()
