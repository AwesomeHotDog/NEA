import tkinter as tk
import login  # Import login module to show login screens

def show_selection_screen():
    """Displays the selection screen for user or staff login."""
    root = tk.Tk()
    root.title("Cinema System - Select Login Type")
    root.geometry("400x300")

    tk.Label(root, text="Select Login Type", font=("Arial", 16)).pack(pady=20)

    # Button to select staff login
    tk.Button(root, text="Staff Login", width=20, command=lambda: open_staff_login(root)).pack(pady=10)

    # Button to select user login
    tk.Button(root, text="User Login", width=20, command=lambda: open_user_login(root)).pack(pady=10)

    root.mainloop()

def open_staff_login(root):
    """Opens the staff login screen."""
    root.destroy()
    login.show_staff_login()

def open_user_login(root):
    """Opens the user login screen."""
    root.destroy()
    login.show_user_login()

if __name__ == "__main__":
    show_selection_screen()
