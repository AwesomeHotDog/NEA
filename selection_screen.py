import tkinter as tk
import login

class SelectionScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Cinema System - Select Login Type")
        self.root.geometry("400x300")

        tk.Label(root, text="Select Login Type", font=("Arial", 14)).pack(pady=20)
        tk.Button(root, text="Staff Login", command=self.staff_login).pack(pady=10)
        tk.Button(root, text="User Login", command=self.user_login).pack(pady=10)

    def staff_login(self):
        print("Staff Login Button Clicked")  # Debugging statement
        self.root.withdraw()  # Hides the selection screen
        login.show_staff_login()  # Calls staff login function

    def user_login(self):
        self.root.withdraw()
        login.show_user_login()

if __name__ == "__main__":
    root = tk.Tk()
    app = SelectionScreen(root)
    root.mainloop()