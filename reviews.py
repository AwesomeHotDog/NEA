import sqlite3
import tkinter as tk
from tkinter import messagebox

def show_review_screen(username):
    """GUI for users to review a movie."""
    review_window = tk.Toplevel()
    review_window.title("Review a Movie")
    review_window.geometry("400x400")

    tk.Label(review_window, text="Movie ID:").pack(pady=5)
    movie_id_entry = tk.Entry(review_window)
    movie_id_entry.pack(pady=5)

    tk.Label(review_window, text="Rating (1-5):").pack(pady=5)
    rating_entry = tk.Entry(review_window)
    rating_entry.pack(pady=5)

    tk.Label(review_window, text="Review:").pack(pady=5)
    review_entry = tk.Entry(review_window)
    review_entry.pack(pady=5)

    def submit_review():
        """Submits a movie review."""
        movie_id = movie_id_entry.get()
        rating = rating_entry.get()
        review = review_entry.get()

        if not movie_id or not rating:
            messagebox.showerror("Error", "Movie ID and Rating are required")
            return

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                messagebox.showerror("Error", "Rating must be between 1 and 5")
                return
        except ValueError:
            messagebox.showerror("Error", "Rating must be a number between 1 and 5")
            return

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()

        # Ensure the user exists in the database
        cursor.execute("SELECT id FROM User WHERE username=?", (username,))
        user = cursor.fetchone()
        if not user:
            messagebox.showerror("Error", "User not found")
            conn.close()
            return

        user_id = user[0]

        cursor.execute("INSERT INTO Reviews (user_id, movie_id, rating, review) VALUES (?, ?, ?, ?)",
                       (user_id, movie_id, rating, review))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Review submitted successfully!")

    tk.Button(review_window, text="Submit Review", command=submit_review).pack(pady=10)
    
def manage_reviews(username):
    """Allows users to edit or delete their reviews."""
    review_window = tk.Toplevel()
    review_window.title("Manage My Reviews")
    review_window.geometry("500x400")

    review_listbox = tk.Listbox(review_window, width=50)
    review_listbox.pack(pady=10)

    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, movie_id, rating, review FROM Reviews WHERE user_id = (SELECT id FROM User WHERE username=?)", (username,))
    reviews = cursor.fetchall()
    conn.close()

    for review in reviews:
        review_listbox.insert(tk.END, f"{review[0]} - Movie {review[1]} - {review[2]}⭐ - {review[3]}")

    def delete_review():
        """Deletes a selected review."""
        selected_review = review_listbox.curselection()
        if not selected_review:
            messagebox.showerror("Error", "Please select a review to delete")
            return

        review_id = review_listbox.get(selected_review).split(" - ")[0]

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Reviews WHERE id=?", (review_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Review deleted successfully!")
        review_window.destroy()

    tk.Button(review_window, text="Delete Selected Review", command=delete_review).pack(pady=5)