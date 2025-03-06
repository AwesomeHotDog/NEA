import sqlite3
import tkinter as tk
from tkinter import messagebox
from omdb_api import fetch_movie_details
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import ttk
from datetime import datetime

def show_movie_management():
    """Shows the movie management window."""
    movie_window = tk.Toplevel()
    movie_window.title("Movie Management")
    movie_window.geometry("800x600")
    movie_window.configure(bg="#2A2A2A")

    # Create main container frame
    main_frame = tk.Frame(movie_window, bg="#2A2A2A")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Create Treeview for movies
    columns = ("ID", "Title", "Genre", "Duration", "Release Date")
    movie_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
    
    # Configure columns
    for col in columns:
        movie_tree.heading(col, text=col)
        movie_tree.column(col, width=150)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=movie_tree.yview)
    movie_tree.configure(yscrollcommand=scrollbar.set)

    # Pack the Treeview and scrollbar
    movie_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_movies():
        """Refresh the movie list."""
        # Clear current items
        for item in movie_tree.get_children():
            movie_tree.delete(item)

        # Load movie data
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Movies ORDER BY title")
        movies = cursor.fetchall()
        conn.close()

        # Insert data into Treeview
        for movie in movies:
            movie_tree.insert("", "end", values=movie)

    def add_movie():
        """Opens a window to add a new movie."""
        add_window = tk.Toplevel(movie_window)
        add_window.title("Add Movie")
        add_window.geometry("400x400")
        add_window.configure(bg="#2A2A2A")
        add_window.transient(movie_window)  # Set as transient to movie_window
        add_window.grab_set()  # Make the window modal

        # Title entry
        tk.Label(add_window, text="Title:", fg="white", bg="#2A2A2A").pack(pady=5)
        title_entry = ttk.Entry(add_window)
        title_entry.pack(pady=5)

        # Genre entry
        tk.Label(add_window, text="Genre:", fg="white", bg="#2A2A2A").pack(pady=5)
        genre_entry = ttk.Entry(add_window)
        genre_entry.pack(pady=5)

        # Duration entry
        tk.Label(add_window, text="Duration (minutes):", fg="white", bg="#2A2A2A").pack(pady=5)
        duration_entry = ttk.Entry(add_window)
        duration_entry.pack(pady=5)

        # Release date entry
        tk.Label(add_window, text="Release Date (YYYY-MM-DD):", fg="white", bg="#2A2A2A").pack(pady=5)
        date_entry = ttk.Entry(add_window)
        date_entry.pack(pady=5)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        def save_movie():
            """Saves the new movie."""
            try:
                title = title_entry.get().strip()
                genre = genre_entry.get().strip()
                duration = int(duration_entry.get().strip())
                release_date = date_entry.get().strip()

                if not all([title, genre, duration, release_date]):
                    messagebox.showerror("Error", "All fields are required")
                    return

                conn = sqlite3.connect("cinema_system.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Movies (title, genre, duration, release_date)
                    VALUES (?, ?, ?, ?)
                """, (title, genre, duration, release_date))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Movie added successfully!")
                add_window.destroy()
                refresh_movies()
            except ValueError:
                messagebox.showerror("Error", "Duration must be a number")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding movie: {str(e)}")

        tk.Button(add_window, text="Save Movie", bg="#4E4E4E", fg="white", command=save_movie).pack(pady=20)

    def delete_movie():
        """Deletes the selected movie."""
        selected_item = movie_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a movie to delete")
            return

        movie_id = movie_tree.item(selected_item[0])['values'][0]
        movie_title = movie_tree.item(selected_item[0])['values'][1]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {movie_title}?\nThis will also delete all associated showtimes and bookings."):
            try:
                conn = sqlite3.connect("cinema_system.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Movies WHERE id=?", (movie_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Movie deleted successfully!")
                refresh_movies()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting movie: {str(e)}")

    # Add buttons frame
    button_frame = tk.Frame(movie_window, bg="#2A2A2A")
    button_frame.pack(fill="x", pady=10)

    tk.Button(button_frame, text="Add Movie", bg="#4E4E4E", fg="white", command=add_movie).pack(side="left", padx=5)
    tk.Button(button_frame, text="Delete Movie", bg="#A83232", fg="white", command=delete_movie).pack(side="left", padx=5)
    tk.Button(button_frame, text="Refresh", bg="#4E4E4E", fg="white", command=refresh_movies).pack(side="left", padx=5)

    # Initial load
    refresh_movies()

    # Make sure this window stays on top of the main window
    movie_window.transient(movie_window.master)
    movie_window.grab_set()
    movie_window.wait_window()

def show_movies():
    """Displays available movies with details and posters."""
    movies_window = tk.Toplevel()
    movies_window.title("Available Movies")
    movies_window.geometry("800x600")
    movies_window.configure(bg="#2A2A2A")  # Dark theme

    # Create main container frame
    main_frame = tk.Frame(movies_window, bg="#2A2A2A")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Left side - Movie list
    left_frame = tk.Frame(main_frame, bg="#2A2A2A")
    left_frame.pack(side="left", fill="y", padx=(0, 20))

    tk.Label(left_frame, text="Available Movies", font=("Arial", 14, "bold"), fg="white", bg="#2A2A2A").pack(pady=10)

    movie_listbox = tk.Listbox(left_frame, width=40, bg="white")
    movie_listbox.pack(pady=5)

    # Right side - Movie details and poster
    right_frame = tk.Frame(main_frame, bg="#2A2A2A")
    right_frame.pack(side="right", fill="both", expand=True)

    # Poster label
    poster_label = tk.Label(right_frame, bg="#2A2A2A")
    poster_label.pack(pady=10)

    details_text = tk.StringVar()
    details_label = tk.Label(right_frame, textvariable=details_text, wraplength=400, fg="white", bg="#2A2A2A", justify="left")
    details_label.pack(pady=10)

    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, genre, duration, release_date FROM Movies")
    movies = cursor.fetchall()
    conn.close()

    movie_dict = {}  # Store movie details
    for movie in movies:
        movie_listbox.insert(tk.END, f"{movie[1]}")  # Show movie title
        movie_dict[movie[1]] = {
            'id': movie[0],
            'genre': movie[2],
            'duration': movie[3],
            'release_date': movie[4]
        }

    def show_movie_details():
        """Fetch and display movie details from OMDB API."""
        selected_index = movie_listbox.curselection()
        if not selected_index:
            details_text.set("Please select a movie.")
            poster_label.config(image="")  # Clear poster
            return

        movie_title = movie_listbox.get(selected_index)
        movie_data = fetch_movie_details(movie_title)
        db_data = movie_dict[movie_title]

        if movie_data:
            # Display text details
            details_text.set(
                f"Title: {movie_data['title']}\n"
                f"Year: {movie_data['year']}\n"
                f"Genre: {movie_data['genre']}\n"
                f"Duration: {db_data['duration']} minutes\n"
                f"Release Date: {db_data['release_date']}\n"
                f"IMDb Rating: {movie_data['rating']}\n"
                f"Plot: {movie_data['plot']}"
            )

            # Display poster
            if movie_data['poster'] and movie_data['poster'] != 'N/A':
                try:
                    response = requests.get(movie_data['poster'])
                    img_data = BytesIO(response.content)
                    img = Image.open(img_data)
                    # Resize image to fit window while maintaining aspect ratio
                    img.thumbnail((300, 400))  # Max size for poster
                    photo = ImageTk.PhotoImage(img)
                    poster_label.config(image=photo)
                    poster_label.image = photo  # Keep a reference
                except Exception as e:
                    print(f"Error loading poster: {e}")
                    poster_label.config(image="")
            else:
                poster_label.config(image="")
        else:
            details_text.set("Movie details not found.")
            poster_label.config(image="")

    # Buttons frame
    button_frame = tk.Frame(left_frame, bg="#2A2A2A")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Show Details", bg="#4E4E4E", fg="white", command=show_movie_details).pack(side="left", padx=5)

    movies_window.mainloop()

def filter_movies(genre=None, min_duration=0, max_duration=300):
    """Fetch movies based on user-defined filters."""
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    
    query = "SELECT id, title, genre, duration, release_date FROM Movies WHERE duration BETWEEN ? AND ?"
    params = (min_duration, max_duration)
    
    if genre:
        query += " AND genre = ?"
        params += (genre,)
    
    cursor.execute(query, params)
    movies = cursor.fetchall()
    conn.close()
    
    return movies  # Return filtered list to display
