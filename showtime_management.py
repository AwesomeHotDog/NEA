import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

def show_schedule():
    """Displays the movie schedule for the next 7 days."""
    schedule_window = tk.Toplevel()
    schedule_window.title("Movie Schedule")
    schedule_window.geometry("1000x600")
    schedule_window.configure(bg="#2A2A2A")  # Dark theme

    # Create main container frame
    main_frame = tk.Frame(schedule_window, bg="#2A2A2A")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Create Treeview for schedule
    columns = ("Date", "Time", "Movie", "Hall", "Price", "Available Seats")
    schedule_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
    
    # Configure columns
    for col in columns:
        schedule_tree.heading(col, text=col)
        schedule_tree.column(col, width=150)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=schedule_tree.yview)
    schedule_tree.configure(yscrollcommand=scrollbar.set)

    # Pack the Treeview and scrollbar
    schedule_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Load schedule data
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    
    # Get today's date and 7 days from now
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    
    cursor.execute("""
        SELECT s.show_date, s.show_time, m.title, s.hall_number, s.price, s.available_seats
        FROM Showtimes s
        JOIN Movies m ON s.movie_id = m.id
        WHERE s.show_date BETWEEN ? AND ?
        ORDER BY s.show_date, s.show_time
    """, (today.strftime("%Y-%m-%d"), next_week.strftime("%Y-%m-%d")))
    
    schedule_data = cursor.fetchall()
    conn.close()

    # Insert data into Treeview
    for row in schedule_data:
        schedule_tree.insert("", "end", values=row)

    # Add filter frame
    filter_frame = tk.Frame(schedule_window, bg="#2A2A2A")
    filter_frame.pack(fill="x", padx=20, pady=10)

    # Date filter
    tk.Label(filter_frame, text="Filter by Date:", fg="white", bg="#2A2A2A").pack(side="left", padx=5)
    date_var = tk.StringVar()
    date_combo = ttk.Combobox(filter_frame, textvariable=date_var, values=["All"] + [d[0] for d in schedule_data], state="readonly")
    date_combo.pack(side="left", padx=5)
    date_combo.set("All")

    # Movie filter
    tk.Label(filter_frame, text="Filter by Movie:", fg="white", bg="#2A2A2A").pack(side="left", padx=5)
    movie_var = tk.StringVar()
    movie_combo = ttk.Combobox(filter_frame, textvariable=movie_var, values=["All"] + list(set(d[2] for d in schedule_data)), state="readonly")
    movie_combo.pack(side="left", padx=5)
    movie_combo.set("All")

    def apply_filters():
        """Apply filters to the schedule view."""
        # Clear current items
        for item in schedule_tree.get_children():
            schedule_tree.delete(item)

        # Get filter values
        selected_date = date_var.get()
        selected_movie = movie_var.get()

        # Filter data
        filtered_data = schedule_data
        if selected_date != "All":
            filtered_data = [d for d in filtered_data if d[0] == selected_date]
        if selected_movie != "All":
            filtered_data = [d for d in filtered_data if d[2] == selected_movie]

        # Insert filtered data
        for row in filtered_data:
            schedule_tree.insert("", "end", values=row)

    # Add filter button
    tk.Button(filter_frame, text="Apply Filters", bg="#4E4E4E", fg="white", command=apply_filters).pack(side="left", padx=5)

    schedule_window.mainloop()

def manage_showtimes():
    """Allows staff to manage showtimes."""
    manage_window = tk.Toplevel()
    manage_window.title("Manage Showtimes")
    manage_window.geometry("1000x600")
    manage_window.configure(bg="#2A2A2A")  # Dark theme

    # Create main container frame
    main_frame = tk.Frame(manage_window, bg="#2A2A2A")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Create Treeview for showtimes
    columns = ("ID", "Movie", "Date", "Time", "Hall", "Price", "Available Seats")
    showtime_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
    
    # Configure columns
    for col in columns:
        showtime_tree.heading(col, text=col)
        showtime_tree.column(col, width=140)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=showtime_tree.yview)
    showtime_tree.configure(yscrollcommand=scrollbar.set)

    # Pack the Treeview and scrollbar
    showtime_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_showtimes():
        """Refresh the showtime list."""
        # Clear current items
        for item in showtime_tree.get_children():
            showtime_tree.delete(item)

        # Load showtime data
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.id, m.title, s.show_date, s.show_time, s.hall_number, s.price, s.available_seats
            FROM Showtimes s
            JOIN Movies m ON s.movie_id = m.id
            ORDER BY s.show_date, s.show_time
        """)
        
        showtime_data = cursor.fetchall()
        conn.close()

        # Insert data into Treeview
        for row in showtime_data:
            showtime_tree.insert("", "end", values=row)

    def add_showtime():
        """Opens a window to add a new showtime."""
        add_window = tk.Toplevel(manage_window)
        add_window.title("Add Showtime")
        add_window.geometry("400x500")
        add_window.configure(bg="#2A2A2A")

        # Movie selection
        tk.Label(add_window, text="Select Movie:", fg="white", bg="#2A2A2A").pack(pady=5)
        movie_var = tk.StringVar()
        movie_combo = ttk.Combobox(add_window, textvariable=movie_var, state="readonly")
        movie_combo.pack(pady=5)

        # Load movies
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM Movies")
        movies = cursor.fetchall()
        conn.close()

        movie_dict = {}
        for movie in movies:
            movie_combo['values'] = (*movie_combo['values'], movie[1])
            movie_dict[movie[1]] = movie[0]

        # Date selection
        tk.Label(add_window, text="Select Date:", fg="white", bg="#2A2A2A").pack(pady=5)
        date_entry = ttk.Entry(add_window)
        date_entry.pack(pady=5)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Time selection
        tk.Label(add_window, text="Select Time:", fg="white", bg="#2A2A2A").pack(pady=5)
        time_var = tk.StringVar()
        time_combo = ttk.Combobox(add_window, textvariable=time_var, values=["10:00", "14:00", "18:00"], state="readonly")
        time_combo.pack(pady=5)

        # Hall selection
        tk.Label(add_window, text="Select Hall:", fg="white", bg="#2A2A2A").pack(pady=5)
        hall_var = tk.StringVar()
        hall_combo = ttk.Combobox(add_window, textvariable=hall_var, values=["1", "2", "3"], state="readonly")
        hall_combo.pack(pady=5)

        # Price entry
        tk.Label(add_window, text="Price:", fg="white", bg="#2A2A2A").pack(pady=5)
        price_entry = ttk.Entry(add_window)
        price_entry.pack(pady=5)
        price_entry.insert(0, "12.99")

        # Available seats
        tk.Label(add_window, text="Available Seats:", fg="white", bg="#2A2A2A").pack(pady=5)
        seats_entry = ttk.Entry(add_window)
        seats_entry.pack(pady=5)
        seats_entry.insert(0, "50")

        def save_showtime():
            """Saves the new showtime."""
            try:
                movie_title = movie_var.get()
                show_date = date_entry.get()
                show_time = time_var.get()
                hall = int(hall_var.get())
                price = float(price_entry.get())
                seats = int(seats_entry.get())

                if not all([movie_title, show_date, show_time, hall, price, seats]):
                    messagebox.showerror("Error", "All fields are required")
                    return

                conn = sqlite3.connect("cinema_system.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Showtimes (movie_id, show_date, show_time, hall_number, price, available_seats)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (movie_dict[movie_title], show_date, show_time, hall, price, seats))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Showtime added successfully!")
                add_window.destroy()
                refresh_showtimes()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding showtime: {str(e)}")

        tk.Button(add_window, text="Save Showtime", bg="#4E4E4E", fg="white", command=save_showtime).pack(pady=20)

    def delete_showtime():
        """Deletes the selected showtime."""
        selected_item = showtime_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a showtime to delete")
            return

        showtime_id = showtime_tree.item(selected_item[0])['values'][0]

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this showtime?"):
            conn = sqlite3.connect("cinema_system.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Showtimes WHERE id=?", (showtime_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Showtime deleted successfully!")
            refresh_showtimes()

    # Add buttons frame
    button_frame = tk.Frame(manage_window, bg="#2A2A2A")
    button_frame.pack(fill="x", pady=10)

    tk.Button(button_frame, text="Add Showtime", bg="#4E4E4E", fg="white", command=add_showtime).pack(side="left", padx=5)
    tk.Button(button_frame, text="Delete Showtime", bg="#A83232", fg="white", command=delete_showtime).pack(side="left", padx=5)

    # Initial load
    refresh_showtimes()

    manage_window.mainloop() 