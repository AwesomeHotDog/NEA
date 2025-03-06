import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from omdb_api import fetch_movie_details
from PIL import Image, ImageTk
import requests
from io import BytesIO

def show_review_screen(username):
    """GUI for users to review a movie."""
    review_window = tk.Toplevel()
    review_window.title("Review a Movie")
    review_window.geometry("800x600")
    review_window.configure(bg="#2A2A2A")  # Dark theme

    # Create main container frame
    main_frame = tk.Frame(review_window, bg="#2A2A2A")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Left side - Movie selection and details
    left_frame = tk.Frame(main_frame, bg="#2A2A2A")
    left_frame.pack(side="left", fill="y", padx=(0, 20))

    tk.Label(left_frame, text="Select a Movie", font=("Arial", 14, "bold"), fg="white", bg="#2A2A2A").pack(pady=10)

    movie_listbox = tk.Listbox(left_frame, width=40, bg="white")
    movie_listbox.pack(pady=5)

    # Right side - Movie details, poster, and review form
    right_frame = tk.Frame(main_frame, bg="#2A2A2A")
    right_frame.pack(side="right", fill="both", expand=True)

    # Poster label
    poster_label = tk.Label(right_frame, bg="#2A2A2A")
    poster_label.pack(pady=10)

    details_text = tk.StringVar()
    details_label = tk.Label(right_frame, textvariable=details_text, wraplength=400, fg="white", bg="#2A2A2A", justify="left")
    details_label.pack(pady=10)

    # Review form
    review_frame = tk.Frame(right_frame, bg="#2A2A2A")
    review_frame.pack(fill="x", pady=10)

    tk.Label(review_frame, text="Your Rating (1-5):", fg="white", bg="#2A2A2A").pack()
    rating_var = tk.StringVar()
    rating_combo = ttk.Combobox(review_frame, textvariable=rating_var, values=["1", "2", "3", "4", "5"], state="readonly", width=5)
    rating_combo.pack(pady=5)

    tk.Label(review_frame, text="Your Review:", fg="white", bg="#2A2A2A").pack()
    review_text = tk.Text(review_frame, height=4, width=40, bg="white")
    review_text.pack(pady=5)

    # Load movies into listbox
    conn = sqlite3.connect("cinema_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM Movies")
    movies = cursor.fetchall()
    conn.close()

    movie_dict = {}  # Store movie details
    for movie in movies:
        movie_listbox.insert(tk.END, f"{movie[1]}")  # Show movie title
        movie_dict[movie[1]] = movie[0]  # Store ID mapped to title

    def show_movie_details():
        """Fetch and display movie details from OMDB API."""
        selected_index = movie_listbox.curselection()
        if not selected_index:
            details_text.set("Please select a movie.")
            poster_label.config(image="")  # Clear poster
            return

        movie_title = movie_listbox.get(selected_index)
        movie_data = fetch_movie_details(movie_title)

        if movie_data:
            # Display text details
            details_text.set(
                f"Title: {movie_data['title']}\n"
                f"Year: {movie_data['year']}\n"
                f"Genre: {movie_data['genre']}\n"
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

    def submit_review():
        """Submits a movie review."""
        selected_index = movie_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a movie to review")
            return

        movie_title = movie_listbox.get(selected_index)
        movie_id = movie_dict[movie_title]
        rating = rating_var.get()
        review = review_text.get("1.0", tk.END).strip()

        if not rating:
            messagebox.showerror("Error", "Please select a rating")
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
        review_window.destroy()

    # Buttons frame
    button_frame = tk.Frame(left_frame, bg="#2A2A2A")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Show Details", bg="#4E4E4E", fg="white", command=show_movie_details).pack(side="left", padx=5)
    tk.Button(button_frame, text="Submit Review", bg="#4E4E4E", fg="white", command=submit_review).pack(side="left", padx=5)

    review_window.mainloop()

def manage_reviews(username):
    """Allows users to edit or delete their reviews."""
    review_window = tk.Toplevel()
    review_window.title("Manage My Reviews")
    review_window.geometry("800x600")
    review_window.configure(bg="#2A2A2A")  # Dark theme

    # Create main container frame
    main_frame = tk.Frame(review_window, bg="#2A2A2A")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Left side - Review list
    left_frame = tk.Frame(main_frame, bg="#2A2A2A")
    left_frame.pack(side="left", fill="y", padx=(0, 20))

    tk.Label(left_frame, text="Your Reviews", font=("Arial", 14, "bold"), fg="white", bg="#2A2A2A").pack(pady=10)

    review_listbox = tk.Listbox(left_frame, width=50, bg="white")
    review_listbox.pack(pady=5)

    # Right side - Review details
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
    cursor.execute("""
        SELECT Reviews.id, Movies.title, Reviews.rating, Reviews.review 
        FROM Reviews 
        JOIN Movies ON Reviews.movie_id = Movies.id 
        JOIN User ON Reviews.user_id = User.id 
        WHERE User.username = ?
    """, (username,))
    reviews = cursor.fetchall()
    conn.close()

    review_dict = {}  # Store review details
    for review in reviews:
        review_text = f"{review[1]} - {review[2]}⭐"  # Movie title and rating
        review_listbox.insert(tk.END, review_text)
        review_dict[review_text] = {
            'id': review[0],
            'title': review[1],
            'rating': review[2],
            'review': review[3]
        }

    def show_review_details():
        """Show details of selected review."""
        selected_index = review_listbox.curselection()
        if not selected_index:
            details_text.set("Please select a review.")
            poster_label.config(image="")
            return

        review_text = review_listbox.get(selected_index)
        review_data = review_dict[review_text]
        movie_data = fetch_movie_details(review_data['title'])

        if movie_data:
            # Display text details
            details_text.set(
                f"Title: {movie_data['title']}\n"
                f"Year: {movie_data['year']}\n"
                f"Genre: {movie_data['genre']}\n"
                f"Your Rating: {review_data['rating']}⭐\n"
                f"Your Review: {review_data['review']}"
            )

            # Display poster
            if movie_data['poster'] and movie_data['poster'] != 'N/A':
                try:
                    response = requests.get(movie_data['poster'])
                    img_data = BytesIO(response.content)
                    img = Image.open(img_data)
                    img.thumbnail((300, 400))
                    photo = ImageTk.PhotoImage(img)
                    poster_label.config(image=photo)
                    poster_label.image = photo
                except Exception as e:
                    print(f"Error loading poster: {e}")
                    poster_label.config(image="")
            else:
                poster_label.config(image="")
        else:
            details_text.set("Movie details not found.")
            poster_label.config(image="")

    def delete_review():
        """Deletes a selected review."""
        selected_index = review_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a review to delete")
            return

        review_text = review_listbox.get(selected_index)
        review_id = review_dict[review_text]['id']

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this review?"):
            conn = sqlite3.connect("cinema_system.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Reviews WHERE id=?", (review_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Review deleted successfully!")
            review_window.destroy()
            manage_reviews(username)  # Refresh the window

    # Buttons frame
    button_frame = tk.Frame(left_frame, bg="#2A2A2A")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Show Details", bg="#4E4E4E", fg="white", command=show_review_details).pack(side="left", padx=5)
    tk.Button(button_frame, text="Delete Review", bg="#A83232", fg="white", command=delete_review).pack(side="left", padx=5)

    review_window.mainloop()