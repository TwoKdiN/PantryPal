import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error
from mysql.connector import connect

def create_connection():
    try:
        connection = connect(
            host='localhost',
            database='pantrypal',
            user='root',
            password='3315'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

class TableSelectionWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Table Selection")

        self.tables_frame = tk.Frame(self.root)
        self.tables_frame.pack()

        self.load_tables()

    def load_tables(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT idTable, status FROM tableNo")
                tables = cursor.fetchall()
                cursor.close()
                connection.close()

                for table in tables:
                    button_text = f"Table {table[0]} - {table[1]}"
                    table_button = tk.Button(self.tables_frame, text=button_text, command=lambda t=table[0]: self.open_table_menu(t))
                    table_button.pack(fill=tk.BOTH, expand=True)

            except Error as e:
                print(f"Error loading tables: {e}")

    def open_table_menu(self, table_id):
        table_menu = tk.Toplevel(self.root)
        table_menu.title(f"Table {table_id} Menu")

        create_order_button = tk.Button(table_menu, text="Δημιουργία νέας παραγγελίας", command=lambda: self.create_order(table_id))
        create_order_button.pack(fill=tk.BOTH, expand=True)

        payment_button = tk.Button(table_menu, text="Πληρωμή τραπεζιού", command=lambda: self.pay_table(table_id))
        payment_button.pack(fill=tk.BOTH, expand=True)

    def create_order(self, table_id):
        CreateOrderWindow(self.root, table_id)

    def pay_table(self, table_id):
        messagebox.showinfo("Pay Table", f"Processing payment for table {table_id}")
        
    def open_table_menu(self, table_id):
        table_menu = tk.Toplevel(self.root)
        table_menu.title(f"Table {table_id} Menu")

        create_order_button = tk.Button(table_menu, text="Δημιουργία νέας παραγγελίας", command=lambda: self.create_order(table_id))
        create_order_button.pack(fill=tk.BOTH, expand=True)

        view_orders_button = tk.Button(table_menu, text="Προβολή παραγγελιών", command=lambda: self.view_orders(table_id))
        view_orders_button.pack(fill=tk.BOTH, expand=True)

        payment_button = tk.Button(table_menu, text="Πληρωμή τραπεζιού", command=lambda: self.pay_table(table_id))
        payment_button.pack(fill=tk.BOTH, expand=True)

    def view_orders(self, table_id):
        # Λειτουργικότητα για την προβολή των παραγγελιών ενός τραπεζιού
        view_orders_window = tk.Toplevel(self.root)
        view_orders_window.title(f"Παραγγελίες τραπεζιού {table_id}")

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT Orders.order_id, plate.namePlate, OrderItems.quantity, OrderItems.special_requests FROM Orders "
                               "INNER JOIN OrderItems ON Orders.order_id = OrderItems.order_id "
                               "INNER JOIN plate ON OrderItems.menu_item_id = plate.idPlate "
                               "WHERE Orders.table_id = %s", (table_id,))
                orders = cursor.fetchall()
                cursor.close()
                connection.close()

                orders_tree = ttk.Treeview(view_orders_window, columns=("OrderID", "Item", "Quantity", "Special Requests"), show='headings')
                orders_tree.heading("OrderID", text="Order ID")
                orders_tree.heading("Item", text="Item")
                orders_tree.heading("Quantity", text="Quantity")
                orders_tree.heading("Special Requests", text="Special Requests")
                orders_tree.pack(fill=tk.BOTH, expand=True)

                for order in orders:
                    orders_tree.insert("", tk.END, values=order)

            except Error as e:
                print(f"Error loading orders: {e}")

class CreateOrderWindow:
    def __init__(self, parent, table_id):
        self.table_id = table_id
        self.order_items = []
        self.special_requests = ""

        self.window = tk.Toplevel(parent)
        self.window.title(f"Create Order for Table {table_id}")

        self.menu_frame = tk.Frame(self.window)
        self.menu_frame.pack()

        self.load_menu()

        self.special_requests_label = tk.Label(self.window, text="Σχόλια/Αλλεργίες:")
        self.special_requests_label.pack()
        self.special_requests_entry = tk.Entry(self.window)
        self.special_requests_entry.pack()

        self.add_item_button = tk.Button(self.window, text="Προσθήκη στο τραπέζι", command=self.add_item)
        self.add_item_button.pack(fill=tk.BOTH, expand=True)

        self.confirm_button = tk.Button(self.window, text="Επιβεβαίωση Παραγγελίας", command=self.confirm_order)
        self.confirm_button.pack(fill=tk.BOTH, expand=True)

        self.cancel_button = tk.Button(self.window, text="Ακύρωση", command=self.window.destroy)
        self.cancel_button.pack(fill=tk.BOTH, expand=True)

    def load_menu(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT idPlate, namePlate, price FROM plate")
                menu_items = cursor.fetchall()
                cursor.close()
                connection.close()

                self.menu_tree = ttk.Treeview(self.menu_frame, columns=("ID", "Name", "Price"), show='headings')
                self.menu_tree.heading("ID", text="ID")
                self.menu_tree.heading("Name", text="Name")
                self.menu_tree.heading("Price", text="Price")
                self.menu_tree.pack(fill=tk.BOTH, expand=True)

                for item in menu_items:
                    self.menu_tree.insert("", tk.END, values=item)

            except Error as e:
                print(f"Error loading menu: {e}")

    def add_item(self):
        selected_item = self.menu_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a menu item to add.")
            return

        item = self.menu_tree.item(selected_item, "values")
        self.order_items.append(item)
        messagebox.showinfo("Item Added", f"Added {item[1]} to the order.")

    def confirm_order(self):
        self.special_requests = self.special_requests_entry.get()
        confirm = messagebox.askyesno("Confirm Order", "Are you sure you want to confirm the order?")
        if confirm:
            self.save_order()
            messagebox.showinfo("Order Confirmed", "Your order has been confirmed.")
            self.window.destroy()
        else:
            cancel_confirm = messagebox.askyesno("Cancel Order", "Do you want to cancel the order?")
            if cancel_confirm:
                self.window.destroy()

    def save_order(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()

                cursor.execute("INSERT INTO Orders (table_id, waiter_id) VALUES (%s, %s)", (self.table_id, 6))  # Assume waiter_id is 1 for now
                order_id = cursor.lastrowid

                for item in self.order_items:
                    cursor.execute("INSERT INTO OrderItems (order_id, menu_item_id, quantity, special_requests) VALUES (%s, %s, %s, %s)",
                                   (order_id, item[0], 1, self.special_requests))

                cursor.execute("UPDATE tableNo SET status = 'Available', orderId = %s WHERE idTable = %s", (order_id, self.table_id))

                connection.commit()
                cursor.close()
                connection.close()
            except Error as e:
                print(f"Error saving order: {e}")
                


def main():
    root = tk.Tk()
    app = TableSelectionWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
