import sqlite3
import tkinter as tk
from tkinter import messagebox

def show_movie_management():
    """GUI for staff to add and delete movies."""
    movie_window = tk.Toplevel()
    movie_window.title("Manage Movies")
    movie_window.geometry("500x600")

    tk.Label(movie_window, text="Movie Title:").pack(pady=5)
    title_entry = tk.Entry(movie_window)
    title_entry.pack(pady=5)

    tk.Label(movie_window, text="Genre:").pack(pady=5)
    genre_entry = tk.Entry(movie_window)
    genre_entry.pack(pady=5)

    tk.Label(movie_window, text="Duration (minutes):").pack(pady=5)
    duration_entry = tk.Entry(movie_window)
    duration_entry.pack(pady=5)

    tk.Label(movie_window, text="Release Date (YYYY-MM-DD):").pack(pady=5)
    release_date_entry = tk.Entry(movie_window)
    release_date_entry.pack(pady=5)

    def add_movie():
        """Inserts a new movie into the database."""
        title = title_entry.get()
        genre = genre_entry.get()
        duration = duration_entry.get()
        release_date = release_date_entry.get()

        if not title or not genre or not duration or not release_date:
            messagebox.showerror("Error", "All fields are required")
            return

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Movies (title, genre, duration, release_date) VALUES (?, ?, ?, ?)",
                       (title, genre, duration, release_date))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Movie added successfully!")
        refresh_movie_list()

    tk.Button(movie_window, text="Add Movie", command=add_movie).pack(pady=10)

    # Movie List Section
    tk.Label(movie_window, text="Existing Movies").pack(pady=10)
    movie_listbox = tk.Listbox(movie_window, width=50)
    movie_listbox.pack(pady=5)

    def refresh_movie_list():
        """Refreshes the movie list after adding/deleting a movie."""
        movie_listbox.delete(0, tk.END)
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM Movies")
        movies = cursor.fetchall()
        conn.close()
        for movie in movies:
            movie_listbox.insert(tk.END, f"{movie[0]} - {movie[1]}")

    def delete_movie():
        """Deletes a selected movie from the database."""
        selected_movie = movie_listbox.curselection()
        if not selected_movie:
            messagebox.showerror("Error", "Please select a movie to delete")
            return

        movie_id = movie_listbox.get(selected_movie).split(" - ")[0]

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Movies WHERE id=?", (movie_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Movie deleted successfully!")
        refresh_movie_list()

    tk.Button(movie_window, text="Delete Selected Movie", command=delete_movie).pack(pady=10)

    refresh_movie_list()  # Load existing movies when opening the window


def show_movies():
    """Displays available movies in a new window."""
    movies_window = tk.Toplevel()
    movies_window.title("Available Movies")
    movies_window.geometry("500x400")

    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, genre, duration, release_date FROM Movies")
    movies = cursor.fetchall()
    conn.close()

    for movie in movies:
        tk.Label(movies_window, text=f"{movie[0]}. {movie[1]} - {movie[2]} ({movie[3]} min) - {movie[4]}").pack(pady=5)
