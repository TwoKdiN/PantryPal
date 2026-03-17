import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def login(self):
        role = self.verify_credentials()
        if role:
            if role == 'Manager':
                messagebox.showinfo("Login", f"{self.username} has logged in as Manager.")
                self.open_manager_window()
            elif role == 'Waiter':
                messagebox.showinfo("Login", f"{self.username} has logged in as Waiter.")
                self.open_waiter_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def logout(self):
        messagebox.showinfo("Logout", f"{self.username} has logged out.")

    def verify_credentials(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='pantrypal',
                user='root',
                password='3315'
            )
            cursor = connection.cursor()
            cursor.execute('SELECT role FROM users WHERE usernameUser = %s AND passwordUser = %s', (self.username, self.password))
            result = cursor.fetchone()
            connection.close()
            if result:
                return result[0]  # Επιστρέφει τον ρόλο του χρήστη
            return None
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return False

    def open_manager_window(self):
        manager_window = tk.Toplevel()
        manager_window.title("Manager Panel")
        manager_window.geometry("400x400")
        
        buttons = [
            ("Δημιουργία Συνταγής", "D:/ΣΧΟΛΗ/Τεχνολογια Λογισμικου/Code/Recipe.py"), ############
            ("Προβολή Υλικών", "D:/ΣΧΟΛΗ/Τεχνολογια Λογισμικου/Code/Show_Ingredient.py"), ############
            ("Έλεγχος Πωλήσεων", "D:/ΣΧΟΛΗ/Τεχνολογια Λογισμικου/Code/Data_Sales.py"), ############
            ("Διαγραφή Υλικού", "D:/ΣΧΟΛΗ/Τεχνολογια Λογισμικου/Code/Delete_Ingredient.py"), ############
            ("Δημιουργία Παραγγελίας προς Προμηθευτή", "D:/ΣΧΟΛΗ/Τεχνολογια Λογισμικου/Code/Supplier_Order.py"), ############
            ("Ενημέρωση Αποθήκης", "D:/ΣΧΟΛΗ/Τεχνολογια Λογισμικου/Code/Update_Base.py"), ############
            ("Εισαγωγή Υλικού", "D:/ΣΧΟΛΗ/Τεχνολογια Λογισμικου/Code/Add_Ingredient.py") ############
        ]
        
        for button_text, script_path in buttons:
            btn = tk.Button(manager_window, text=button_text, command=lambda p=script_path: subprocess.Popen(["python", p]))
            btn.pack(fill='x', padx=10, pady=5)
            
    def open_waiter_window(self):
        waiter_window = tk.Toplevel()
        waiter_window.title("Waiter Panel")
        waiter_window.geometry("400x300")
    
        buttons = [
            ("Προβολή Τραπεζιών", "D:/ΣΧΟΛΗ/Τεχνολογια Λογισμικου/Code/Table.py"),
            ("Δημιουργία Παραγγελίας", "D:/ΣΧΟΛΗ/Τεχνολογια Λογισμικου/Code/Create_Order.py"),
            ("Πληρωμή", "D:/ΣΧΟΛΗ/Τεχνολογια Λογισμικου/Code/")
            ]
    
        for button_text, script_path in buttons:
            btn = tk.Button(waiter_window, text=button_text, command=lambda p=script_path: subprocess.Popen(["python", p]))
            btn.pack(fill='x', padx=10, pady=5)
        
        
def main():
    def login_action():
        username = user_text.get()
        password = password_text.get()
        user = User(username, password)
        user.login()

    def logout_action():
        username = user_text.get()
        password = password_text.get()
        user = User(username, password)
        user.logout()

    # Create the main window
    root = tk.Tk()
    root.title("User Login/Logout Test")
    root.geometry("400x200")
    root.grid_columnconfigure(1, weight=1)

    # Username label and text entry box
    user_label = tk.Label(root, text="Username:")
    user_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
    user_text = tk.Entry(root)
    user_text.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    # Password label and password entry box
    password_label = tk.Label(root, text="Password:")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    password_text = tk.Entry(root, show='*')
    password_text.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

    # Login button
    login_button = tk.Button(root, text="Login", command=login_action)
    login_button.grid(row=3, column=0, padx=10, pady=10)

    # Logout button
    logout_button = tk.Button(root, text="Logout", command=logout_action)
    logout_button.grid(row=3, column=1, padx=10, pady=10)

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()

