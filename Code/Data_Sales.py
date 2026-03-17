import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error

# Σύνδεση στη βάση δεδομένων
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='pantrypal',
            user='root',
            password='3315'
        )
        if connection.is_connected():
            print("Η σύνδεση με τη βάση δεδομένων ήταν επιτυχής")
        return connection
    except Error as e:
        print(f"Σφάλμα κατά τη σύνδεση στη MySQL: {e}")
        return None

# Ανάκτηση προφίλ σερβιτόρων από τη βάση δεδομένων
def get_waiter_profiles():
    connection = create_connection()
    waiters = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT idUser, usernameUser FROM users WHERE role = 'Waiter'")
            waiters = cursor.fetchall()
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Failed to retrieve waiters: {e}")
    return waiters

# Υπολογισμός συνολικού ποσού πωλήσεων για επιλεγμένο σερβιτόρο και ημερομηνία
def calculate_total_sales(waiter_id, date):
    connection = create_connection()
    total_sales = 0.0
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT SUM(amount) 
                FROM sales 
                WHERE idOfWaiter = %s AND dateSale = %s
            """, (waiter_id, date))
            result = cursor.fetchone()
            if result and result[0]:
                total_sales = result[0]
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Failed to calculate sales: {e}")
    return total_sales

# Δημιουργία της εφαρμογής με Tkinter
class SalesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Management")

        # Επιλογή σερβιτόρου
        self.waiter_label = tk.Label(root, text="Select Waiter")
        self.waiter_label.pack(pady=5)
        self.waiter_combobox = ttk.Combobox(root)
        self.waiter_combobox.pack(pady=5)
        self.load_waiters()

        # Επιλογή ημερομηνίας
        self.date_label = tk.Label(root, text="Select Date")
        self.date_label.pack(pady=5)
        self.date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(pady=5)

        # Κουμπί υπολογισμού πωλήσεων
        self.calculate_button = tk.Button(root, text="Calculate Sales", command=self.calculate_sales)
        self.calculate_button.pack(pady=20)

        # Εμφάνιση αποτελέσματος
        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

    def load_waiters(self):
        waiters = get_waiter_profiles()
        self.waiter_combobox['values'] = [f"{waiter[1]} (ID: {waiter[0]})" for waiter in waiters]

    def calculate_sales(self):
        selected_waiter = self.waiter_combobox.get()
        if selected_waiter:
            try:
                waiter_id = int(selected_waiter.split("(ID: ")[1][:-1])
                date = self.date_entry.get_date().strftime('%Y-%m-%d')
                total_sales = calculate_total_sales(waiter_id, date)
                self.result_label.config(text=f"Total Sales: {total_sales:.2f}")
            except IndexError:
                messagebox.showerror("Selection Error", "Invalid waiter selection")
            except ValueError:
                messagebox.showerror("Selection Error", "Failed to parse waiter ID")
        else:
            messagebox.showwarning("Selection Error", "Please select a waiter")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesApp(root)
    root.mainloop()
