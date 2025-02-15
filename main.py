import tkinter as tk
from database import initialize_database 
from database import populate_movies
import login
import register

def main():
    """Main function to initialize the database and launch the application."""
    initialize_database()  # Ensure database and tables exist
    populate_movies()

    root = tk.Tk()
    root.title("Cinema Booking System")
    root.geometry("500x400")

    tk.Label(root, text="Welcome to the Cinema Booking System", font=("Arial", 16)).pack(pady=20)
    
    tk.Button(root, text="User Login", command=login.show_user_login).pack(pady=10)
    tk.Button(root, text="Staff Login", command=login.show_staff_login).pack(pady=10)
    tk.Button(root, text="Register", command=register.show_registration).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
