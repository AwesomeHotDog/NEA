import sqlite3
import tkinter as tk
from tkinter import messagebox

def show_user_management():
    """Displays a list of users with management options."""
    user_window = tk.Toplevel()
    user_window.title("User Management")
    user_window.geometry("500x400")

    user_listbox = tk.Listbox(user_window, width=50)
    user_listbox.pack(pady=10)

    def refresh_users():
        """Refresh the user list."""
        user_listbox.delete(0, tk.END)
        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM User")
        users = cursor.fetchall()
        conn.close()
        for user in users:
            user_listbox.insert(tk.END, f"{user[0]} - {user[1]}")

    def delete_user():
        """Deletes the selected user."""
        selected_user = user_listbox.curselection()
        if not selected_user:
            messagebox.showerror("Error", "Please select a user to delete")
            return

        user_id = user_listbox.get(selected_user).split(" - ")[0]

        conn = sqlite3.connect("cinema_system.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM User WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "User deleted successfully!")
        refresh_users()

    tk.Button(user_window, text="Delete Selected User", command=delete_user).pack(pady=5)
    refresh_users()
